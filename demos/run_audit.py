"""
run_audit.py — Cosmic OS Unified Audit Entry Point
Detects changes → runs all checks → attempts fixes → loops until clean

Usage:
  python3 demos/run_audit.py              # headless, full audit
  python3 demos/run_audit.py --visual     # opens browser (requires mode-browser)
  python3 demos/run_audit.py --dims UJ,API,SEC  # specific dimensions only

Self-healing loop:
  Run 1: full audit → collect failures
  Run 2: attempt fixes → re-audit
  Run 3: re-audit → escalate unresolved to fix_queue.json
  Writes history to ~/.agent/memory/working/AUDIT_MEMORY.json
"""

import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT  = Path(__file__).parent.parent
REPORT_PATH   = PROJECT_ROOT / "docs" / "AUDIT_REPORT.md"
SPEC_PATH     = PROJECT_ROOT / "docs" / "AUDIT_SPEC.md"
FIX_QUEUE     = PROJECT_ROOT / "docs" / "fix_queue.json"
MEMORY_PATH   = Path.home() / "Dev/.agent/memory/working/AUDIT_MEMORY.json"
MAX_ATTEMPTS  = 3

VISUAL    = "--visual" in sys.argv
DIM_FILTER = None
for arg in sys.argv:
    if arg.startswith("--dims="):
        DIM_FILTER = set(arg.split("=")[1].upper().split(","))

# ── Change detection ──────────────────────────────────────

def get_changed_files():
    try:
        r = subprocess.run(
            ["git", "diff", "HEAD~1", "--name-only"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5
        )
        files = [f for f in r.stdout.strip().split("\n") if f]
        if not files:
            # Fall back to staged/unstaged changes
            r2 = subprocess.run(
                ["git", "status", "--short"],
                cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5
            )
            files = [l[3:].strip() for l in r2.stdout.strip().split("\n") if l]
        return files
    except Exception:
        return []

def priority_dims(changed_files):
    if DIM_FILTER:
        return DIM_FILTER
    dims = set()
    for f in changed_files:
        if any(x in f for x in ["static", ".html", ".css", ".js", "style"]):
            dims.update(["UJ", "CQ", "DT", "FC"])
        if any(x in f for x in ["main.py", "api", "route", "endpoint"]):
            dims.update(["API", "RES"])
        if any(x in f for x in ["auth", ".env", "secret"]):
            dims.add("SEC")
        if any(x in f for x in ["engine.py", "astro", "timing", "numerology"]):
            dims.update(["API", "FC"])
    return dims if dims else {"ALL"}

# ── Audit runners ─────────────────────────────────────────

def run_master_audit():
    """Run master_audit.py, return (stdout, pass_count, warn_count, fail_count, failures)."""
    args = [sys.executable, "demos/master_audit.py"]
    if VISUAL:
        args.append("--visual")
    result = subprocess.run(args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=300)
    output = result.stdout + result.stderr

    # Parse canonical summary line rather than counting raw emojis (avoids double-counting)
    summary = re.search(r"✅\s+(\d+)\s+⚠️\s+(\d+)\s+❌\s+(\d+)", output)
    if summary:
        passes = int(summary.group(1))
        warns  = int(summary.group(2))
        fails  = int(summary.group(3))
    else:
        passes = len(re.findall(r"✅", output))
        warns  = len(re.findall(r"⚠️", output))
        fails  = len(re.findall(r"❌", output))

    # Collect per-check failures, excluding the summary line itself
    SUMMARY_RE = re.compile(r"✅\s+\d+\s+⚠️\s+\d+\s+❌\s+\d+")
    failures = []
    for line in output.split("\n"):
        if ("❌" in line or "⚠️" in line) and not SUMMARY_RE.search(line):
            failures.append(line.strip())

    return output, passes, warns, fails, failures

def run_visual_demo():
    """Run visual_demo.py separately (only when --visual flag set)."""
    if not VISUAL:
        return "", 0, 0, 0, []
    args = [sys.executable, "demos/visual_demo.py"]
    result = subprocess.run(args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=600)
    output = result.stdout + result.stderr

    # Parse canonical final summary line (avoids counting per-act summaries)
    # visual_demo.py prints: "✅ N working  ⚠️  N needs attention  ❌ N broken"
    final_summary = re.search(r"✅\s+(\d+)\s+working\s+⚠️\s+(\d+)\s+needs attention\s+❌\s+(\d+)\s+broken", output)
    if final_summary:
        passes = int(final_summary.group(1))
        warns  = int(final_summary.group(2))
        fails  = int(final_summary.group(3))
    else:
        passes = output.count("✅")
        warns  = output.count("⚠️")
        fails  = output.count("❌")

    # Exclude per-act summaries (✅N ⚠️ N ❌N) and final summary from failures
    SUMMARY_RE = re.compile(r"✅\s*\d+.*⚠️.*\d+.*❌.*\d+")
    failures = [l.strip() for l in output.split("\n")
                if ("❌" in l or "⚠️" in l) and not SUMMARY_RE.search(l)]
    return output, passes, warns, fails, failures

# ── Fix logic ─────────────────────────────────────────────

# Simple pattern-based auto-fixes (no AI needed)
SIMPLE_FIX_PATTERNS = [
    {
        "match": r"lat=999 returned 200",
        "file": "src/main.py",
        "desc": "Add lat/lon boundary validation",
        "auto": False  # requires code change — queue for human
    },
    {
        "match": r"Invalid date.*returned 200",
        "file": "src/main.py",
        "desc": "Add date range validation (1900-2100)",
        "auto": False
    },
    {
        "match": r"video.*Estaa",
        "file": "demos/visual_demo.py",
        "desc": "Fix video recording path from Estaa to Jyotish",
        "auto": True,
        "old": 'record_video_dir="/Users/pranavsinghal/Dev/professional/Estaa/videos/"',
        "new": 'record_video_dir="/tmp/cosmic_os_audit_videos/"'
    },
]

def attempt_simple_fixes(failures):
    """Apply pattern-matched auto-fixes. Returns count of fixes applied."""
    applied = 0
    fix_queue = []

    for failure in failures:
        matched = False
        for pattern in SIMPLE_FIX_PATTERNS:
            if re.search(pattern["match"], failure, re.IGNORECASE):
                matched = True
                if pattern.get("auto") and pattern.get("old"):
                    fpath = PROJECT_ROOT / pattern["file"]
                    try:
                        src = fpath.read_text()
                        if pattern["old"] in src:
                            fpath.write_text(src.replace(pattern["old"], pattern["new"], 1))
                            print(f"  AUTO-FIX applied: {pattern['desc']}")
                            applied += 1
                    except Exception as e:
                        print(f"  AUTO-FIX failed: {e}")
                else:
                    fix_queue.append({
                        "failure": failure,
                        "file": pattern["file"],
                        "description": pattern["desc"],
                        "timestamp": datetime.now().isoformat()
                    })
        if not matched:
            fix_queue.append({
                "failure": failure,
                "file": "unknown",
                "description": "No auto-fix pattern matched — human review needed",
                "timestamp": datetime.now().isoformat()
            })

    # Write fix queue
    if fix_queue:
        existing = []
        if FIX_QUEUE.exists():
            try:
                existing = json.loads(FIX_QUEUE.read_text())
            except Exception:
                pass
        FIX_QUEUE.write_text(json.dumps(existing + fix_queue, indent=2))
        print(f"  {len(fix_queue)} items written to docs/fix_queue.json")

    return applied

# ── Memory ────────────────────────────────────────────────

def write_memory(runs, final_fails, final_warns):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = {}
    if MEMORY_PATH.exists():
        try:
            history = json.loads(MEMORY_PATH.read_text())
        except Exception:
            pass

    history[datetime.now().isoformat()] = {
        "project": "jyotish-engine-core",
        "runs": runs,
        "final_fails": final_fails,
        "final_warns": final_warns,
        "remaining_failures": final_fails,
        "fix_queue": str(FIX_QUEUE) if FIX_QUEUE.exists() else None
    }

    # Keep last 20 runs
    keys = sorted(history.keys())[-20:]
    history = {k: history[k] for k in keys}
    MEMORY_PATH.write_text(json.dumps(history, indent=2))

# ── Report writer ─────────────────────────────────────────

def write_report(all_output, passes, warns, fails, attempt):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Cosmic OS — Audit Report",
        f"**Run:** {ts} | run_audit.py (attempt {attempt})",
        f"**Score:** ✅ {passes} · ⚠️  {warns} · ❌ {fails} (total {passes+warns+fails})",
        "",
        "> Paste summary into `docs/AUDIT_SPEC.md → LAST REPORT SUMMARY`.",
        "> For every ❌ or ⚠️, add a tighter check to the relevant dimension in AUDIT_SPEC.md.",
        "",
        "## Raw Output",
        "```",
        all_output[:8000],  # cap at 8k chars
        "```",
    ]
    REPORT_PATH.write_text("\n".join(lines))

# ── Main ──────────────────────────────────────────────────

def main():
    print(f"\n{'═'*58}")
    print(f"  COSMIC OS — UNIFIED AUDIT RUNNER")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  visual={'ON' if VISUAL else 'OFF'}")
    print(f"{'═'*58}")

    # Step 1: Change detection
    changed = get_changed_files()
    dims = priority_dims(changed)
    if changed:
        print(f"\n  Changed files: {', '.join(changed[:5])}{' ...' if len(changed) > 5 else ''}")
    print(f"  Priority dimensions: {', '.join(sorted(dims))}")

    all_passes = all_warns = all_fails = 0
    all_failures = []
    run_log = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n{'─'*58}")
        print(f"  RUN {attempt} / {MAX_ATTEMPTS}")
        print(f"{'─'*58}")

        # Step 2: Run master audit
        output, passes, warns, fails, failures = run_master_audit()
        all_passes, all_warns, all_fails = passes, warns, fails

        # Step 3: Run visual demo if requested
        if VISUAL:
            print(f"\n  Running visual demo (7-act user journey)...")
            v_out, v_pass, v_warn, v_fail, v_fail_list = run_visual_demo()
            output += "\n" + v_out
            all_passes += v_pass
            all_warns  += v_warn
            all_fails  += v_fail
            failures   += v_fail_list

        run_log.append({
            "attempt": attempt,
            "passes": all_passes, "warns": all_warns, "fails": all_fails,
            "failure_count": len(failures)
        })

        print(f"\n  Score: ✅ {all_passes}  ⚠️  {all_warns}  ❌ {all_fails}")

        if all_fails == 0 and all_warns == 0:
            print(f"\n  ✅ ALL CHECKS CLEAN on attempt {attempt}")
            break

        if attempt < MAX_ATTEMPTS:
            print(f"\n  Attempting fixes for {len(failures)} issues...")
            fixed = attempt_simple_fixes(failures)
            print(f"  {fixed} auto-fixes applied. Re-running...")
        else:
            print(f"\n  ⚠️  Max attempts reached.")
            all_failures = failures
            attempt_simple_fixes(failures)

    # Step 4: Write report
    write_report(output, all_passes, all_warns, all_fails, attempt)

    # Step 5: Write memory
    write_memory(run_log, all_fails, all_warns)

    # Step 6: Summary
    print(f"\n{'═'*58}")
    print(f"  AUDIT COMPLETE")
    print(f"  Final: ✅ {all_passes}  ⚠️  {all_warns}  ❌ {all_fails}")
    print(f"  Report  → docs/AUDIT_REPORT.md")
    print(f"  Memory  → {MEMORY_PATH}")
    if FIX_QUEUE.exists():
        q = json.loads(FIX_QUEUE.read_text())
        print(f"  Fix queue → docs/fix_queue.json ({len(q)} items need human review)")
    print(f"{'═'*58}\n")

    # Exit non-zero if failures remain
    sys.exit(1 if all_fails > 0 else 0)

if __name__ == "__main__":
    main()
