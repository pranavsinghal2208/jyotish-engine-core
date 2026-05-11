import os, sys, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== STARTUP DIAGNOSTIC ===", flush=True)

# Step 1: Test pyswisseph
try:
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    jd = swe.julday(2000, 1, 1, 12.0)
    swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    print("OK: pyswisseph", flush=True)
except Exception as e:
    print(f"FAIL: pyswisseph — {e}", flush=True)
    traceback.print_exc()

# Step 2: Test heavy imports one by one
imports = [
    ("fastapi", "from fastapi import FastAPI"),
    ("sqlalchemy", "from sqlalchemy import create_engine"),
    ("google_auth", "from google_auth_oauthlib.flow import Flow"),
    ("jose", "from jose import jwt"),
    ("src.engine", "from src.engine import JyotishEngine"),
    ("src.database", "from src.database.session import init_db"),
    ("src.auth.google", "from src.auth.google_auth import GoogleAuthManager"),
    ("src.auth.apple", "from src.auth.apple_auth import AppleAuthManager"),
    ("src.numerology", "from src.numerology import NumerologyEngine"),
    ("src.astro_tools", "from src.astro_tools import detect_yogas"),
    ("src.core", "from src.core.context import CosmicContext"),
    ("src.services", "from src.services.transits import get_live_transits"),
    ("src.api", "from src.api.router import router"),
]
for name, stmt in imports:
    try:
        exec(stmt)
        print(f"OK: {name}", flush=True)
    except Exception as e:
        print(f"FAIL: {name} — {e}", flush=True)
        traceback.print_exc()

# Step 3: Try full app import
try:
    from src.main import app
    print("OK: src.main full import", flush=True)
except Exception as e:
    print(f"FAIL: src.main — {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)

import uvicorn
port = int(os.environ.get("PORT", 8000))
print(f"Starting uvicorn on port {port}", flush=True)
uvicorn.run(app, host="0.0.0.0", port=port)
