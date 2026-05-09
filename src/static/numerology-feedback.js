// ── Gender toggle ─────────────────────────────────────────────

function setGender(gender) {
    document.getElementById('gender').value = gender;
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `gender${gender}`);
    });
}

// ── Jyotish Numerology — current user ─────────────────────────

async function loadMyNumerology() {
    const birthDate = document.getElementById('date').value;
    const fullName  = document.getElementById('fullName').value.trim();
    const gender    = document.getElementById('gender')?.value || 'Male';

    const nameReqEl = document.getElementById('jyNameRequired');
    if (!birthDate || !fullName) {
        if (nameReqEl) nameReqEl.classList.remove('hidden');
        return;
    }
    if (nameReqEl) nameReqEl.classList.add('hidden');
    loadPersonalCycles(birthDate);
    loadForecast();
    populateCompatibilityDropdowns();

    const loadingEl = document.getElementById('jyLoadingState');
    const panel     = document.getElementById('jyProfilePanel');
    if (loadingEl) loadingEl.classList.remove('hidden');
    panel.classList.add('hidden');

    try {
        const res = await fetch('/api/numerology/jyotish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ birth_date: birthDate, full_name: fullName, gender })
        });
        if (!res.ok) throw new Error('Numerology calculation failed');
        const d = await res.json();

        document.getElementById('jyName').textContent = fullName;
        const dt = new Date(birthDate + 'T12:00:00');
        const dobDisplay = `${String(dt.getDate()).padStart(2,'0')}-${String(dt.getMonth()+1).padStart(2,'0')}-${dt.getFullYear()}`;
        document.getElementById('jyMeta').textContent = `${gender} · DOB ${dobDisplay}`;

        document.getElementById('jyMulank').textContent   = d.mulank;
        document.getElementById('jyBhagyank').textContent = d.bhagyank;
        document.getElementById('jyGift').textContent     = d.gift_number;
        document.getElementById('jyKua').textContent      = d.kua_number;
        document.getElementById('jyNamank').textContent   = d.namank;

        renderLoShuGrid(d.lo_shu_grid.grid);
        document.getElementById('jyMissingNums').textContent =
            d.lo_shu_grid.missing.length ? d.lo_shu_grid.missing.join(', ') : 'None';

        const dc = d.driver_conductor_profile;
        if (dc) {
            document.getElementById('jyDcLabel').textContent      = `${d.mulank}~${d.bhagyank}`;
            document.getElementById('jyCompatBadge').textContent  = `${dc.compatibility}% compatible`;
            document.getElementById('jyDcMode').textContent       = dc.mode;
            document.getElementById('jyDcIndustries').textContent = dc.industries.join(' · ');
            document.getElementById('jyDcPros').innerHTML = dc.pros.map(p => `<li>${p}</li>`).join('');
            document.getElementById('jyDcCons').innerHTML = dc.cons.map(c => `<li>${c}</li>`).join('');
        }

        const row = document.getElementById('jyRemediesRow');
        row.innerHTML = '';
        (d.missing_remedies || []).forEach(r => {
            const card = document.createElement('div');
            card.className = 'jy-remedy-card';
            card.innerHTML = `
                <div class="remedy-num">#${r.number}</div>
                <div class="remedy-planet">${r.planet} · ${r.color}</div>
                <div class="remedy-element">${r.element}</div>
                <ul class="remedy-list">${r.remedies.map(x => `<li>${x}</li>`).join('')}</ul>
            `;
            row.appendChild(card);
        });
        document.getElementById('jyRemediesSection').style.display =
            d.missing_remedies && d.missing_remedies.length ? '' : 'none';

        panel.classList.remove('hidden');
    } catch (e) {
        console.error('Numerology error:', e);
    } finally {
        if (loadingEl) loadingEl.classList.add('hidden');
    }
}

const LO_SHU_LAYOUT = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
];

function renderLoShuGrid(grid) {
    const tbody = document.querySelector('#jyLoShuTable tbody');
    tbody.innerHTML = '';
    grid.forEach((row, ri) => {
        const tr = document.createElement('tr');
        row.forEach((cell, ci) => {
            const td = document.createElement('td');
            const num = LO_SHU_LAYOUT[ri][ci];
            td.dataset.num = num;
            td.className = cell.count > 0 ? 'present' : 'absent';
            td.innerHTML = `<span class="cell-num">${num}</span><span class="cell-count">${cell.count > 0 ? '×'.repeat(cell.count) : ''}</span>`;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// ── Feedback Functions ───────────────────────────────────────

let currentRating = 0;

function toggleFeedback() {
    const panel = document.querySelector('.feedback-panel');
    panel.classList.toggle('hidden');
    
    // Reset form when opening
    if (!panel.classList.contains('hidden')) {
        resetFeedbackForm();
    }
}

function resetFeedbackForm() {
    currentRating = 0;
    document.querySelectorAll('.star').forEach(star => {
        star.classList.remove('active');
    });
    document.getElementById('feedbackText').value = '';
    document.getElementById('featureUsed').value = '';
    document.getElementById('feedbackStatus').classList.add('hidden');
}

// Initialize feedback functionality when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    // Star rating functionality
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('click', () => {
            const rating = parseInt(star.dataset.rating);
            currentRating = rating;
            
            // Update visual state
            document.querySelectorAll('.star').forEach(s => {
                s.classList.toggle('active', parseInt(s.dataset.rating) <= rating);
            });
        });
    });
});

async function submitFeedback() {
    const feedbackText = document.getElementById('feedbackText').value.trim();
    const featureUsed = document.getElementById('featureUsed').value;

    if (!currentRating) {
        alert('Please select a rating');
        return;
    }

    if (!feedbackText) {
        alert('Please provide feedback text');
        return;
    }

    try {
        const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                rating: currentRating,
                feedback_text: feedbackText,
                feature_used: featureUsed,
                session_id: 'web'
            })
        });
        const result = await res.json();
        const statusDiv = document.getElementById('feedbackStatus');
        if (res.ok) {
            statusDiv.textContent = '✅ Thank you! Your feedback has been submitted.';
            statusDiv.className = 'feedback-status success';
            statusDiv.classList.remove('hidden');
            setTimeout(() => { toggleFeedback(); }, 2000);
        } else {
            statusDiv.textContent = '❌ Failed to submit: ' + (result.message || 'Unknown error');
            statusDiv.className = 'feedback-status error';
            statusDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Feedback submission error:', error);
        const statusDiv = document.getElementById('feedbackStatus');
        statusDiv.textContent = '❌ Failed to submit feedback. Please try again.';
        statusDiv.className = 'feedback-status error';
        statusDiv.classList.remove('hidden');
    }
}

// ── #11 Yearly Forecast ───────────────────────────────────────────────────────

let currentForecastYear = new Date().getFullYear();

async function loadForecast(yearOffset) {
    if (yearOffset !== undefined) currentForecastYear += yearOffset;
    const birthDate = document.getElementById('date')?.value;
    if (!birthDate) return;

    const section   = document.getElementById('forecastSection');
    const yearLabel = document.getElementById('forecastYearLabel');
    const yearCard  = document.getElementById('forecastYearCard');
    const grid      = document.getElementById('forecastGrid');
    const highlights = document.getElementById('forecastHighlights');
    if (!section || !yearCard || !grid) return;

    if (yearLabel) yearLabel.textContent = currentForecastYear;

    try {
        const res = await fetch(`/api/numerology/forecast?birth_date=${birthDate}&year=${currentForecastYear}`);
        if (!res.ok) return;
        const d = await res.json();
        const py = d.personal_year;

        yearCard.innerHTML = `
            <div class="card" style="background:linear-gradient(135deg,rgba(99,91,255,0.08),rgba(99,91,255,0.03));border-color:rgba(99,91,255,0.2)">
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px">
                    <div style="font-size:56px;font-weight:800;color:var(--accent);line-height:1">${py.number}</div>
                    <div>
                        <div style="font-size:20px;font-weight:700;color:var(--text);letter-spacing:-0.02em">${py.theme}</div>
                        <div style="font-size:13px;color:var(--muted);margin-top:2px">${py.energy} · ${py.planet} · ${py.color}</div>
                    </div>
                </div>
                <div style="font-size:14px;color:var(--text);line-height:1.65">${py.focus}</div>
            </div>`;

        grid.innerHTML = (d.months || []).map(m => {
            const hl = d.highlights || {};
            const isAction = (hl.action_months || []).includes(m.month_name);
            const isRest   = (hl.rest_months   || []).includes(m.month_name);
            const tag = isAction
                ? '<span style="font-size:10px;font-weight:700;background:rgba(34,197,94,0.12);color:#16a34a;border-radius:20px;padding:2px 8px">Action</span>'
                : isRest
                    ? '<span style="font-size:10px;font-weight:700;background:rgba(245,158,11,0.10);color:#d97706;border-radius:20px;padding:2px 8px">Rest</span>'
                    : '';
            const borderHighlight = isAction ? ';border-color:rgba(34,197,94,0.35)' : isRest ? ';border-color:rgba(245,158,11,0.25)' : '';
            return `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px 12px;box-shadow:var(--shadow)${borderHighlight}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--muted)">${m.month_name}</div>
                    ${tag}
                </div>
                <div style="font-size:32px;font-weight:800;color:var(--accent);line-height:1;margin-bottom:6px">${m.personal_month}</div>
                <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:3px">${m.theme}</div>
                <div style="font-size:11px;color:var(--muted)">${m.energy} · ${m.planet}</div>
            </div>`;
        }).join('');

        const hl = d.highlights || {};
        if (hl.action_months?.length || hl.rest_months?.length) {
            highlights.innerHTML = `<div style="display:flex;gap:20px;flex-wrap:wrap;padding-top:4px">
                ${hl.action_months?.length ? `<div style="font-size:13px;color:#16a34a"><strong style="font-weight:700">Action months:</strong> ${hl.action_months.join(', ')}</div>` : ''}
                ${hl.rest_months?.length   ? `<div style="font-size:13px;color:#d97706"><strong style="font-weight:700">Rest months:</strong>   ${hl.rest_months.join(', ')}</div>`   : ''}
            </div>`;
        }

        section.classList.remove('hidden');
    } catch (e) {
        console.error('Forecast error:', e);
    }
}

// ── #8 Personal Cycles ────────────────────────────────────────────────────────

async function loadPersonalCycles(birthDate) {
    if (!birthDate) return;
    try {
        const res = await fetch(`/api/numerology/cycles?birth_date=${birthDate}`);
        if (!res.ok) return;
        const d = await res.json();

        const section = document.getElementById('cyclesSection');
        const row = document.getElementById('cyclesRow');
        if (!section || !row) return;

        const cycles = [
            { label: 'Personal Year', data: d.personal_year },
            { label: 'Personal Month', data: d.personal_month },
            { label: 'Personal Day', data: d.personal_day },
        ];

        row.innerHTML = cycles.map(c => `
            <div class="cycle-card">
                <div class="cycle-label">${c.label}</div>
                <div class="cycle-number">${c.data.number}</div>
                <div class="cycle-theme">${c.data.theme}</div>
                <div class="cycle-energy">${c.data.energy} · ${c.data.planet}</div>
                <div class="cycle-focus">${c.data.focus}</div>
            </div>`).join('');

        section.classList.remove('hidden');
    } catch (e) {
        console.error('Cycles error:', e);
    }
}

// ── #10 Two-Person Compatibility ──────────────────────────────────────────────

let _compatProfiles = [];

async function populateCompatibilityDropdowns() {
    if (_compatProfiles.length) return; // already loaded
    try {
        const res = await fetch('/api/numerology/profiles');
        if (!res.ok) return;
        _compatProfiles = await res.json();
        const selA = document.getElementById('compatPersonA');
        const selB = document.getElementById('compatPersonB');
        if (!selA || !selB) return;
        const opts = _compatProfiles.map(p =>
            `<option value="${p.label}">${p.name}</option>`).join('');
        selA.innerHTML = opts;
        selB.innerHTML = opts;
        if (_compatProfiles.length > 1) selB.selectedIndex = 1;
    } catch (e) { console.error('Compat dropdown error:', e); }
}

async function loadCompatibility() {
    const labelA = document.getElementById('compatPersonA')?.value;
    const labelB = document.getElementById('compatPersonB')?.value;
    const resultEl = document.getElementById('compatResult');
    if (!labelA || !labelB || !resultEl) return;
    if (labelA === labelB) {
        resultEl.innerHTML = '<div style="color:var(--muted);font-size:13px;padding:12px">Select two different people.</div>';
        resultEl.classList.remove('hidden');
        return;
    }

    resultEl.innerHTML = '<div style="color:var(--muted);font-size:13px;padding:12px">Comparing…</div>';
    resultEl.classList.remove('hidden');

    try {
        const res = await fetch(`/api/numerology/compatibility?label_a=${labelA}&label_b=${labelB}`);
        if (!res.ok) throw new Error('Failed');
        const d = await res.json();
        const c = d.compatibility;

        const scoreColor = c.score >= 80 ? '#22c55e' : c.score >= 65 ? '#635bff' : c.score >= 50 ? '#f59e0b' : '#ef4444';
        const aName = d.person_a.name || labelA;
        const bName = d.person_b.name || labelB;

        resultEl.innerHTML = `
            <div class="compat-result-card">
                <div class="compat-score-row">
                    <div class="compat-score-num" style="color:${scoreColor}">${c.score}</div>
                    <div>
                        <div class="compat-verdict">${c.verdict}</div>
                        <div class="compat-names">${aName} × ${bName}</div>
                    </div>
                </div>
                <div class="compat-summary">${c.summary}</div>
                <div class="compat-duo-row">
                    <div class="compat-person-block">
                        <div class="compat-person-name">${aName}</div>
                        <div class="compat-person-nums">Driver ${c.person_a.mulank} (${c.person_a.driver_planet}) · Conductor ${c.person_a.bhagyank} (${c.person_a.conductor_planet})</div>
                    </div>
                    <div class="compat-person-block">
                        <div class="compat-person-name">${bName}</div>
                        <div class="compat-person-nums">Driver ${c.person_b.mulank} (${c.person_b.driver_planet}) · Conductor ${c.person_b.bhagyank} (${c.person_b.conductor_planet})</div>
                    </div>
                </div>
                <div class="compat-dynamics">
                    <div class="compat-dyn-block">
                        <div class="compat-dyn-label">${aName} leads</div>
                        <div class="compat-dyn-score">${c.dynamics.a_leads_b.score}%</div>
                        <ul class="compat-dyn-list">${(c.dynamics.a_leads_b.pros || []).map(p => `<li>${p}</li>`).join('')}</ul>
                    </div>
                    <div class="compat-dyn-block">
                        <div class="compat-dyn-label">${bName} leads</div>
                        <div class="compat-dyn-score">${c.dynamics.b_leads_a.score}%</div>
                        <ul class="compat-dyn-list">${(c.dynamics.b_leads_a.pros || []).map(p => `<li>${p}</li>`).join('')}</ul>
                    </div>
                </div>
            </div>`;
    } catch (e) {
        resultEl.innerHTML = '<div style="color:#ef4444;font-size:13px;padding:12px">Failed to load compatibility.</div>';
    }
}
