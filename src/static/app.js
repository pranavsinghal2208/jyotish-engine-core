let currentChartData = null;

// ── Auth ──────────────────────────────────────────────────
async function checkAuthStatus() {
    try {
        const res = await fetch("/api/auth/status");
        const { authenticated, email } = await res.json();

        // Results header
        const authLinks = document.getElementById("authLinks");
        const logoutBtn = document.getElementById("headerLogoutBtn");
        const authBadge = document.getElementById("headerAuthBadge");
        
        if (authLinks) authLinks.classList.toggle("hidden", authenticated);
        if (logoutBtn) logoutBtn.classList.toggle("hidden", !authenticated);
        if (authBadge) authBadge.classList.toggle("hidden", !authenticated);

        // Update name chip if authenticated but no name set
        if (authenticated && email && !localStorage.getItem("cosmicOsName")) {
            const nameChip = document.getElementById("headerName");
            if (nameChip) nameChip.textContent = (email && email !== "default@psbc.com") ? email.split("@")[0] : "Traveler";
        }
    } catch (e) {
        console.error('Auth check failed', e);
    }
}

// ── Tab navigation ────────────────────────────────────────
function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const view = btn.dataset.view;
            document.getElementById('strategicView').classList.toggle('hidden', view !== 'strategic');
            document.getElementById('technicalView').classList.toggle('hidden', view !== 'technical');
            document.getElementById('numerologyView').classList.toggle('hidden', view !== 'numerology');

            if (view === 'technical' && currentChartData) populateTechnicalView();
            if (view === 'numerology') loadMyNumerology();
        });
    });
}

// ── City search ───────────────────────────────────────────
function initHeroSearch() {
    const citySearch  = document.getElementById('citySearch');
    const cityResults = document.getElementById('cityResults');
    const momentRow   = document.getElementById('momentStep');
    const ctaBtn      = document.getElementById('generateBtn');
    let debounce;

    citySearch.addEventListener('input', () => {
        clearTimeout(debounce);
        const q = citySearch.value.trim();
        if (q.length < 2) { cityResults.classList.add('hidden'); return; }

        debounce = setTimeout(async () => {
            try {
                const res  = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}&addressdetails=1&limit=5`);
                const data = await res.json();
                cityResults.innerHTML = '';
                data.forEach(city => {
                    const label = city.display_name.split(',').slice(0, 2).join(', ');
                    const div   = document.createElement('div');
                    div.className = 'city-item';
                    div.textContent = label;
                    div.onclick = () => {
                        document.getElementById('lat').value    = city.lat;
                        document.getElementById('lon').value    = city.lon;
                        citySearch.value = label;
                        cityResults.classList.add('hidden');
                        momentRow.classList.remove('hidden');
                        ctaBtn.classList.remove('hidden');
                    };
                    cityResults.appendChild(div);
                });
                cityResults.classList.remove('hidden');
            } catch (e) { console.error(e); }
        }, 380);
    });

    document.addEventListener('click', e => {
        if (!cityResults.contains(e.target) && e.target !== citySearch) {
            cityResults.classList.add('hidden');
        }
    });
}

// ── Profile recovery ──────────────────────────────────────
async function checkUserProfile() {
    try {
        const res = await fetch("/api/user/profile");
        const d = await res.json();
        
        if (d.status === "success") {
            // Existing user: Pre-fill and load chart
            document.getElementById("fullName").value = localStorage.getItem("cosmicOsName") || "";
            document.getElementById("date").value = d.date;
            quickUnlock();
            document.getElementById("time").value = d.time;
            document.getElementById("lat").value = d.lat;
            document.getElementById("lon").value = d.lon;
            document.getElementById("offset").value = d.offset;
            document.getElementById("citySearch").value = d.location_name;
            
            // Auto-trigger chart for returning user
            generateChart();
        } else if (d.new_user) {
            // New User flow: Show welcome message
            showWelcomeToast(d.email);
            // Pre-fill name from email if possible
            if (d.email && !document.getElementById("fullName").value) {
                document.getElementById("fullName").value = d.email.split("@")[0].charAt(0).toUpperCase() + d.email.split("@")[0].slice(1);
            }
        }
    } catch (e) {
        console.log("Profile check failed", e);
    }
}

function showWelcomeToast(email) {
    const toast = document.createElement("div");
    toast.className = "welcome-toast";
    toast.innerHTML = `
        <div class="welcome-header">Welcome, ${email === "default@psbc.com" ? "Traveler" : email.split("@")[0]}</div>
        <div class="welcome-body">To calibrate your personal intelligence dashboard, we need your birth coordinates once.</div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("reveal"), 500);
}

// ── Generate chart ────────────────────────────────────────
async function generateChart() {
    const btn  = document.getElementById('generateBtn');
    const name = document.getElementById('fullName')?.value.trim();
    if (name) localStorage.setItem('cosmicOsName', name);

    btn.textContent = 'Computing…';
    btn.disabled    = true;

    const payload = {
        date:             document.getElementById('date').value,
        time:             document.getElementById('time').value,
        lat:              parseFloat(document.getElementById('lat').value),
        lon:              parseFloat(document.getElementById('lon').value),
        timezone_offset:  parseFloat(document.getElementById('offset').value)
    };

    try {
        const res  = await fetch('/api/chart', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!res.ok) throw new Error('Analysis failed.');
        const data = await res.json();
        currentChartData = data;

        document.getElementById('landingScreen').classList.add('hidden');
        document.getElementById('resultsScreen').classList.remove('hidden');
        document.getElementById('feedbackWidget').classList.remove('hidden');
        checkAuthStatus();
        populateStrategicView(data);
    } catch (e) {
        alert(e.message);
    } finally {
        btn.textContent = 'Generate Chart';
        btn.disabled    = false;
    }
}

// ── Strategic view ────────────────────────────────────────
function populateStrategicView(data) {

    // Clear initial placeholders before populating
    ["dailyTheme", "energySignature", "activeDasha"].forEach(id => {
        const el = document.getElementById(id);
        if (el && el.textContent === "—") el.textContent = "Processing...";
    });

    const { insights, business_pulse, cosmic_schedule, nakshatra } = data;

    // Header name chip
    const savedName = localStorage.getItem('cosmicOsName');
    const nameChip  = document.getElementById('headerName');
    if (savedName && nameChip) nameChip.textContent = savedName;

    document.getElementById('dailyTheme').textContent      = insights.daily_theme;
    document.getElementById('energySignature').textContent  = insights.energy_signature;
    document.getElementById('upliftNarrative').textContent  = insights.uplift_narrative || '';

    // Nakshatra strip
    if (nakshatra) {
        document.getElementById('nakshatraName').textContent = nakshatra.name;
        document.getElementById('nakshatraMeta').textContent = `Lord: ${nakshatra.lord} · Pada ${nakshatra.pada}`;
        document.getElementById('nakshatraStrip').classList.remove('hidden');
    }

    // Panchanga (birth Tithi + Yoga from natal Sun/Moon)
    if (data.planets?.Sun && data.planets?.Moon) {
        const sunLon  = data.planets.Sun.longitude;
        const moonLon = data.planets.Moon.longitude;
        const tithiIdx = Math.floor(((moonLon - sunLon + 360) % 360) / 12);
        const yogaIdx  = Math.floor(((sunLon + moonLon) % 360) / (360 / 27));
        const paksha   = tithiIdx < 15 ? 'Shukla' : 'Krishna';
        document.getElementById('tithiName').textContent = `${TITHI_NAMES[tithiIdx]} · ${paksha} Paksha`;
        document.getElementById('yogaName').textContent  = YOGA_NAMES[yogaIdx % 27];
        document.getElementById('panchangaStrip').classList.remove('hidden');
    }

    // Superpowers
    const spList = document.getElementById('superpowerList');
    spList.innerHTML = '<div class="card-label">Your natal blueprint</div>';
    insights.superpowers.forEach(p => {
        const div = document.createElement('div');
        div.className = 'power-item';
        div.innerHTML = `<div class="power-title">${p.title}</div><div class="power-desc">${p.description}</div>`;
        spList.appendChild(div);
    });

    document.getElementById('operationalPointer').textContent = insights.operational_pointer;

    // Today's actions
    const actionsWrap = document.getElementById('dailyActionsWrap');
    const actionsList = document.getElementById('dailyActionsList');
    if (insights.daily_actions && insights.daily_actions.length > 0) {
        actionsList.innerHTML = '';
        insights.daily_actions.forEach(a => {
            const li = document.createElement('li');
            li.textContent = a;
            actionsList.appendChild(li);
        });
        actionsWrap.classList.remove('hidden');
    }

    // Dasha pulse
    document.getElementById('activeDasha').textContent   = business_pulse.display_dasha || business_pulse.active_dasha;
    document.getElementById('pulseFocus').textContent    = business_pulse.focus;
    document.getElementById('pulseStrategy').textContent  = business_pulse.strategy;
    document.getElementById('targetKpi').textContent     = business_pulse.target_kpi;

    // Calendar alerts
    const section  = document.getElementById('cosmicScheduleSection');
    const alertList = document.getElementById('alertList');
    alertList.innerHTML = '';
    if (cosmic_schedule && cosmic_schedule.length > 0) {
        section.classList.remove('hidden');
        cosmic_schedule.forEach(a => {
            const riskClass = a.risk === 'High' ? 'risk-high' : a.risk === 'Low' ? 'risk-low' : 'risk-mod';
            const div = document.createElement('div');
            div.className = 'alert-card';
            div.innerHTML = `
                <div class="alert-event">${a.event} <span class="${riskClass}" style="font-size:11px;font-weight:700;">${a.risk} risk</span></div>
                <div class="alert-reason">${a.reason}</div>
                <div class="alert-action">→ ${a.action}</div>
            `;
            alertList.appendChild(div);
        });
    } else {
        section.classList.add('hidden');
    }

    // Morning Brief + Timing Advisor (fetched async after chart load)
    loadMorningBrief();
    loadTimingAdvisor();
}

async function loadMorningBrief() {
    const briefSection = document.getElementById('morningBriefSection');
    const briefCard    = document.getElementById('morningBriefCard');
    if (!briefSection || !briefCard) return;

    briefCard.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <div class="skeleton" style="height:14px;width:130px"></div>
            <div class="skeleton" style="height:22px;width:90px;border-radius:20px"></div>
        </div>
        <div class="skeleton" style="height:36px;width:100%;margin-bottom:16px"></div>
        <div style="display:flex;gap:12px">
            <div class="skeleton" style="height:76px;flex:1;border-radius:8px"></div>
            <div class="skeleton" style="height:76px;flex:1;border-radius:8px"></div>
            <div class="skeleton" style="height:76px;flex:1;border-radius:8px"></div>
        </div>`;
    briefSection.classList.remove('hidden');

    try {
        const res = await fetch('/api/brief/morning');
        if (!res.ok) return;
        const d = await res.json();
        const pd = d.personal_day;
        const highlightHtml = (d.transit_highlights || [])
            .map(h => `<div class="brief-highlight">${h}</div>`).join('');
        briefCard.innerHTML = `
            <div class="brief-top-row">
                <div class="brief-date">${d.day_name}, ${d.date}</div>
                <div class="brief-window-badge">${d.overall_window}</div>
            </div>
            <div class="brief-desc">${d.overall_description}</div>
            <div class="brief-cycles-row">
                <div class="brief-cycle">
                    <div class="brief-cycle-label">Personal Day</div>
                    <div class="brief-cycle-num">${pd.number}</div>
                    <div class="brief-cycle-theme">${pd.theme}</div>
                </div>
                <div class="brief-cycle">
                    <div class="brief-cycle-label">Nakshatra</div>
                    <div class="brief-cycle-num" style="font-size:18px">${d.nakshatra}</div>
                    <div class="brief-cycle-theme">${d.active_dasha}</div>
                </div>
                <div class="brief-cycle">
                    <div class="brief-cycle-label">Best Day This Week</div>
                    <div class="brief-cycle-num" style="font-size:18px">${d.best_day_this_week?.day || '—'}</div>
                    <div class="brief-cycle-theme">${d.best_day_this_week?.date || ''}</div>
                </div>
            </div>
            ${highlightHtml ? `<div class="brief-highlights">${highlightHtml}</div>` : ''}
            ${d.top_action?.label ? `<div class="brief-action">Top action today: <strong>${d.top_action.label}</strong> — ${d.top_action.window}</div>` : ''}`;
        briefSection.classList.remove('hidden');
    } catch (e) {
        console.error('Morning brief error:', e);
    }
}

async function loadTimingAdvisor() {
    const section  = document.getElementById('timingAdvisorSection');
    const overview = document.getElementById('timingOverviewCard');
    const grid     = document.getElementById('timingActionsGrid');
    if (!section || !overview || !grid) return;

    overview.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <div>
                <div class="skeleton" style="height:22px;width:110px;border-radius:20px;margin-bottom:8px"></div>
                <div class="skeleton" style="height:14px;width:220px"></div>
            </div>
            <div style="text-align:right">
                <div class="skeleton" style="height:12px;width:90px;margin-bottom:6px"></div>
                <div class="skeleton" style="height:20px;width:60px"></div>
            </div>
        </div>`;
    grid.innerHTML = Array(6).fill(`
        <div class="skeleton" style="height:110px;border-radius:10px"></div>`).join('');
    section.classList.remove('hidden');

    try {
        const res = await fetch('/api/timing/advisor');
        if (!res.ok) return;
        const d = await res.json();
        overview.innerHTML = `
            <div class="timing-overview-row">
                <div>
                    <div class="timing-window-badge timing-${d.overall_window.toLowerCase().replace(' ','-')}">${d.overall_window}</div>
                    <div class="timing-desc">${d.overall_description}</div>
                </div>
                <div class="timing-best-day">
                    <div class="timing-best-label">Best day this week</div>
                    <div class="timing-best-value">${d.best_day_this_week?.day}</div>
                    <div class="timing-best-date">${d.best_day_this_week?.date}</div>
                </div>
            </div>
            <div class="timing-dasha-note">${d.dasha_lord} Maha-Dasha · ${d.nakshatra} Nakshatra</div>`;

        grid.innerHTML = (d.actions || []).map(a => {
            const wClass = a.window.toLowerCase().replace(' ', '-');
            return `<div class="timing-action-card timing-action-${wClass}">
                <div class="timing-action-top">
                    <span class="timing-action-icon">${a.icon}</span>
                    <span class="timing-action-label">${a.label}</span>
                    <span class="timing-action-score">${a.score}</span>
                </div>
                <div class="timing-action-window">${a.window}</div>
                <div class="timing-action-advice">${a.advice}</div>
                <div class="timing-dasha-note" style="margin-top:6px">${a.dasha_note}</div>
            </div>`;
        }).join('');
        section.classList.remove('hidden');
    } catch (e) {
        console.error('Timing advisor error:', e);
    }
}

// ── Technical view ────────────────────────────────────────
const SIGN_INTERPRETATIONS = {
    "Aries":       "Strategic Disruptor. Built for first-mover advantage and high-impact initiative.",
    "Taurus":      "Institutional Builder. Built for resource optimization and compounding stability.",
    "Gemini":      "Network Architect. Built for information arbitrage and tactical outreach.",
    "Cancer":      "Intuitive Leader. Built for tactical empathy and high-speed risk detection.",
    "Leo":         "Authority Figure. Built for executive presence and defining the market narrative.",
    "Virgo":       "Operational Specialist. Built for system precision and zero-defect auditing.",
    "Libra":       "Deal Architect. Built for strategic diplomacy and structured win-win scenarios.",
    "Scorpio":     "Crisis Navigator. Built for truth extraction and high-stakes transformation.",
    "Sagittarius": "Scale Visionary. Built for expansive strategy and macro-trend alignment.",
    "Capricorn":   "Domain Master. Built for institutional endurance and structural integrity.",
    "Aquarius":    "Future-Thinker. Built for systemic innovation and disruptive network leverage.",
    "Pisces":      "Pattern Synthesizer. Built for creative synthesis and intuitive pattern recognition."
};

const PLANET_ROLES = {
    "Sun":     { role: "Core Identity",            biz: "Identity, authority & leadership recognition" },
    "Moon":    { role: "Mind & Emotions",           biz: "Mindset, environment & cultural alignment" },
    "Mars":    { role: "Will & Drive",              biz: "Speed, momentum & market capture" },
    "Mercury": { role: "Intelligence & Voice",      biz: "Systems, communication & information arbitrage" },
    "Jupiter": { role: "Wisdom & Growth",           biz: "Scaling, growth & macro-mentorship" },
    "Venus":   { role: "Love & Beauty",             biz: "Partnerships, quality & asset appreciation" },
    "Saturn":  { role: "Discipline & Karma",        biz: "Discipline, legacy & institutional building" },
    "Rahu":    { role: "Ambition & Obsession",      biz: "Disruption, ambition & rapid market entry" },
    "Ketu":    { role: "Detachment & Mastery",      biz: "Refinement, depth & proprietary technology" }
};

const PLANET_IN_SIGN = {
    "Sun": {
        "Aries":"Your identity is forged in action. You lead by doing, not by committee.", "Taurus":"Your identity is rooted in stability and the long game. You build empires slowly.", "Gemini":"Your identity is intellectual — you define yourself through ideas and dialogue.", "Cancer":"Your identity is emotional and protective. You lead through care and intuition.", "Leo":"You were born to shine. Leadership is your natural state — the room rearranges around you.", "Virgo":"Your identity is in the detail. You define excellence through precision and refinement.", "Libra":"Your identity is relational. You find yourself through others and fair exchange.", "Scorpio":"Your identity is forged in transformation. You are never the same person twice.", "Sagittarius":"Your identity is expansive. You define yourself through growth, truth and exploration.", "Capricorn":"Your identity is institutional. You are building something that outlasts you.", "Aquarius":"Your identity is original. You define yourself by how far ahead of the curve you stand.", "Pisces":"Your identity is fluid and empathic. You absorb the world and reflect its depth back."
    },
    "Moon": {
        "Aries":"Your instinct is to act first and feel later. Emotional courage is your default mode.", "Taurus":"Your inner world craves security and beauty. You are most yourself in calm, abundant environments.", "Gemini":"Your mind never stops. Curiosity and connection are your emotional fuel.", "Cancer":"Your emotional depth is your greatest strength. You feel everything — protect that gift.", "Leo":"Your heart is generous and warm. You need appreciation to feel truly at home in the world.", "Virgo":"You process emotion through analysis. Order and care are how you express love.", "Libra":"You seek harmony in all things. Conflict disturbs you because your nature is to balance.", "Scorpio":"Your emotional world is intense and private. Loyalty is everything; betrayal is unforgettable.", "Sagittarius":"Your heart is optimistic and free. You need space, adventure and meaning to feel alive.", "Capricorn":"You hold your feelings close. Emotional strength looks like quiet composure to others.", "Aquarius":"Your heart belongs to humanity. You feel most alive in community and shared purpose.", "Pisces":"Your emotions are vast and deep. You sense what others cannot — honour that perception."
    },
    "Mars": {
        "Aries":"Pure fire. You were built to initiate and compete. No one outworks you at a sprint.", "Taurus":"Your drive is slow, deliberate and unstoppable. You finish what others abandoned.", "Gemini":"Your energy is mental — you win through strategy and speed of thought.", "Cancer":"Your drive is fiercely protective. You fight hardest for those you love.", "Leo":"Bold, dramatic action. You fight for recognition and refuse to be overlooked.", "Virgo":"Your effort is precise and methodical. You improve systems until they're flawless.", "Libra":"You fight for fairness. Conflict is uncomfortable but you will hold your ground for justice.", "Scorpio":"Relentless and strategic. You never reveal your full hand, but you always win the long game.", "Sagittarius":"Your drive is philosophical. You fight for ideas, expansion and freedom.", "Capricorn":"You have the patience of stone and the ambition of mountains. Nothing stops your climb.", "Aquarius":"Your energy is unconventional. You solve problems no one else sees as solvable.", "Pisces":"Your drive is spiritual. You work best when your effort connects to something larger than yourself."
    },
    "Mercury": {
        "Aries":"Sharp, quick, direct. You cut through noise instantly and prefer action to analysis.", "Taurus":"Methodical and thorough. Your thinking is slow to start but rock-solid once formed.", "Gemini":"Brilliant and multi-threaded. Your mind holds ten conversations at once.", "Cancer":"Intuitive logic. You read subtext and unspoken meaning as clearly as words.", "Leo":"Persuasive and dramatic. You communicate with authority and inspire through storytelling.", "Virgo":"Analytical and precise. You find the flaw in any argument and the solution in any problem.", "Libra":"Balanced and diplomatic. You weigh every side before speaking — and then speak beautifully.", "Scorpio":"Penetrating and strategic. You say less than you know and ask more than you reveal.", "Sagittarius":"Expansive and visionary. You communicate in big ideas and long horizons.", "Capricorn":"Precise and authoritative. You speak with weight and your words carry institutional credibility.", "Aquarius":"Original and ahead of the curve. You think in systems and futures most haven't imagined.", "Pisces":"Imaginative and empathic. Your words carry emotional resonance that logic alone cannot."
    },
    "Jupiter": {
        "Aries":"Growth through bold action. Fortune favours your willingness to go first.", "Taurus":"Growth through patience and resource building. Wealth accumulates steadily and permanently.", "Gemini":"Growth through learning and networks. Every conversation is a potential expansion.", "Cancer":"Growth through emotional wisdom and nurturing. Your intuition is a compass to abundance.", "Leo":"Growth through self-expression and generosity. The more you give, the more returns.", "Virgo":"Growth through mastery and service. Excellence in your craft opens every door.", "Libra":"Growth through partnerships and fairness. The right alliance multiplies everything.", "Scorpio":"Growth through depth and transformation. You access resources others cannot see.", "Sagittarius":"Jupiter at home — natural wisdom, abundance and the vision to match. Expansion is your birthright.", "Capricorn":"Growth through discipline and integrity. Every investment of effort compounds over decades.", "Aquarius":"Growth through community and innovation. Your network is your most valuable asset.", "Pisces":"Growth through faith and creativity. You are guided by something larger than strategy."
    },
    "Venus": {
        "Aries":"You love with urgency and passion. Quick to desire, quick to pursue — but also quick to move on.", "Taurus":"Venus at home — deep sensuality, loyalty and a love of beauty that borders on devotion.", "Gemini":"You love through words and wit. Intellectual connection is the deepest form of intimacy for you.", "Cancer":"You love by nurturing. Your home is your sanctuary and your relationships are your world.", "Leo":"Generous, dramatic and devoted — when you love, you love loudly and without apology.", "Virgo":"You love through acts of service. Your devotion is quiet, precise and deeply practical.", "Libra":"Venus at home — you were made for partnership. Beauty, harmony and love are your native language.", "Scorpio":"You love with total intensity. Depth, loyalty and transformation are your relationship standard.", "Sagittarius":"You love with freedom. Adventure, honesty and growth keep any relationship alive for you.", "Capricorn":"You love with commitment. Relationships must have structure and a future to hold your full heart.", "Aquarius":"You love with originality. Conventional romance bores you — you need a partner who's also your peer.", "Pisces":"You love with boundless compassion. Your heart has no walls — protect it with equal wisdom."
    },
    "Saturn": {
        "Aries":"Saturn challenges your impulsiveness. Patience is the karmic lesson — and the greatest reward.", "Taurus":"Steady discipline around resources. Saturn teaches you that real wealth is built, not found.", "Gemini":"Saturn disciplines your scattered mind. Focus is the gift that comes from this pressure.", "Cancer":"Saturn asks you to build emotional boundaries. Your security must come from within.", "Leo":"Saturn tempers your ego. True authority is earned through humility and consistent effort.", "Virgo":"Saturn sharpens your precision. Mastery through relentless refinement is your path.", "Libra":"Saturn is exalted here — justice, balance and right relationship are the pillars of your karma.", "Scorpio":"Saturn in Scorpio demands you face what others refuse to look at. This is the source of your depth.", "Sagittarius":"Saturn disciplines your optimism. Structure applied to vision creates wisdom.", "Capricorn":"Saturn at home — institutional builder. Discipline, patience and mastery are your nature.", "Aquarius":"Saturn brings order to your innovation. Systematic change outlasts revolution.", "Pisces":"Saturn asks for grounded spirituality. Your gifts are real — structure helps you deploy them."
    },
    "Rahu": {
        "Aries":"Your hunger is for independence and new territory. This life, you must learn to lead.", "Taurus":"Your hunger is for security and beauty. This life, you must learn to build and hold.", "Gemini":"Your hunger is for knowledge and connection. This life, you must learn to communicate.", "Cancer":"Your hunger is for belonging and emotional depth. This life, you must learn to nurture.", "Leo":"Your hunger is for recognition and creative expression. This life, you must learn to shine without fear.", "Virgo":"Your hunger is for mastery and precision. This life, you must learn to perfect your craft.", "Libra":"Your hunger is for partnership and harmony. This life, you must learn to meet others halfway.", "Scorpio":"Your hunger is for transformation and power. This life, you must learn to surrender control.", "Sagittarius":"Your hunger is for truth and expansion. This life, you must learn to think and live bigger.", "Capricorn":"Your hunger is for achievement and status. This life, you must learn discipline as devotion.", "Aquarius":"Your hunger is for innovation and community. This life, you must learn to serve the collective.", "Pisces":"Your hunger is for transcendence and creativity. This life, you must learn to trust the unseen."
    },
    "Ketu": {
        "Aries":"You carry past-life warrior energy. The lesson now is to let others lead while you go deeper.", "Taurus":"You carry past-life material mastery. The lesson now is non-attachment to security.", "Gemini":"You carry past-life intellectual prowess. The lesson now is silence and inner knowing.", "Cancer":"You carry past-life emotional bonds. The lesson now is to find home within yourself.", "Leo":"You carry past-life royal authority. The lesson now is to lead without needing the spotlight.", "Virgo":"You carry past-life precision and service. The lesson now is to release perfectionism.", "Libra":"You carry past-life harmony and diplomacy. The lesson now is to stand alone with conviction.", "Scorpio":"You carry past-life depth and occult knowledge. The lesson now is to forgive and release.", "Sagittarius":"You carry past-life wisdom and philosophy. The lesson now is to live the truth, not just know it.", "Capricorn":"You carry past-life institutional mastery. The lesson now is to release ambition for its own sake.", "Aquarius":"You carry past-life collective service. The lesson now is to honour your individual path.", "Pisces":"You carry past-life spiritual depth. The lesson now is to ground your gifts in practical form."
    }
};


const DASHA_DETAIL = {
    "Sun": {
        narrative: "A period when your sense of self comes into full focus. Who you are, what you stand for, and how you want to be known in the world — these are no longer abstract questions. This is the chapter where you step into the light and own it.",
        expect: ["Clarity about your unique strategic advantage begins to emerge", "Recognition and visibility — your signal is finally cutting through the noise", "Challenges to your authority that force you to refine your leadership model"],
        act:    ["Claim your authority in high-stakes environments — don't ask for permission", "Make your strategic vision visible; audit your public signal for clarity", "Define success by your own KPIs, not industry averages"],
        remedies: ["Morning Intention (5 mins): Align your daily tasks with your 10-year vision", "Visual Authority: Ensure your digital and physical presence reflects your rank", "Weekly Audit: Review where you traded authority for comfort"]
    },
    "Moon": {
        narrative: "A deeply internal chapter. Your intuition is at its most reliable, and your emotional world becomes the terrain you must learn to navigate. What nourishes you — your home, your inner circle, your daily rhythms — matters more than it ever has.",
        expect: ["Heightened tactical intuition — you'll sense market shifts before they manifest", "Significant shifts in your environment or core team composition", "Logic-defying gut feels that prove to be the most profitable path"],
        act:    ["Audit your 'Mindset Bottlenecks' — where is your internal state slowing you down?", "Trust your intuition in high-stakes hiring or partnership decisions", "Nurture your 'Inner Circle' — loyalty is your primary currency in this phase"],
        remedies: ["Environment Audit: Remove one source of 'Sensory Friction' from your workspace", "Reflective Journaling: Document your gut feels vs. outcomes to calibrate your intuition", "Hydration Mastery: High cognitive load requires optimal brain hydration (3L/day)"]
    },
    "Mars": {
        narrative: "A period of raw energy and forward motion. The desire to act, to build, to fight for what you want is at its most intense. This chapter rewards those who move before they feel fully ready.",
        expect: ["High-intensity momentum on your primary objectives", "Decisive windows where 'Moving Fast' yields 10x the results of 'Moving Correctly'", "Friction with slower entities (team or partners) — use it to pressure-test your speed"],
        act:    ["Prioritise execution speed over total perfection — capture the territory first", "Take the bold, 'uncomfortable' action you've been delaying", "Channel competitive drive into market share, not internal politics"],
        remedies: ["High-Intensity Interval Training (HIIT): Channel Mars energy to avoid burnout", "Daily Kill List: Tackle your most difficult task at 8:00 AM sharp", "Fire Focus: Use red/orange highlights in your focus apps to signal 'Action Mode'"]
    },
    "Mercury": {
        narrative: "Your mind opens. This is a chapter of learning, connecting, and communicating — a time when words, ideas, and the people who carry them become your most important tools. The skill you build here stays with you for decades.",
        expect: ["Accelerated information processing — you'll learn 3x faster than usual", "Networking and outreach produce high-signal opportunities rapidly", "Systems and documentation become your primary leverage points"],
        act:    ["Build and document systems relentlessly — this is your 'Scale Foundation' phase", "Communicate your insights publicly to build 'Information Arbitrage' authority", "Acquire one high-value technical skill that removes a scaling bottleneck"],
        remedies: ["Speed Reading/Synthesis: Consume and distill 3x more high-signal content", "Logic Puzzles/Strategy Games: Keep your tactical mind sharp and agile", "Digital Declutter: Optimize your 'Information Architecture' for speed"]
    },
    "Jupiter": {
        narrative: "A chapter of genuine good fortune and growth. The world feels larger, more generous, more full of possibility. Teachers appear. Doors open. The invitation of this period is to say yes to a life that is bigger than the one you have been living.",
        expect: ["Macro-opportunities expand — you'll be presented with 'Too Big to Fail' deals", "Mentors and high-level advisors enter your circle unexpectedly", "Wisdom grows — you'll start playing the 'Infinite Game' instead of the quarter"],
        act:    ["Say 'Yes' to scale opportunities that challenge your current capacity", "Actively seek 'Level 10' mentors — learn the mechanics of the next tier", "Be strategically generous — Jupiter rewards value-circulation"],
        remedies: ["Philanthropy/Mentorship: Circulate 5% of your time/value to seed future growth", "Strategic Gratitude: Formally acknowledge those who opened doors for you", "Expansion Meditation: Spend 10 mins visualizing your organization at 10x scale"]
    },
    "Venus": {
        narrative: "A chapter devoted to beauty, love, and the things that make life worth living. Your relationships deepen, your creative instincts sharpen, and the quality of your daily experience matters as much as your achievements. This is a period of richness — inner and outer.",
        expect: ["Enriched partnership ecosystem and 'Aesthetic Alpha' in your brand", "Prosperity that follows high-quality, high-design output", "Key relationships — professional and personal — become your primary multipliers"],
        act:    ["Invest in 'High-Design' assets and high-value partnerships", "Audit your 'Brand Beauty' — does your output command a premium?", "Focus on 'Depth of Relationship' over 'Breadth of Network'"],
        remedies: ["Aesthetic Upgrade: Improve one piece of your daily tech/environment for 'Joy ROI'", "Relationship First: Have one 'No-Agenda' lunch with a high-value contact weekly", "Sensory Refinement: Use scent or high-quality audio to optimize your focus state"]
    },

    "Saturn": {
        narrative: "A chapter of serious, unhurried work. Saturn does not rush, and neither will your growth during this period. What you build here is solid. What you ignore will surface. This is the chapter where patience stops being a virtue and becomes the only real path.",
        expect: ["A demanding but high-integrity phase — you are building for the next 30 years", "Patience will be tested; shortcuts will be blocked by 'System Gravity'", "Structural weaknesses in your life or business will be exposed for fixing"],
        act:    ["Eliminate every source of 'Operational Debt' or inefficiency", "Show up with 'Obsessive Consistency' — Saturn rewards the last person standing", "Honour every commitment with 'Institutional Integrity'"],
        remedies: ["Routine Locking: Perform your core tasks at the exact same time every day", "Service/Legacy: Dedicate one block a week to the 'Invisible Work' that sustains the whole", "Grounding: Spend time in nature or with 'Old Wisdom' (books/elders) to gain perspective"]
    },

    "Rahu": {
        narrative: "A chapter of intense ambition and rapid change. Rahu pulls you toward unfamiliar territory — new places, new people, new versions of yourself. The hunger you feel is real and productive, but it needs direction. This period rewards those who chase something specific, not just everything at once.",
        expect: ["Rapid, high-variance change — 'Normal' strategies will fail", "Opportunities in 'Foreign' or 'Uncharted' territory (new tech, new markets)", "Obsessive focus that can produce massive breakthroughs or total burnout"],
        act:    ["Embrace the 'Wild Card' strategy — innovate where others are hesitating", "Enter new markets or niches that feel 'uncomfortable' but high-potential", "Avoid 'Moral Shortcuts' — Rahu rewards boldness, but punishes dishonesty"],
        remedies: ["Grounding Meditation: 10 mins of breathwork to stabilize Rahu's 'Restless Ambition'", "Tech Sabbatical: 4 hours of 'No-Screen' time weekly to reset your nervous system", "Unconventional Input: Read one book/article entirely outside your field weekly"]
    },
    "Ketu": {
        narrative: "A chapter of letting go and going deep. The outer world holds less pull than usual, and that is not a problem — it is an invitation. This period rewards those who turn inward, master what they already carry, and release what no longer serves the person they are becoming.",
        expect: ["Inner mastery and 'Proprietary Depth' become your primary advantages", "A natural pulling away from 'Vain Metrics' toward 'True Value'", "Intuitive 'Past-Life' skills resurface — you'll suddenly master something 'hard'"],
        act:    ["Perform a 'Deep Audit' of your core technology or skill — make it world-class", "Cut the 'Fat' from your life and business — Ketu rewards minimalist precision", "Resist the urge to 'Scale Wide' — this is the time to 'Scale Deep'"],
        remedies: ["Digital Minimalism: Delete three apps or subscriptions that provide no real value", "Deep Work Immersion: Blocks of 4 hours for 'One Task Only' mastery", "Silent Retreat: Spend one morning a month in total silence to hear your 'Deep Voice'"]
    }
};


const SIGN_ORDER = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"];
const HOUSE_ORDINALS = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"];

const TITHI_NAMES = [
    "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Purnima",
    "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Amavasya"
];

const YOGA_NAMES = [
    "Vishkambha","Preeti","Ayushman","Saubhagya","Shobhana",
    "Atiganda","Sukarma","Dhriti","Shoola","Ganda",
    "Vriddhi","Dhruva","Vyaghata","Harshana","Vajra",
    "Siddhi","Vyatipata","Variyana","Parigha","Shiva",
    "Siddha","Sadhya","Shubha","Shukla","Brahma",
    "Indra","Vaidhriti"
];

const NAKSHATRA_DETAIL = {
    "Ashwini":          { deity: "Ashwini Kumaras (divine physicians)", meaning: "You came into the world moving fast. Your gift is the energy of beginnings — healing, speed, and the courage to leap before looking." },
    "Bharani":          { deity: "Yama (lord of dharma & transformation)", meaning: "You carry more than most people see. Your depth comes from understanding that creation and destruction are the same force." },
    "Krittika":         { deity: "Agni (sacred fire)", meaning: "Your mind cuts cleanly. You see through pretence, and your clarity — though sometimes sharp — is ultimately a gift to those around you." },
    "Rohini":           { deity: "Brahma (the creator)", meaning: "You nourish everything you touch. Beauty, abundance, and deep sensory richness are not indulgences for you — they are your natural language." },
    "Mrigashira":       { deity: "Soma (the Moon god)", meaning: "You are always searching — for the perfect idea, place, or understanding. Your curiosity is your greatest strength; let it roam freely." },
    "Ardra":            { deity: "Rudra (the storm)", meaning: "You understand destruction. You have lived through disruption and emerged sharper. Your rawness is your power, not your flaw." },
    "Punarvasu":        { deity: "Aditi (the boundless mother)", meaning: "You return. No matter how far you wander or how much is stripped away, you find your way back to your essential self." },
    "Pushya":           { deity: "Brihaspati (the great teacher)", meaning: "You nourish. Your deepest calling is to feed others — with wisdom, care, and a safe harbour they can return to. You are built to protect." },
    "Ashlesha":         { deity: "Naga (serpent consciousness)", meaning: "Your intelligence is coiled and patient. You understand people at a level they often can't articulate, and you use that knowledge wisely." },
    "Magha":            { deity: "Pitrs (ancestral lineage)", meaning: "You carry a lineage. There is a dignity and authority in you that traces back further than this life. Honour where you came from." },
    "Purva Phalguni":   { deity: "Bhaga (lord of fortune & delight)", meaning: "You were built to enjoy being alive. Creativity, pleasure, and deep rest are not luxuries for you — they restore your full power." },
    "Uttara Phalguni":  { deity: "Aryaman (the benefactor)", meaning: "You give. Partnership, service, and fair contracts are your natural terrain. You build structures that sustain others long after you leave." },
    "Hasta":            { deity: "Savitar (the skilled sun god)", meaning: "Your hands and mind work together. Craft, precision, and the ability to make things real are your primary tools in the world." },
    "Chitra":           { deity: "Vishvakarman (the cosmic architect)", meaning: "You see what things could look like at their best. Brilliance, design, and the drive for perfection are woven into your nature." },
    "Swati":            { deity: "Vayu (the wind god)", meaning: "You need freedom to move. Independence is not stubbornness — it is the condition under which you produce your best thinking and work." },
    "Vishakha":         { deity: "Indra-Agni (power & fire)", meaning: "You aim at a singular target and do not stop. The long wait before breakthrough is part of your design, not a sign that you are wrong." },
    "Anuradha":         { deity: "Mitra (the friend)", meaning: "Your loyalty is rare and real. The people you commit to — and the causes you commit to — know they have found something irreplaceable in you." },
    "Jyeshtha":         { deity: "Indra (king of gods)", meaning: "You lead, often before you are ready. Responsibility finds you. Your courage in taking it on — and your willingness to stand alone — is your mark." },
    "Mula":             { deity: "Nirriti (dissolution)", meaning: "You go to the root. You cannot accept surface explanations. Your path involves uprooting what is false to plant something that will last." },
    "Purva Ashadha":    { deity: "Apah (cosmic waters)", meaning: "You are unstoppable when you believe in the cause. Your confidence, once ignited, runs deep and carries others along in its current." },
    "Uttara Ashadha":   { deity: "Vishvadevas (universal gods)", meaning: "You are built for lasting victory — not the quick win, but the achievement that endures. Your success benefits more than just yourself." },
    "Shravana":         { deity: "Vishnu (the preserver)", meaning: "You listen at a depth most people cannot reach. You learn by absorbing, and your greatest insights come from what you hear between the words." },
    "Dhanishtha":       { deity: "Ashta Vasus (gods of abundance)", meaning: "Rhythm and ambition run through you simultaneously. You move fast, but you also know how to make a life resonate with what matters." },
    "Shatabhisha":      { deity: "Varuna (lord of cosmic law)", meaning: "You are a quiet investigator. Your healing and insight come from seeing what others overlook, and from a solitude that generates, not isolates." },
    "Purva Bhadrapada": { deity: "Aja Ekapada (the primal fire)", meaning: "You burn for something. The transformation you have lived through is not random — it is preparation for a purpose larger than you currently know." },
    "Uttara Bhadrapada":{ deity: "Ahir Budhnya (the deep serpent)", meaning: "Your wisdom is rooted in the unseen. Compassion, depth, and a quiet mastery of the inner world are your most enduring contributions." },
    "Revati":           { deity: "Pushan (the nurturer & guide)", meaning: "You carry people home. Your gift is safe passage — through transitions, across thresholds — and the nourishment that makes the journey bearable." }
};

const BHUKTI_DETAIL = {
    "Sun": {
        expect: ["A moment of personal clarity and heightened confidence — your signal is unusually strong", "Visibility opportunities arrive: public recognition, new contacts, leadership tests", "Conflicts around authority may surface — use them to define your boundaries clearly"],
        act:    ["Step into one visible leadership role you've been avoiding", "Clarify your personal brand and what you uniquely stand for right now", "Schedule a high-stakes conversation you've been delaying"],
        practices: ["Morning affirmation aligned to your core purpose (5 mins)", "Review your 3 non-negotiable values weekly — are your actions matching them?", "Spend one hour per week doing deep, undistracted solo work"]
    },
    "Moon": {
        expect: ["Heightened emotional sensitivity — your gut is unusually accurate this sub-period", "Shifts in your home environment, family dynamics, or key personal relationships", "Intuitive hunches that seem irrational but consistently prove correct"],
        act:    ["Trust your gut on one decision you've been over-analysing", "Spend deliberate time nurturing your closest relationships — they are your anchor", "Audit your physical environment — remove what drains you emotionally"],
        practices: ["Evening reflection journal: one win, one lesson, one gratitude (10 mins)", "Reduce decision fatigue — pick your 3 daily priorities the night before", "Weekly digital detox evening to let your nervous system reset"]
    },
    "Mars": {
        expect: ["A burst of energy and impatience — momentum is available if you channel it correctly", "Conflict or friction with others is likely; it is clearing old blockages, not creating new problems", "Opportunities that require bold, fast commitment rather than careful deliberation"],
        act:    ["Attack your single most important goal with focused intensity for 90-day sprints", "Resolve one lingering conflict directly rather than letting it fester", "Take the physical or strategic risk you have been calculating but not executing"],
        practices: ["Daily physical exertion (30 mins minimum) to metabolise the extra drive", "One uncomfortable action every morning before checking your phone", "Weekly review: did you move forward or just stay busy?"]
    },
    "Mercury": {
        expect: ["Your mind runs faster and connections click more easily — absorb this fully", "Networking and outreach yield unusually high-quality responses during this window", "Contracts, agreements, and written or spoken communication carry extra weight"],
        act:    ["Launch or deepen one communication-led initiative — writing, speaking, teaching", "Formalise any handshake agreements into written clarity before the window closes", "Learn one skill that directly removes your current biggest bottleneck"],
        practices: ["Read 30 mins daily in a domain adjacent to your work — cross-pollination accelerates", "Write one clear, concise summary of your strategy weekly to sharpen your thinking", "Audit your digital tools monthly — remove anything that adds friction, not leverage"]
    },
    "Jupiter": {
        expect: ["A window of genuine good fortune — doors open that require you to walk through them", "A teacher, mentor, or wise advisor appears and offers perspective you cannot yet see", "Your confidence in the bigger picture grows; small setbacks feel less significant"],
        act:    ["Say yes to one opportunity that stretches your current capacity", "Actively seek a mentor or guide who is 10 years ahead of where you want to be", "Be deliberately generous — share your knowledge or time without immediate return"],
        practices: ["Weekly gratitude practice focused on people who opened doors for you", "Invest 5% of your energy in someone junior — teaching accelerates your own mastery", "Review your 5-year vision — Jupiter sub-periods are windows for long-term decisions"]
    },
    "Venus": {
        expect: ["Relationships deepen and high-quality partnerships form more naturally than usual", "Financial flow improves — aesthetic, creative, and collaborative work receives recognition", "An appreciation for beauty, comfort, and meaningful pleasure returns to your daily life"],
        act:    ["Invest deliberately in one key relationship — professional or personal", "Upgrade one element of your workspace or daily environment for genuine quality", "Pursue one creative or aesthetic project you've been shelving for practicality"],
        practices: ["Schedule one no-agenda meal with a high-value relationship weekly", "Create something beautiful with your hands or words monthly", "Audit your income streams — Venus rewards quality and refinement, not hustle"]
    },
    "Saturn": {
        expect: ["Delays and friction are not punishment — they are quality control for your next chapter", "Discipline and consistency compound sharply during this window; shortcuts fail visibly", "Karmic debts surface to be settled; integrity in small things matters more than usual"],
        act:    ["Lock your core daily routine and protect it with near-religious consistency", "Complete the long, unglamorous foundational task you have been avoiding for months", "Honour every commitment, no matter how small — your word is your ledger"],
        practices: ["Daily grounding: 20 mins outdoors or in silence without screens", "One act of genuine service per week — help without expectation of return", "Weekly review of one structural weakness in your life or work and one concrete fix"]
    },
    "Rahu": {
        expect: ["Sudden, fast-moving opportunities in unfamiliar or 'foreign' territory", "Obsessive focus on a new goal — powerful if directed, destabilising if not grounded", "Unexpected disruptions that break old patterns — these are invitations, not threats"],
        act:    ["Pursue one unconventional strategy you have dismissed as too different or too risky", "Move into a new domain, market, or skill set that currently makes you slightly uncomfortable", "Establish one clear ethical boundary before the ambition surge peaks — Rahu rewards boldness but punishes dishonesty"],
        practices: ["10 mins of breathwork daily to stabilise Rahu's restless, amplifying energy", "One full day per month without screens or digital input to reset your nervous system", "Track your obsessions weekly — distinguish productive drive from anxious chasing"]
    },
    "Ketu": {
        expect: ["A pull towards silence, depth, and inner refinement rather than outer activity", "Sudden mastery in a domain you had not consciously practiced — past skill re-emerges", "A natural detachment from status, metrics, and social validation — lean into it"],
        act:    ["Perform a deep audit of your core skill or craft and make it genuinely world-class", "Cut one commitment, project, or relationship that no longer carries real meaning", "Spend extended time alone to hear your own signal clearly, without external noise"],
        practices: ["One morning of total silence per month — no input, no output, just presence", "4-hour deep work blocks with a single focus only — let the mind go narrow and deep", "Minimalist audit: remove three things (subscriptions, objects, commitments) that add no real value"]
    }
};

function interpretPlanet(name, info) {
    const container  = document.getElementById('techInterpretation');
    const role       = PLANET_ROLES[name] || { role: '', biz: '' };
    const specificText = (PLANET_IN_SIGN[name] || {})[info.sign] || SIGN_INTERPRETATIONS[info.sign] || '';
    const retroNote  = info.is_retrograde
        ? 'Retrograde — this planet\'s energy turns inward. Its lessons are being processed deeply before they can fully express.'
        : 'Direct — energy flows outward and expresses freely in the world.';
    const statusTag  = info.is_retrograde
        ? '<span class="interp-tag retro">Retrograde</span>'
        : '<span class="interp-tag direct">Direct</span>';

    container.innerHTML = `
        <div class="interp-planet-name">${name}</div>
        <div class="interp-placement">${info.sign} · ${info.degree_in_sign.toFixed(1)}°</div>
        <div class="interp-section-label">${role.role}</div>
        <p class="interp-body">${specificText}</p>
        <div class="interp-section-label">Motion</div>
        <p class="interp-body" style="color:var(--muted);font-size:0.85rem">${retroNote}</p>
        <div class="interp-meta">
            ${statusTag}
            <span class="interp-tag">${info.sign}</span>
            <span class="interp-tag">${info.degree_in_sign.toFixed(1)}°</span>
        </div>
    `;

    document.querySelectorAll('.planet-row').forEach(r => r.classList.remove('selected'));
    document.querySelector(`[data-planet="${name}"]`)?.classList.add('selected');

    // Sync Kundali chart highlight
    document.getElementById('kundaliChart')?._syncPlanet?.(info.sign);
}

function interpretDasha(mdLord, adLord, start, end, duration) {
    const container = document.getElementById('techInterpretation');
    const md        = DASHA_DETAIL[mdLord] || {};
    const bhukti    = BHUKTI_DETAIL[adLord] || {};

    const makeBullets = (items, cls) =>
        `<ul class="interp-bullet-list ${cls || ''}">${items.map(i => `<li>${i}</li>`).join('')}</ul>`;

    const expectItems = bhukti.expect?.length ? bhukti.expect : (md.expect || []);
    const actItems    = bhukti.act?.length    ? bhukti.act    : (md.act    || []);
    const practices   = bhukti.practices?.length ? bhukti.practices : (md.remedies || []);

    container.innerHTML = `
        <div class="interp-planet-name">${mdLord} MD · ${adLord} Bhukti</div>
        <div class="interp-placement">${start.slice(0,7).replace('-','/')} → ${end.slice(0,7).replace('-','/')} · ${duration.toFixed(1)} years</div>

        <div class="interp-section-label">Your life chapter</div>
        <p class="interp-body">${md.narrative || ''}</p>

        <div class="interp-section-label">Right now — ${adLord} Bhukti</div>
        <p class="interp-body">${(PLANET_ROLES[adLord]?.biz || '')}.</p>

        <div class="interp-section-label">What to expect</div>
        ${makeBullets(expectItems, '')}

        <div class="interp-section-label">What to do</div>
        ${makeBullets(actItems, '')}

        <div class="interp-section-label">Daily practices</div>
        ${makeBullets(practices, 'remedy-list')}

        <div class="interp-meta" style="margin-top:16px">
            <span class="interp-tag">${mdLord} MD</span>
            <span class="interp-tag">${adLord} Bhukti</span>
            <span class="interp-tag">${duration.toFixed(1)} yrs</span>
        </div>
    `;
}

function renderKundali(chartData) {
    const container = document.getElementById('kundaliChart');
    if (!container) return;

    const natal     = chartData.natal_planets || chartData.planets || {};
    const lagnaSign = (chartData.lagna || {}).sign || '';

    const GRID_SIGNS = [
        ['Pisces',      'Aries',   'Taurus',  'Gemini'],
        ['Aquarius',    null,      null,       'Cancer'],
        ['Capricorn',   null,      null,       'Leo'],
        ['Sagittarius', 'Scorpio', 'Libra',   'Virgo']
    ];

    const ABBR = { Sun:'Su', Moon:'Mo', Mars:'Ma', Mercury:'Me', Jupiter:'Ju', Venus:'Ve', Saturn:'Sa', Rahu:'Ra', Ketu:'Ke' };
    const PLANET_ORDER = ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu'];

    const signPlanets = {};
    Object.entries(natal).forEach(([name, info]) => {
        if (!info?.sign) return;
        (signPlanets[info.sign] = signPlanets[info.sign] || []).push({ abbr: ABBR[name] || name.slice(0,2), retro: info.is_retrograde });
    });

    const S = 320, C = S / 4;
    let svg = `<svg viewBox="0 0 ${S} ${S}" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block">`;

    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 4; col++) {
            const sign = GRID_SIGNS[row][col];
            const x = col * C, y = row * C;

            if (!sign) {
                if (row === 1 && col === 1) {
                    svg += `<rect x="${C}" y="${C}" width="${C*2}" height="${C*2}" rx="4" style="fill:var(--hero-bg)"/>`;
                    svg += `<text x="${S/2}" y="${S/2-8}" text-anchor="middle" style="fill:var(--accent);font-size:13px;font-weight:600;font-family:Inter,sans-serif;letter-spacing:0.04em">Kundali</text>`;
                    svg += `<text x="${S/2}" y="${S/2+9}" text-anchor="middle" style="fill:rgba(245,240,232,0.45);font-size:9px;font-family:Inter,sans-serif">${lagnaSign} Rising</text>`;
                    svg += `<text x="${S/2}" y="${S/2+23}" text-anchor="middle" style="fill:rgba(245,240,232,0.25);font-size:8px;font-family:Inter,sans-serif">South Indian</text>`;
                }
                continue;
            }

            const isLagna = sign === lagnaSign;
            const hasPlanets = (signPlanets[sign] || []).length > 0;
            const cursor = hasPlanets ? 'pointer' : 'default';
            svg += `<rect data-sign="${sign}" x="${x}" y="${y}" width="${C}" height="${C}" style="fill:${isLagna ? 'rgba(200,168,106,0.12)' : 'var(--surface)'};stroke:var(--border);stroke-width:1;cursor:${cursor};transition:fill 0.15s"/>`;

            if (isLagna) {
                svg += `<polyline points="${x},${y+22} ${x},${y} ${x+22},${y}" style="fill:none;stroke:var(--accent);stroke-width:2;stroke-linecap:round;pointer-events:none"/>`;
                svg += `<text x="${x+C-5}" y="${y+13}" text-anchor="end" style="fill:var(--accent);font-size:8px;font-weight:700;font-family:Inter,sans-serif;pointer-events:none">Lg</text>`;
            }

            svg += `<text x="${x+5}" y="${y+13}" style="fill:var(--muted);font-size:9px;font-family:Inter,sans-serif;pointer-events:none">${sign.slice(0,3)}</text>`;

            (signPlanets[sign] || []).forEach((p, i) => {
                const py = y + 27 + i * 13;
                if (py > y + C - 5) return;
                const rTag = p.retro ? `<tspan style="fill:var(--accent);font-size:7px" dy="-3">R</tspan><tspan dy="3"> </tspan>` : '';
                svg += `<text x="${x+C/2}" y="${py}" text-anchor="middle" style="fill:var(--text);font-size:11px;font-weight:500;font-family:Inter,sans-serif;pointer-events:none">${p.abbr}${rTag}</text>`;
            });
        }
    }

    svg += `<rect x="0.5" y="0.5" width="${S-1}" height="${S-1}" style="fill:none;stroke:var(--border);stroke-width:1.5;pointer-events:none"/>`;
    svg += '</svg>';
    container.innerHTML = svg;

    // Interactivity: hover + click to show planet interpretation
    const cellIndex = {};

    function selectCell(rect, sign) {
        container.querySelectorAll('[data-sign]').forEach(r => {
            const s = r.dataset.sign;
            delete r.dataset.selected;
            r.style.fill = s === lagnaSign ? 'rgba(200,168,106,0.12)' : 'var(--surface)';
            r.style.stroke = 'var(--border)';
            r.style.strokeWidth = '1';
        });
        rect.dataset.selected = '1';
        rect.style.fill = 'rgba(200,168,106,0.22)';
        rect.style.stroke = 'var(--accent)';
        rect.style.strokeWidth = '2';
    }

    container.querySelectorAll('[data-sign]').forEach(rect => {
        const sign = rect.dataset.sign;
        const planetsInSign = PLANET_ORDER.filter(n => natal[n]?.sign === sign);
        if (!planetsInSign.length) return;

        rect.addEventListener('mouseenter', () => {
            if (!rect.dataset.selected) rect.style.fill = 'rgba(200,168,106,0.18)';
        });
        rect.addEventListener('mouseleave', () => {
            if (!rect.dataset.selected) rect.style.fill = sign === lagnaSign ? 'rgba(200,168,106,0.12)' : 'var(--surface)';
        });
        rect.addEventListener('click', () => {
            selectCell(rect, sign);
            cellIndex[sign] = ((cellIndex[sign] ?? -1) + 1) % planetsInSign.length;
            interpretPlanet(planetsInSign[cellIndex[sign]], natal[planetsInSign[cellIndex[sign]]]);
        });
    });

    // Sync: clicking a planet row also highlights its Kundali cell
    container._syncPlanet = (planetSign) => {
        const rect = container.querySelector(`[data-sign="${planetSign}"]`);
        if (rect) selectCell(rect, planetSign);
    };
}

function populateTechnicalView() {
    if (!currentChartData) return;
    renderKundali(currentChartData);
    const { planets, dashas, business_pulse, nakshatra } = currentChartData;
    const [activeMD, activeAD] = business_pulse.active_dasha.split('-').map(s => s.trim());

    // Planet grid
    const planetGrid = document.getElementById('planetGrid');
    planetGrid.innerHTML = '';
    const lagnaSignIdx = SIGN_ORDER.indexOf(currentChartData.lagna?.sign || '');
    Object.entries(planets).forEach(([name, info]) => {
        const row = document.createElement('div');
        row.className   = 'planet-row';
        row.dataset.planet = name;
        const retroHtml = info.is_retrograde ? '<span class="retro-badge">R</span>' : '';
        const houseNum  = lagnaSignIdx >= 0
            ? ((SIGN_ORDER.indexOf(info.sign) - lagnaSignIdx + 12) % 12) + 1
            : null;
        const housePart = houseNum ? ` · ${HOUSE_ORDINALS[houseNum - 1]}` : '';
        row.innerHTML   = `
            <span class="planet-name">${name}${retroHtml}</span>
            <span class="planet-pos">${info.sign} ${info.degree_in_sign.toFixed(1)}°${housePart}</span>
        `;
        row.onclick = () => interpretPlanet(name, info);
        planetGrid.appendChild(row);

        if (name === 'Moon' && nakshatra) {
            const nd = NAKSHATRA_DETAIL[nakshatra.name] || {};
            const card = document.createElement('div');
            card.className = 'nak-mini-card';
            card.innerHTML = `
                <div class="nak-mini-name">${nakshatra.name} Nakshatra</div>
                <div class="nak-mini-meta">Lord: ${nakshatra.lord} · Deity: ${nd.deity || '—'} · Pada ${nakshatra.pada}</div>
                <p class="nak-mini-body">${nd.meaning || ''}</p>
            `;
            planetGrid.appendChild(card);
        }
    });

    // Dasha timeline
    const dashaTimeline = document.getElementById('dashaTimeline');
    dashaTimeline.innerHTML = '';
    dashas.forEach(md => {
        const isActiveMD = md.lord === activeMD;
        const item       = document.createElement('div');
        item.className   = 'dasha-md-item';

        const bhuktiHtml = md.bhuktis.map(ad => {
            const isActiveAD = isActiveMD && ad.lord === activeAD;
            const shortDate  = ad.start.slice(2, 7).replace('-', '/');
            return `
                <div class="bhukti-cell ${isActiveAD ? 'active-ad' : ''}"
                     onclick="event.stopPropagation(); interpretDasha('${md.lord}','${ad.lord}','${ad.start}','${ad.end}',${ad.duration})">
                    ${ad.lord}
                    <span class="ad-dates">${shortDate}</span>
                </div>`;
        }).join('');

        item.innerHTML = `
            <div class="dasha-md-header ${isActiveMD ? 'active' : ''}">
                <span class="md-lord">${md.lord} Maha-Dasha ${isActiveMD ? '· Active' : ''}</span>
                <div class="md-header-right">
                    <span class="md-dates">${md.start.slice(0,4)} – ${md.end.slice(0,4)}</span>
                    <span class="md-toggle" data-expanded="${isActiveMD}">${isActiveMD ? '▴' : '▾'}</span>
                </div>
            </div>
            <div class="bhukti-grid ${isActiveMD ? '' : 'hidden'}">${bhuktiHtml}</div>
        `;

        // Clicking the label area → show MD interpretation, expand bhuktis
        item.querySelector('.md-lord').onclick = (e) => {
            e.stopPropagation();
            const grid   = item.querySelector('.bhukti-grid');
            const toggle = item.querySelector('.md-toggle');
            grid.classList.remove('hidden');
            toggle.textContent = '▴';
            toggle.dataset.expanded = 'true';
            interpretDasha(md.lord, md.bhuktis[0].lord, md.start, md.end, md.duration);
        };

        // Clicking the arrow → just toggle expand/collapse
        item.querySelector('.md-toggle').onclick = (e) => {
            e.stopPropagation();
            const grid    = item.querySelector('.bhukti-grid');
            const toggle  = e.target;
            const hidden  = grid.classList.toggle('hidden');
            toggle.textContent = hidden ? '▾' : '▴';
            toggle.dataset.expanded = String(!hidden);
        };

        // Clicking the header row itself (not label or arrow) also expands + interprets
        item.querySelector('.dasha-md-header').onclick = () => {
            const grid   = item.querySelector('.bhukti-grid');
            const toggle = item.querySelector('.md-toggle');
            grid.classList.remove('hidden');
            toggle.textContent = '▴';
            toggle.dataset.expanded = 'true';
            interpretDasha(md.lord, md.bhuktis[0].lord, md.start, md.end, md.duration);
        };

        dashaTimeline.appendChild(item);
    });

    populateAdvancedAnalysis(currentChartData);
}

// ─── Advanced Analysis Population ────────────────────────────────────────────

function populateAdvancedAnalysis(data) {
    const { yogas, sade_sati, mangal_dosha, ashtakavarga, divisional_charts, varshaphal } = data;

    // Yogas
    const yogaContainer = document.getElementById('yogaCards');
    if (yogaContainer) {
        if (!yogas || yogas.length === 0) {
            yogaContainer.innerHTML = '<div class="yoga-empty">No prominent yogas detected in this chart.</div>';
        } else {
            yogaContainer.innerHTML = yogas.map(y => `
                <div class="yoga-card">
                    <div class="yoga-card-name">${y.name}</div>
                    <div class="yoga-card-type">${y.type}</div>
                    <div class="yoga-card-strength ${y.strength === 'Very Strong' ? 'very-strong' : ''}">${y.strength}</div>
                    <div class="yoga-card-desc">${y.description}</div>
                    <div class="yoga-card-impact">${y.business_impact}</div>
                </div>`).join('');
        }
    }

    // Sade Sati
    const ssEl = document.getElementById('sadeSatiCard');
    if (ssEl && sade_sati) {
        const badgeClass = sade_sati.active
            ? (sade_sati.severity === 'High' ? 'active' : 'moderate')
            : 'inactive';
        const remediesHtml = sade_sati.remedies?.length
            ? `<div class="adv-block-label" style="margin-top:12px">Remedies</div>
               <ul class="adv-remedies">${sade_sati.remedies.map(r => `<li>${r}</li>`).join('')}</ul>`
            : '';
        ssEl.innerHTML = `
            <div class="adv-status-row">
                <div class="adv-status-badge ${badgeClass}">${sade_sati.active ? sade_sati.phase : 'Not Active'}</div>
            </div>
            <div class="adv-status-desc">${sade_sati.description}</div>
            ${sade_sati.active ? `<div style="font-size:12px;color:var(--muted)">~${sade_sati.years_remaining} yrs remaining</div>` : ''}
            ${remediesHtml}`;
    }

    // Mangal Dosha
    const mdEl = document.getElementById('mangalDoshaCard');
    if (mdEl && mangal_dosha) {
        const badgeClass = mangal_dosha.active ? 'active' : 'inactive';
        const remediesHtml = mangal_dosha.remedies?.length
            ? `<div class="adv-block-label" style="margin-top:12px">Remedies</div>
               <ul class="adv-remedies">${mangal_dosha.remedies.map(r => `<li>${r}</li>`).join('')}</ul>`
            : '';
        const cancHtml = mangal_dosha.cancellations?.length
            ? `<div style="font-size:12px;color:#16a34a;margin-top:6px">${mangal_dosha.cancellations.join('<br>')}</div>`
            : '';
        mdEl.innerHTML = `
            <div class="adv-status-row">
                <div class="adv-status-badge ${badgeClass}">${mangal_dosha.active ? `${mangal_dosha.severity} · H${mangal_dosha.mars_house_from_lagna}` : 'None'}</div>
            </div>
            <div class="adv-status-desc">${mangal_dosha.description}</div>
            ${cancHtml}
            ${remediesHtml}`;
    }

    // Ashtakavarga
    const ashEl = document.getElementById('ashtakavargaGrid');
    if (ashEl && ashtakavarga?.houses) {
        const houses = ashtakavarga.houses;
        ashEl.innerHTML = Object.keys(houses).sort((a, b) => +a - +b).map(k => {
            const h = houses[k];
            return `<div class="ashtak-cell ${(h.strength || '').toLowerCase()}">
                <div class="ashtak-house">H${k}</div>
                <div class="ashtak-score">${h.bindus ?? h.score ?? 0}</div>
                <div class="ashtak-label">${h.strength}</div>
            </div>`;
        }).join('');
    }

    // Divisional Charts
    const navEl  = document.getElementById('navamsaCard');
    const dasEl  = document.getElementById('dasamsaCard');
    const d9 = divisional_charts?.d9;
    const d10 = divisional_charts?.d10;
    if (navEl && d9) {
        navEl.innerHTML = _renderDivChart(d9.planets, 'D-9 Lagna: ' + (d9.lagna || '—') + ' · ' + (d9.purpose || ''));
    }
    if (dasEl && d10) {
        dasEl.innerHTML = _renderDivChart(d10.planets, 'D-10 Lagna: ' + (d10.lagna || '—') + ' · ' + (d10.purpose || ''));
    }

    // Varshaphal
    const vpEl = document.getElementById('varshaphalCard');
    if (vpEl && varshaphal) {
        const vpPlanets = varshaphal.planets || {};
        const planetRows = Object.entries(vpPlanets).map(([p, pd]) =>
            `<div class="varsha-planet-row"><span>${p}</span><span class="varsha-planet-sign">${pd.sign}</span></div>`
        ).join('');
        const lagnaSign = varshaphal.lagna?.sign || varshaphal.lagna || '—';
        vpEl.innerHTML = `
            <div class="varsha-grid">
                <div class="varsha-cell"><div class="varsha-cell-label">Return Date</div><div class="varsha-cell-value" style="font-size:14px">${varshaphal.return_date || '—'}</div></div>
                <div class="varsha-cell"><div class="varsha-cell-label">Return Time (IST)</div><div class="varsha-cell-value">${varshaphal.return_time_ist || '—'}</div></div>
                <div class="varsha-cell"><div class="varsha-cell-label">Lagna</div><div class="varsha-cell-value">${lagnaSign}</div></div>
                <div class="varsha-cell"><div class="varsha-cell-label">Year</div><div class="varsha-cell-value">${varshaphal.year || '—'}</div></div>
            </div>
            <div class="varsha-planets">
                <div class="varsha-section-title">${varshaphal.interpretation || 'Solar Return Chart'}</div>
                ${planetRows}
            </div>`;
    }
}

function _renderDivChart(chartData, title) {
    if (!chartData) return '<div style="color:var(--muted);font-size:13px;padding:12px">Data unavailable</div>';
    const rows = Object.entries(chartData).map(([p, d]) =>
        `<div class="div-chart-planet">
            <span class="div-planet-name">${p}</span>
            <span class="div-planet-sign">${d.sign || '—'}</span>
            <span class="div-planet-deg" style="font-size:11px;color:var(--muted)">${d.natal_sign ? '← ' + d.natal_sign : ''}</span>
        </div>`).join('');
    return `<div style="font-size:12px;color:var(--muted);margin-bottom:10px;font-weight:600;padding:12px 0 0">${title}</div>${rows}`;
}

// ── Progressive landing reveal ────────────────────────────
function initLandingReveal() {
    const nameEl     = document.getElementById('fullName');
    const dateEl     = document.getElementById('date');
    const cardTag    = document.getElementById('previewCardTag');
    const lockedHint = document.getElementById('previewLockedHint');
    const sunPreview = document.getElementById('sunSignPreview');

    const SIGN_NATAL_PREVIEW = {
        "Aries":       "You came here to initiate. There is a fire in you that wants to move first, break ground, and lead the charge — even when no one asked you to.",
        "Taurus":      "You came here to build. Your gifts are patience, loyalty, and the rare ability to create things that last long after the rush has faded.",
        "Gemini":      "You came here to connect. Your mind bridges worlds, people, and ideas — you are the living conversation between things that did not know they were related.",
        "Cancer":      "You came here to protect. You sense the emotional weather in any room and your deepest instinct is to make people feel safe enough to be themselves.",
        "Leo":         "You came here to lead with your heart. Your warmth, generosity, and refusal to hide are not indulgences — they are your contribution to the world.",
        "Virgo":       "You came here to perfect. You notice the gap between what is and what could be — and you close it with work, care, and quietly extraordinary precision.",
        "Libra":       "You came here to harmonise. You carry an instinct for fairness that most people have to learn. Your gift is making the complex feel balanced and the broken feel whole.",
        "Scorpio":     "You came here to transform. You are unafraid of what is real, what is hidden, or what must be released. You go where others will not — and bring back what matters.",
        "Sagittarius": "You came here to search. Your hunger for truth, meaning, and the widest possible view is not restlessness — it is your compass pointing toward the work only you can do.",
        "Capricorn":   "You came here to endure. Your patience is not passive — it is the deep, structural patience of someone who is building something worth outlasting them.",
        "Aquarius":    "You came here to see ahead. Your sense that the world could be radically different is not naive — it is the perception that makes genuine change possible.",
        "Pisces":      "You came here to feel what others cannot. Your sensitivity is not weakness — it is the instrument through which you perceive what logic alone will always miss."
    };

    function getApproxSunSign(dateStr) {
        const d = new Date(dateStr + 'T12:00:00');
        const m = d.getMonth() + 1, day = d.getDate();
        if ((m === 3 && day >= 21) || (m === 4 && day <= 19)) return 'Aries';
        if ((m === 4 && day >= 20) || (m === 5 && day <= 20)) return 'Taurus';
        if ((m === 5 && day >= 21) || (m === 6 && day <= 20)) return 'Gemini';
        if ((m === 6 && day >= 21) || (m === 7 && day <= 22)) return 'Cancer';
        if ((m === 7 && day >= 23) || (m === 8 && day <= 22)) return 'Leo';
        if ((m === 8 && day >= 23) || (m === 9 && day <= 22)) return 'Virgo';
        if ((m === 9 && day >= 23) || (m === 10 && day <= 22)) return 'Libra';
        if ((m === 10 && day >= 23) || (m === 11 && day <= 21)) return 'Scorpio';
        if ((m === 11 && day >= 22) || (m === 12 && day <= 21)) return 'Sagittarius';
        if ((m === 12 && day >= 22) || (m === 1 && day <= 19)) return 'Capricorn';
        if ((m === 1 && day >= 20) || (m === 2 && day <= 18)) return 'Aquarius';
        return 'Pisces';
    }

    // Step 1 — name personalises the Nakshatra card header
    nameEl?.addEventListener('input', () => {
        const first = nameEl.value.trim().split(' ')[0];
        if (cardTag) cardTag.textContent = first ? `${first}'s Nakshatra reading` : 'Your Nakshatra reading';
    });

    // Step 2 — birth date reveals a sun sign preview card + personalises Dasha card
    dateEl?.addEventListener('change', () => {
        const val = dateEl.value;
        if (!val || !sunPreview) return;

        const sign = getApproxSunSign(val);
        sunPreview.innerHTML = `
            <div class="preview-sun-tag">Sun in ${sign} · A first glimpse</div>
            <p class="preview-sun-text">${SIGN_NATAL_PREVIEW[sign] || ''}</p>
            <div class="preview-sun-note">Exact Vedic positions are calculated when you generate your chart</div>
        `;
        sunPreview.classList.remove('hidden');
        if (lockedHint) lockedHint.textContent = 'Generate your chart to unlock your full reading →';

        // Dasha card scarcity — personalise with age
        const birthDate   = new Date(val + 'T12:00:00');
        const today       = new Date();
        const ageYears    = today.getFullYear() - birthDate.getFullYear() -
            (today < new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate()) ? 1 : 0);
        const birthYear   = birthDate.getFullYear();
        const firstName   = nameEl?.value.trim().split(' ')[0] || '';
        const subject     = firstName || 'You';
        const verb        = firstName ? 'are' : 'are';

        const titleEl   = document.getElementById('dashaCardTitle');
        const bodyEl    = document.getElementById('dashaCardBody');
        const exampleEl = document.getElementById('dashaCardExample');
        const personalEl = document.getElementById('dashaCardPersonal');

        if (titleEl) titleEl.textContent = `${subject} ${verb} ${ageYears}. Your chapter is running.`;
        if (bodyEl)  bodyEl.textContent  = `Born ${birthYear}. Right now, Vedic timing has placed ${firstName ? 'you' : 'you'} inside one of nine named chapters — each with its own theme, its own lord, and its own end date. Some last 6 years. Some last 20.`;
        if (exampleEl) exampleEl.classList.add('hidden');
        if (personalEl) {
            personalEl.innerHTML = `<span class="dasha-urgency">Generate your chart to see which chapter you're in — and how long remains.</span>`;
            personalEl.classList.remove('hidden');
        }
    });
}

// ── Edit details ──────────────────────────────────────────
function editDetails() {
    document.getElementById('landingScreen').classList.remove('hidden');
    document.getElementById('resultsScreen').classList.add('hidden');
    document.getElementById('feedbackWidget').classList.add('hidden');
}

// ── Share reading ─────────────────────────────────────────
function buildShareText(data) {
    const name    = data.user_name ? `${data.user_name}'s` : 'My';
    const coach   = data.coach_insights || {};
    const pulse   = data.business_pulse || {};
    const natal   = data.natal_planets  || data.planets || {};
    const lagna   = data.lagna || {};
    const nakStr  = natal.Moon ? ` · Moon in ${natal.Moon.sign}` : '';

    const lines = [
        `✦ ${name} Cosmic OS Reading — ${new Date().toLocaleDateString('en-IN', {day:'numeric',month:'long',year:'numeric'})}`,
        '',
        `Theme: ${coach.daily_theme || '—'}`,
        `Energy: ${coach.energy_signature || '—'}`,
        '',
        coach.uplift_narrative || '',
        '',
        `Birth chart: ${lagna.sign ? lagna.sign + ' Rising' : ''}${nakStr}`,
        pulse.display_dasha ? `Life chapter: ${pulse.display_dasha}` : '',
        pulse.focus          ? `Focus: ${pulse.focus}` : '',
        '',
        coach.operational_pointer || '',
        '',
        '— Generated by Cosmic OS (cosmicosveda.in)'
    ];
    return lines.filter(l => l !== undefined).join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

function initShareBtn() {
    const btn = document.getElementById('shareReadingBtn');
    if (!btn) return;
    btn.addEventListener('click', async () => {
        if (!currentChartData) return;
        const text = buildShareText(currentChartData);
        if (navigator.clipboard && navigator.clipboard.writeText) {
            try {
                await navigator.clipboard.writeText(text);
                const orig = btn.innerHTML;
                btn.textContent = '✓ Copied';
                setTimeout(() => { btn.innerHTML = orig; }, 2000);
                return;
            } catch (_) {}
        }
        window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    });
}

// ── Boot ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    checkUserProfile();
    initTabs();
    initHeroSearch();
    initLandingReveal();
    initShareBtn();

    document.getElementById('generateBtn').addEventListener('click', generateChart);
});

// ── Quick Unlock (Friction Reduction) ─────────────────────
async function quickUnlock() {
    const date = document.getElementById("date").value;
    const name = document.getElementById("fullName").value;
    const precisionFields = document.getElementById("precisionFields");
    const generateBtn = document.getElementById("generateBtn");
    
    if (!date || date === "1990-01-01") return;

    // Show the rest of the form
    if (precisionFields) precisionFields.classList.remove("hidden");
    if (generateBtn) generateBtn.classList.remove("hidden");

    try {
        const res = await fetch(`/api/quick-decode?date=${date}&name=${encodeURIComponent(name)}`);
        const data = await res.json();
        
        if (data.error) return;

        // Update Preview Card
        const previewTag = document.getElementById("previewCardTag");
        const previewQuote = document.querySelector(".preview-quote");
        const previewSource = document.querySelector(".preview-quote-source");
        const previewOverlay = document.getElementById("previewFadeOverlay");

        if (previewTag) previewTag.textContent = `Your ${data.sun_sign} Nature`;
        if (previewQuote) {
            previewQuote.textContent = `"${data.natal}"`;
            previewQuote.style.opacity = "1";
        }
        if (previewSource) {
            previewSource.textContent = `${data.sun_sign} · Mulank ${data.mulank} · Bhagyank ${data.bhagyank}`;
            previewSource.style.opacity = "1";
        }
        
        // Remove the locked overlay
        if (previewOverlay) {
            previewOverlay.style.opacity = "0";
            setTimeout(() => {
                previewOverlay.classList.add("hidden");
                // Ensure form components are definitely visible
                if (precisionFields) precisionFields.classList.remove("hidden");
                if (generateBtn) generateBtn.classList.remove("hidden");
            }, 300);
        }

    } catch (e) {
        console.error("Quick unlock failed", e);
    }
}

// ── Cosmic Pulse Intelligence (v2) ────────────────────────
async function updateCosmicPulse() {
    try {
        const res = await fetch("/api/v2/intelligence");
        const data = await res.json();
        const pulse = data.transits;

        if (!pulse || pulse.error) return;

        const ticker = document.getElementById("cosmicPulseTicker");
        const progress = document.getElementById("tickerProgress");
        const vibe = document.getElementById("tickerVibe");
        const highlight = document.getElementById("tickerHighlight");

        if (ticker) ticker.classList.remove("hidden");
        if (progress) progress.style.width = `${pulse.score}%`;
        if (vibe) vibe.textContent = pulse.vibe;
        if (highlight) highlight.textContent = pulse.highlights[0] || "Global transits are stable. Maintain focus.";

    } catch (e) {
        console.error("Pulse update failed", e);
    }
}

// Start Pulse loop every 60 seconds
setInterval(updateCosmicPulse, 60000);

// ── Lucky Windows Intelligence (v2) ──────────────────────
function renderLuckyWindows(data) {
    const grid = document.getElementById("luckyWindowsGrid");
    const section = document.getElementById("luckyWindowsSection");
    if (!grid || !data || !data.windows) return;
    
    section.classList.remove("hidden");
    grid.innerHTML = "";
    
    // Show top 12 windows for cleaner UI
    const topWindows = data.windows.slice(0, 12);
    
    topWindows.forEach(win => {
        const div = document.createElement("div");
        div.className = "lucky-item";
        
        const vibeClass = win.score > 70 ? "vibe-peak" : (win.score > 55 ? "vibe-good" : "vibe-neut");
        const dateObj = new Date(win.timestamp.replace(" ", "T"));
        const timeStr = dateObj.toLocaleDateString([], {month:"short", day:"numeric"}) + " · " + dateObj.toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});

        div.innerHTML = `
            <span class="lucky-time">${timeStr}</span>
            <div class="lucky-score">${win.score}%</div>
            <span class="lucky-vibe-tag ${vibeClass}">${win.vibe}</span>
        `;
        grid.appendChild(div);
    });
}

// ── Subscription & Retention (v2) ─────────────────────────
function renderSubscriptionHook(data) {
    const hook = document.getElementById("subHook");
    const subText = document.getElementById("subText");
    if (!hook || !data || !data.next_peak_window) return;
    
    hook.classList.remove("hidden");
    const win = data.next_peak_window;
    const dateObj = new Date(win.timestamp.replace(" ", "T"));
    const timeStr = dateObj.toLocaleDateString([], {weekday:"short", hour:"2-digit"});
    
    subText.textContent = `Strategic Peak Window: ${timeStr} (${win.score}% momentum).`;
}

function toggleSub() {
    alert("Subscription logic enabled. You will now receive a browser notification when your peak window opens.");
    // In production, this would trigger a POST to /api/v2/preferences
}

function resetSession() {
    if (confirm("This will clear your chart and return to the start. Proceed?")) {
        localStorage.clear();
        window.location.href = "/auth/logout";
    }
}

// ── Remedy & Progress Intelligence (v2) ──────────────────
function renderRemedies(data) {
    const grid = document.getElementById("remediesGrid");
    const section = document.getElementById("remediesSection");
    if (!grid || !data || data.length === 0) return;
    
    section.classList.remove("hidden");
    grid.innerHTML = "";
    
    data.forEach(rem => {
        const div = document.createElement("div");
        div.className = "remedy-card";
        const priorityClass = rem.priority.toLowerCase() === "high" ? "high" : "";
        
        div.innerHTML = `
            <div class="rem-header">
                <div class="rem-challenge">${rem.challenge}</div>
                <div class="rem-tag ${priorityClass}">${rem.priority} Priority</div>
            </div>
            <div class="rem-body">
                <div class="rem-item">
                    <span class="rem-label">Progress Signal</span>
                    <span class="rem-value">${rem.progress_signal}</span>
                </div>
                <div class="rem-item">
                    <span class="rem-label">Strategic Ritual</span>
                    <span class="rem-value">${rem.ritual}</span>
                </div>
                <div class="rem-item">
                    <span class="rem-label">Supplements</span>
                    <span class="rem-value">${rem.supplement}</span>
                </div>
                <div class="rem-item">
                    <span class="rem-label">Natural Stones</span>
                    <span class="rem-value">${rem.stone}</span>
                    <span class="rem-product-link" onclick="alert('Product catalog coming soon in Phase 4')">View Collection →</span>
                </div>
            </div>
        `;
        grid.appendChild(div);
    });
}

// ── Marketing Persona Intelligence (v2) ──────────────────
function renderPersona(data) {
    const badge = document.getElementById("personaBadge");
    if (!badge || !data || !data.name) return;
    
    badge.textContent = data.name;
    badge.classList.remove("hidden");
    
    // Log for marketing analysis
    console.log(`[Marketing] Detected Persona: ${data.name} | Hook: ${data.retention_hook}`);
}
