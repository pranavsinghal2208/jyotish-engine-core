// ── Gender toggle ─────────────────────────────────────────────

function setGender(gender) {
    document.getElementById('gender').value = gender;
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `gender${gender}`);
    });
}

// ── Numerology description repository ────────────────────────
const NUM_DESC = {
    mulank: {
        1: { planet: "Sun", keyword: "Pioneer", desc: "You are built to initiate. The Sun drives you toward leadership, independence, and originality. You do not follow — you set direction. The challenge is learning that leading from ego burns bridges; leading from vision builds empires." },
        2: { planet: "Moon", keyword: "Diplomat", desc: "You are the force behind the scenes. The Moon gives you extraordinary emotional intelligence, the ability to read a room instantly, and a gift for mediation. Your strength is not loudness — it is depth. Partnerships and patience are your power zones." },
        3: { planet: "Jupiter", keyword: "Communicator", desc: "Jupiter expands everything it touches, and for you that means self-expression, optimism, and creative output. You naturally attract people, opportunities, and luck. The trap is scattering — Jupiter's abundance can become excess without discipline." },
        4: { planet: "Rahu", keyword: "Builder", desc: "Rahu gives you relentless drive, an appetite for unconventional paths, and a builder's patience. You construct what others only dream. The shadow: obsessive focus can tip into rigidity. Your greatest work comes when you balance structure with adaptability." },
        5: { planet: "Mercury", keyword: "Catalyst", desc: "Mercury makes you fast, versatile, and perpetually curious. You process faster than almost anyone around you, shift gears effortlessly, and see connections others miss. The challenge is depth — your gift for variety can prevent mastery." },
        6: { planet: "Venus", keyword: "Nurturer", desc: "Venus orients you toward beauty, harmony, responsibility, and love. You feel a deep pull to care for others — family, community, creative work. Relationships are your curriculum. The lesson: you cannot pour from an empty vessel." },
        7: { planet: "Ketu", keyword: "Seeker", desc: "Ketu strips away the material and points you inward. You are unusually analytical, philosophical, and spiritually wired. You see through surfaces others accept as real. The challenge: detachment can shade into isolation. Your wisdom is meant to be shared." },
        8: { planet: "Saturn", keyword: "Authority", desc: "Saturn tests before it rewards. You are built for authority, long games, and material mastery — but none of it comes easily. What you earn, you keep. What you build, you build to last. The lesson: power used without responsibility always returns as loss." },
        9: { planet: "Mars", keyword: "Humanitarian", desc: "Mars gives you fire, courage, and an instinct for justice. You complete cycles — you are the person who finishes what others start. At your best you are selfless, visionary, and fearless. The trap is aggression when things don't move at your pace." },
    },
    bhagyank: {
        1: { keyword: "Pioneering Path", desc: "Your destiny line asks you to lead — to start things, take independent action, and own your decisions. You are being shaped, over a lifetime, into someone who creates rather than reacts. Every major chapter will test your courage to go first." },
        2: { keyword: "Partnership Path", desc: "Your life unfolds through relationships, collaboration, and sensitivity. You are being shaped into a master of nuance — someone who can hold two truths at once. The big chapters of your life will hinge on who you choose to build with." },
        3: { keyword: "Expression Path", desc: "Your destiny runs through communication, creativity, and inspiration. The life chapters that feel most meaningful will be the ones where you create something — write it, speak it, teach it, build it. Joy is part of your assignment, not a distraction from it." },
        4: { keyword: "Foundation Path", desc: "Your destiny is to build things that last — systems, organisations, families, crafts. The 4 path is not glamorous, but it is load-bearing. The world needs your steadiness more than it needs your sparkle. Master the invisible work." },
        5: { keyword: "Freedom Path", desc: "Your destiny runs through change, movement, and experience. You are being shaped by variety — not as escape, but as curriculum. Every pivot, every unexpected turn, is teaching you something that a conventional life cannot. Trust the detour." },
        6: { keyword: "Service Path", desc: "Your destiny is service — not servitude, but the deep satisfaction of making things better for others. Home, family, healing, and community are your arenas. You are being shaped into someone whose reliability becomes a kind of love." },
        7: { keyword: "Wisdom Path", desc: "Your destiny is understanding — deep, hard-won, private understanding. You are here to ask the questions others avoid. Your most important contributions will come from periods of solitude, study, and reflection. Trust the process of going deep." },
        8: { keyword: "Mastery Path", desc: "Your destiny runs through achievement, material mastery, and the right use of power. You are being groomed for authority — but only after you have learned the lessons of integrity. Money and power are teachers on your path, not distractions from it." },
        9: { keyword: "Completion Path", desc: "Your destiny involves endings, release, and transformation. You are here to distil wisdom from experience and offer it back. Every time you release what no longer serves — a role, a relationship, a version of yourself — you step closer to your actual purpose." },
    },
    kua: {
        1: { group: "East Group", directions: "SE, E, S, N", avoid: "NE, SW, NW, W", desc: "Your power directions are Southeast (growth), East (health), South (prosperity), and North (personal development). Face these when working, negotiating, or sleeping to align with your natural energy flow." },
        2: { group: "West Group", directions: "NE, W, NW, SW", avoid: "SE, E, S, N", desc: "Your power directions are Northeast (knowledge), West (creativity), Northwest (mentors), and Southwest (relationships). Arrange your workspace and home to face these for maximum support." },
        3: { group: "East Group", directions: "S, N, SE, E", avoid: "SW, NW, NE, W", desc: "South (fame/recognition) and North (career growth) are your top directions. You thrive when oriented toward movement and expansion. Face South during important presentations." },
        4: { group: "East Group", directions: "N, S, SE, E", avoid: "NW, SW, W, NE", desc: "North is your strongest personal direction — excellent for sleep orientation and desk placement. You are energetically wired for learning, growth, and upward movement." },
        5: { group: "West Group (M)", directions: "NE, W, NW, SW", avoid: "SE, E, S, N", desc: "As a Kua 5 (male), you align with the West group. Face Northeast for your sharpest thinking and decision-making. This number sits at the centre of the Lo Shu grid — you are a natural mediator." },
        6: { group: "West Group", directions: "W, NE, SW, NW", avoid: "E, SE, N, S", desc: "West is your personal prosperity direction. Northwest activates mentor energy — face it when seeking guidance or making strategic decisions. Your natural authority is amplified in West-group spaces." },
        7: { group: "West Group", directions: "NW, SW, NE, W", avoid: "N, S, E, SE", desc: "Northwest activates your leadership and sky-luck direction. You are energetically suited to positions of quiet authority. Arrange important spaces so you face NW for maximum leverage." },
        8: { group: "West Group", directions: "SW, NW, W, NE", avoid: "S, N, SE, E", desc: "Southwest (relationships and stability) is your primary direction. You accumulate energy — and wealth — steadily when aligned. Face SW for financial decisions and major negotiations." },
        9: { group: "East Group", directions: "E, SE, S, N", avoid: "W, NW, SW, NE", desc: "East (health and vitality) and Southeast (wealth and abundance) are your primary directions. You are energetically expansive — fame, recognition, and creative work are amplified when you face South." },
    },
    gift: "Your Gift Number is the unreduced total of all letters in your full name before the final digit reduction. When it contains a Master Number (11, 22, 33), those double-digit energies are kept intact — they represent an amplified potential, above the base single digit. This number shows latent talent that doesn't announce itself; it tends to emerge through practice and crisis."
};

const NAK_DESC = {
    "Ashwini":    { lord: "Ketu",    quality: "Active", desc: "Swift, pioneering, and healing. You have a natural instinct for beginnings — you arrive early, move fast, and catalyse. The healer archetype lives here: a drive to fix, restore, and initiate. Guard against impatience and recklessness." },
    "Bharani":    { lord: "Venus",   quality: "Active", desc: "Intense, creative, and transformative. You carry the energy of birth and death simultaneously — a tolerance for extremes that most people avoid. Artistic depth, sensuality, and fierce loyalty define you. Guard against possessiveness." },
    "Krittika":   { lord: "Sun",     quality: "Mixed",  desc: "Sharp, purifying, and determined. You cut through what is false with precision. The Sun's directness runs through your nature — a brightness that can illuminate or burn. Leadership and discernment are your core gifts." },
    "Rohini":     { lord: "Moon",    quality: "Passive", desc: "Magnetic, creative, and deeply sensual. The Moon in its most fertile and beautiful placement. You attract naturally — beauty, abundance, and comfort flow toward you when you are aligned. Growth and material pleasure are your domains." },
    "Mrigashira": { lord: "Mars",    quality: "Passive", desc: "Curious, searching, and perpetually in motion. You are a seeker — always scanning for the next discovery. Mrigashira energy is gentle but restless, intellectually alive, and perennially romantic. Learn to inhabit the present." },
    "Ardra":      { lord: "Rahu",    quality: "Active",  desc: "Turbulent, transformative, and brutally honest. Ardra strips away pretence through storm. You have survived intensity that others haven't, and it has made you sharper. Your empathy is born from having been broken and rebuilt." },
    "Punarvasu":  { lord: "Jupiter", quality: "Passive", desc: "Optimistic, nurturing, and philosophical. Punarvasu means 'return of light.' You have an extraordinary capacity for renewal — you come back. Jupiter's wisdom and abundance run through your nature; you are a natural teacher." },
    "Pushya":     { lord: "Saturn",  quality: "Passive", desc: "Nourishing, responsible, and deeply reliable. The most auspicious of all nakshatras. Saturn gives you discipline, and Pushya gives you the heart to use it in service of others. You are the person people come to when things break." },
    "Ashlesha":   { lord: "Mercury", quality: "Active",  desc: "Intense, perceptive, and psychologically complex. Ashlesha sees everything — your ability to read beneath the surface of people and situations is unmatched. Use it for healing, not manipulation. Your intuition is your most accurate instrument." },
    "Magha":      { lord: "Ketu",    quality: "Active",  desc: "Regal, ancestral, and magnetically authoritative. Magha carries the energy of lineage — you feel a pull toward legacy, leadership, and honoring what came before. People recognise something in you that is older than this lifetime." },
    "Purva Phalguni": { lord: "Venus", quality: "Passive", desc: "Pleasure-seeking, creative, and magnetic. Venus in full expression — an artist, lover, and performer. You are here to enjoy, to create beauty, and to connect deeply. Rest and pleasure are not indulgences for you; they are your fuel." },
    "Uttara Phalguni": { lord: "Sun", quality: "Passive", desc: "Generous, socially gifted, and quietly powerful. You have a talent for bringing people together and a deep need to be of use. The Sun gives you natural authority; Uttara Phalguni gives you the warmth to wield it without alienating." },
    "Hasta":      { lord: "Moon",    quality: "Passive", desc: "Skilled, practical, and emotionally intelligent. Your hands are your instrument — craft, precision, and the ability to make things work beautifully. You are dexterous in mind and body, and people trust you because you deliver." },
    "Chitra":     { lord: "Mars",    quality: "Active",  desc: "Aesthetic, perfectionist, and brilliantly visual. You see the world in terms of structure and beauty simultaneously. Mars gives you drive; Chitra gives you taste. Architecture, design, fashion, strategy — wherever beauty requires precision, you belong." },
    "Swati":      { lord: "Rahu",    quality: "Passive", desc: "Independent, curious, and remarkably adaptable. Like a blade of grass in the wind, you bend without breaking. Rahu makes you restless and boundary-pushing; Swati channels it into diplomacy and innovation. You are surprisingly difficult to pin down." },
    "Vishakha":   { lord: "Jupiter", quality: "Mixed",   desc: "Purposeful, ambitious, and intensely focused. Jupiter gives you vision; Vishakha gives you the relentless drive to reach the goal regardless of how long it takes. You do not give up. The danger is fanaticism — pursue your goal without losing your humanity." },
    "Anuradha":   { lord: "Saturn",  quality: "Passive", desc: "Devoted, socially gifted, and quietly perseverant. Saturn's discipline is softened here by the nakshatra's gift for friendship and collaboration. You build loyal relationships over time — and those relationships become your greatest resource." },
    "Jyeshtha":   { lord: "Mercury", quality: "Active",  desc: "Senior, protective, and intensely competent. Jyeshtha means 'eldest' — the one who carries responsibility, leads the group, and does not flinch. You are capable of enormous pressure. The shadow: the need to control what cannot be controlled." },
    "Mula":       { lord: "Ketu",    quality: "Active",  desc: "Radical, penetrating, and built for transformation. Ketu strips away the inessential, and Mula begins at the root. You go to the foundation of things — philosophically, professionally, personally. Upheaval often precedes your greatest chapters." },
    "Purva Ashadha": { lord: "Venus", quality: "Active", desc: "Invincible, passionate, and undefeated. Venus gives you charm; Purva Ashadha gives you a fire that does not go out. You do not yield easily. Your persistence is your superpower — and the source of your deepest frustrations when fighting the wrong battles." },
    "Uttara Ashadha": { lord: "Sun", quality: "Passive", desc: "Victorious, principled, and built for the long game. The Sun's permanence is expressed here. You do not peak early — your greatest work comes through sustained effort over years. Integrity is non-negotiable for you; compromise rarely serves you." },
    "Shravana":   { lord: "Moon",    quality: "Passive", desc: "A listener, a learner, and a connector of wisdom. The Moon makes you extraordinarily receptive — you absorb what others miss. Shravana natives often become repositories of knowledge, culture, and tradition. Teach what you've learned." },
    "Dhanishtha": { lord: "Mars",    quality: "Mixed",   desc: "Abundant, musical, and powerfully self-sufficient. Mars gives you enterprise; Dhanishtha gives you rhythm — an instinct for timing that makes your moves land. Wealth and recognition come when you trust your instinct and move on beat." },
    "Shatabhisha": { lord: "Rahu",   quality: "Passive", desc: "Solitary, healing, and profoundly original. Rahu here drives you toward the unconventional, the esoteric, and the hidden. You are a researcher of truth — in science, spirituality, or both. Your best work often happens alone, in depth." },
    "Purva Bhadrapada": { lord: "Jupiter", quality: "Active", desc: "Passionate, transformative, and intensely visionary. Jupiter's wisdom is weaponised here — you are a firebrand philosopher. You can move people with words and ideas. The challenge is channelling the fire constructively rather than burning the very things you're trying to build." },
    "Uttara Bhadrapada": { lord: "Saturn", quality: "Passive", desc: "Deep, compassionate, and enduring. Saturn's wisdom at its most refined — patient, universal, unhurried. You are interested in the big picture, the long arc, the truth beneath the obvious. You age into your power rather than peaking early." },
    "Revati":     { lord: "Mercury", quality: "Passive", desc: "Gentle, spiritually attuned, and deeply empathetic. Mercury's perceptiveness softened into intuition. You feel the emotional temperature of any room. Your gifts include nurturing, healing, and safe-guiding others across transitions. An old soul energy." },
};

// Expose for use in app.js
window.NAK_DESC = NAK_DESC;

// ── Jyotish Numerology — current user ─────────────────────────

function _setOrCreate(id, html) {
    let el = document.getElementById(id);
    if (!el) {
        el = document.createElement('div');
        el.id = id;
        el.className = 'jy-num-desc';
        const ref = document.getElementById(id.replace('Desc', ''));
        if (ref) ref.closest('.jy-num-card')?.appendChild(el);
    }
    el.innerHTML = html;
}

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
        const namankVal = typeof d.namank === 'object' ? d.namank.number : d.namank;
        document.getElementById('jyNamank').textContent = namankVal;
        const namankMeaning = typeof d.namank === 'object' ? d.namank.meaning : null;
        if (namankMeaning) _setOrCreate('jyNamankDesc', namankMeaning);

        // Inject descriptions
        const mulankInfo = NUM_DESC.mulank[d.mulank];
        if (mulankInfo) {
            _setOrCreate('jyMulankDesc', `<strong>${mulankInfo.keyword}</strong> · ${mulankInfo.planet} · ${mulankInfo.desc}`);
        }
        const bhagyankInfo = NUM_DESC.bhagyank[d.bhagyank];
        if (bhagyankInfo) {
            _setOrCreate('jyBhagyankDesc', `<strong>${bhagyankInfo.keyword}</strong> · ${bhagyankInfo.desc}`);
        }
        const kuaInfo = NUM_DESC.kua[d.kua_number];
        if (kuaInfo) {
            const kuaEl = document.getElementById('jyKuaDesc');
            if (kuaEl) kuaEl.innerHTML = `<strong style="color:var(--gold,#C8A86A)">${kuaInfo.group}</strong><br>Best directions: <strong>${kuaInfo.directions}</strong><br><span style="opacity:0.8">${kuaInfo.desc}</span>`;
        }
        // Gift Number: full reduction chain + personal meaning
        const giftRaw = d.gift_number;
        const masterNums = [11, 22, 33];
        // Fully reduce to single digit (or master number), building the chain as we go
        const _giftChain = [giftRaw];
        let _n = giftRaw;
        while (_n > 9 && !masterNums.includes(_n)) {
            _n = String(_n).split('').reduce((s, c) => s + +c, 0);
            _giftChain.push(_n);
        }
        const giftReduced = _n;
        const chainText = _giftChain.length > 1 ? _giftChain.join(' → ') : String(giftRaw);
        _setOrCreate('jyGiftHint', `<span class="jy-num-hint">${chainText}</span>`);
        const giftInfo = NUM_DESC.mulank[giftReduced] || {};
        const giftPersonal = giftInfo.desc
            ? `<strong>${giftRaw} → ${giftReduced} · ${giftInfo.keyword || ''}</strong> · ${giftInfo.planet || ''} · ${giftInfo.desc}`
            : NUM_DESC.gift;
        _setOrCreate('jyGiftDesc', giftPersonal);

        // Render Lottery Numbers
        const lotteryGrid = document.getElementById('lotteryGrid');
        if (lotteryGrid && d.lottery_numbers) {
            const ln = d.lottery_numbers;
            lotteryGrid.innerHTML = `
                <div class="lottery-item-new">
                    <div class="lottery-label-new">${ln.primary.label}</div>
                    <div class="lottery-val-new">${ln.primary.number}</div>
                    <div class="lottery-impact-new">${ln.primary.meaning}</div>
                </div>
                <div class="lottery-item-new">
                    <div class="lottery-label-new">${ln.secondary.label}</div>
                    <div class="lottery-val-new">${ln.secondary.number}</div>
                    <div class="lottery-impact-new">${ln.secondary.meaning}</div>
                </div>
            `;
        }

        renderLoShuGrid(d.lo_shu_grid.grid);
        document.getElementById('jyMissingNums').textContent =
            d.lo_shu_grid.missing.length ? d.lo_shu_grid.missing.join(', ') : 'None';

        const dc = d.driver_conductor_profile;
        if (dc) {
            document.getElementById('jyDcLabel').textContent      = `${d.mulank}~${d.bhagyank}`;
            const pct = dc.compatibility;
            const compatEl = document.getElementById('jyCompatBadge');
            compatEl.textContent = `${pct}% compatible`;
            compatEl.className = `jy-compat-badge ${pct >= 75 ? 'compat-high' : (pct >= 50 ? 'compat-mid' : 'compat-low')}`;
            document.getElementById('jyDcMode').textContent       = dc.mode;
            document.getElementById('jyDcIndustries').textContent = dc.industries.join(' · ');
            document.getElementById('jyDcPros').innerHTML = dc.pros.map(p => `<li>${p}</li>`).join('');
            document.getElementById('jyDcCons').innerHTML = dc.cons.map(c => `<li>${c}</li>`).join('');
            // Add range legend if not already present
            const dcCard = document.getElementById('jyDcMode').closest('.jy-dc-card') || document.getElementById('jyDcMode').parentElement;
            if (dcCard && !dcCard.querySelector('.dc-compat-range')) {
                const range = document.createElement('div');
                range.className = 'dc-compat-range';
                range.textContent = 'Below 50 = tension · 50–75 = workable · 75+ = harmonious';
                compatEl.insertAdjacentElement('afterend', range);
            }
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

    const section    = document.getElementById('forecastSection');
    const yearLabel  = document.getElementById('forecastYearLabel');
    const yearCard   = document.getElementById('forecastYearCard');
    const grid       = document.getElementById('forecastGrid');
    const highlights = document.getElementById('forecastHighlights');
    if (!section || !yearCard || !grid) return;

    if (yearLabel) yearLabel.textContent = currentForecastYear;

    try {
        // Try astrology-enriched endpoint first; fall back to numerology-only
        let d, hasDasha = false;
        const fullRes = await fetch(`/api/forecast/yearly?year=${currentForecastYear}`);
        if (fullRes.ok) {
            d = await fullRes.json();
            hasDasha = Array.isArray(d.dasha_overlay) && d.dasha_overlay.length > 0;
        } else {
            const res = await fetch(`/api/numerology/forecast?birth_date=${birthDate}&year=${currentForecastYear}`);
            if (!res.ok) return;
            d = await res.json();
        }

        const py = d.personal_year;
        const dashaMap = {};
        if (hasDasha) d.dasha_overlay.forEach(o => { dashaMap[o.month] = o; });

        // Year card — with dasha context if available
        const dashaYearSummary = hasDasha ? (() => {
            const lords = [...new Set(d.dasha_overlay.map(o => `${o.md_lord} MD · ${o.ad_lord} Bh`))];
            return `<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(99,91,255,0.15);font-size:12px;color:var(--muted)">
                <span style="font-weight:600;color:var(--accent)">Dasha context</span> · ${lords.join(' → ')}
            </div>`;
        })() : '';

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
                ${dashaYearSummary}
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
            const dasha = dashaMap[m.month];
            const dashaStrip = dasha
                ? `<div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="${dasha.md_lord} MD · ${dasha.ad_lord} Bhukti">${dasha.md_lord} · ${dasha.ad_lord}</div>`
                : '';
            return `<div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px 12px;box-shadow:var(--shadow)${borderHighlight}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                    <div style="font-size:13px;font-weight:700;color:var(--muted)">${m.month_name}</div>
                    ${tag}
                </div>
                <div style="font-size:32px;font-weight:800;color:var(--accent);line-height:1;margin-bottom:6px">${m.personal_month}</div>
                <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:3px">${m.theme}</div>
                <div style="font-size:13px;color:var(--muted)">${m.energy} · ${m.planet}</div>
                ${dashaStrip}
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
    if (_compatProfiles.length) return;
    try {
        const res = await fetch('/api/numerology/profiles');
        if (!res.ok) return;
        _compatProfiles = await res.json();
        const selB = document.getElementById('compatPersonB');
        if (!selB) return;
        
        // Keep the top options
        const topOpts = `
            <option value="ME">Me</option>
            <option value="CUSTOM">+ Add Someone New</option>
            <option value="" disabled>── From Atlas ──</option>
        `;
        const atlasOpts = _compatProfiles.map(p =>
            `<option value="${p.label}">${p.name}</option>`).join('');
        selB.innerHTML = topOpts + atlasOpts;
        if (_compatProfiles.length > 0) selB.selectedIndex = 3; // First atlas person
    } catch (e) { console.error('Compat dropdown error:', e); }
}

function toggleCustomInput(val) {
    const customDiv = document.getElementById('customPersonInput');
    if (customDiv) customDiv.classList.toggle('hidden', val !== 'CUSTOM');
}

async function loadCompatibilityV2() {
    const valB = document.getElementById('compatPersonB')?.value;
    const resultEl = document.getElementById('compatResult');
    if (!valB || !resultEl) return;

    const birthDateA = document.getElementById('date')?.value;
    const nameA = document.getElementById('fullName')?.value.trim();
    const genderA = document.getElementById('gender')?.value || 'Male';

    if (!birthDateA || !nameA) {
        alert("Please enter your details in 'Strategic' view first.");
        return;
    }

    resultEl.innerHTML = '<div style="color:var(--muted);font-size:13px;padding:12px">Calculating energy resonance…</div>';
    resultEl.classList.remove('hidden');

    try {
        let payload = {
            name_a: nameA, dob_a: birthDateA, gender_a: genderA
        };

        if (valB === 'ME') {
            payload.name_b = nameA; payload.dob_b = birthDateA; payload.gender_b = genderA;
        } else if (valB === 'CUSTOM') {
            const nameB = document.getElementById('customName').value.trim();
            const dobB = document.getElementById('customDob').value;
            const genB = document.getElementById('customGender').value;
            if (!nameB || !dobB) { alert("Please enter Name and DOB for Person 2"); return; }
            payload.name_b = nameB; payload.dob_b = dobB; payload.gender_b = genB;
        } else {
            // Label from atlas
            payload.label_b = valB;
        }

        const res = await fetch('/api/numerology/compatibility/v2', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) throw new Error('Failed');
        const d = await res.json();
        const c = d.compatibility;

        const scoreColor = c.score >= 80 ? '#22c55e' : c.score >= 65 ? '#635bff' : c.score >= 50 ? '#f59e0b' : '#ef4444';
        const aName = d.person_a.name;
        const bName = d.person_b.name;

        // Shared resonance pills
        const pills = [];
        if (c.shared?.same_driver)    pills.push(`<span class="resonance-pill">Same Driver · ${c.person_a.driver_planet}</span>`);
        if (c.shared?.same_conductor)  pills.push(`<span class="resonance-pill">Same Conductor · ${c.person_a.conductor_planet}</span>`);
        if (c.shared?.planet_match)   pills.push(`<span class="resonance-pill">Planet Match · ${c.person_a.driver_planet}</span>`);

        resultEl.innerHTML = `
            <div class="card" style="margin-top:16px; border-color:${scoreColor}44">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px">
                    <div>
                        <div style="font-size:18px; font-weight:700; color:var(--text)">${aName} × ${bName}</div>
                        <div style="font-size:13px; color:var(--muted); margin-top:2px">${c.verdict}</div>
                    </div>
                    <div style="font-size:32px; font-weight:800; color:${scoreColor}">${c.score}%</div>
                </div>
                
                <div class="resonance-pills" style="margin-bottom:16px">${pills.join('')}</div>
                
                <div class="compat-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:16px">
                    <div class="compat-mini-card">
                        <div class="mini-label">${aName}</div>
                        <div style="font-size:14px; font-weight:700">Driver ${d.person_a.mulank} · Conductor ${d.person_a.bhagyank}</div>
                        <div style="font-size:11px; color:var(--muted)">${d.person_a.driver_planet} energy</div>
                    </div>
                    <div class="compat-mini-card">
                        <div class="mini-label">${bName}</div>
                        <div style="font-size:14px; font-weight:700">Driver ${d.person_b.mulank} · Conductor ${d.person_b.bhagyank}</div>
                        <div style="font-size:11px; color:var(--muted)">${d.person_b.driver_planet} energy</div>
                    </div>
                </div>

                <div style="margin-top:16px; padding-top:16px; border-top:1px solid var(--border); font-size:13px; line-height:1.6; color:var(--text)">
                    ${d.interpretation || 'This combination suggests a unique energetic resonance. Focus on shared goals and clear communication.'}
                </div>

                <div style="margin-top:14px; padding-top:14px; border-top:1px solid var(--border)">
                    <div style="font-size:11px;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Why this score?</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                        <div style="background:var(--surface);border-radius:10px;padding:10px;border:1px solid var(--border)">
                            <div style="font-size:11px;color:var(--muted);margin-bottom:4px">${aName} leads · ${c.dynamics?.a_leads_b?.score ?? '—'}/100</div>
                            ${(c.dynamics?.a_leads_b?.pros || []).map(p => `<div style="font-size:12px;color:#22c55e;line-height:1.4">+ ${p}</div>`).join('')}
                            ${(c.dynamics?.a_leads_b?.cons || []).map(p => `<div style="font-size:12px;color:#ef4444;line-height:1.4">− ${p}</div>`).join('')}
                        </div>
                        <div style="background:var(--surface);border-radius:10px;padding:10px;border:1px solid var(--border)">
                            <div style="font-size:11px;color:var(--muted);margin-bottom:4px">${bName} leads · ${c.dynamics?.b_leads_a?.score ?? '—'}/100</div>
                            ${(c.dynamics?.b_leads_a?.pros || []).map(p => `<div style="font-size:12px;color:#22c55e;line-height:1.4">+ ${p}</div>`).join('')}
                            ${(c.dynamics?.b_leads_a?.cons || []).map(p => `<div style="font-size:12px;color:#ef4444;line-height:1.4">− ${p}</div>`).join('')}
                        </div>
                    </div>
                    <div style="font-size:12px;color:var(--muted);margin-top:8px">${c.summary || ''}</div>
                </div>
            </div>`;
    } catch (e) {
        console.error('Compat error:', e);
        resultEl.innerHTML = '<div style="color:var(--muted);font-size:13px;padding:12px">Failed to calculate compatibility.</div>';
    }
}
