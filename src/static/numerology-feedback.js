// Numerology and Feedback Functions for Jyotish Engine Core

// Chaldean Numerology Values
const chaldeanValues = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
};

// Interpretations for numbers 1-9
const lifePathInterpretations = {
    1: "You are a natural leader with strong independence and determination. You have the potential to achieve great things through your initiative and pioneering spirit.",
    2: "You are cooperative and diplomatic, with a talent for bringing people together. You thrive in partnerships and value harmony in relationships.",
    3: "You are creative and expressive, with a gift for communication and inspiration. Your optimistic nature and artistic abilities make you a joy to be around.",
    4: "You are practical and reliable, with a strong sense of discipline and organization. You build solid foundations and value hard work and stability.",
    5: "You are a free spirit with a natural curiosity and desire for adventure. Change and variety are essential to your well-being and personal growth.",
    6: "You are nurturing and responsible, with a deep concern for others. You excel in roles that involve care, teaching, or service to your community.",
    7: "You are analytical and introspective, with a thirst for knowledge and understanding. You seek deeper meaning and often prefer solitude for contemplation.",
    8: "You are ambitious and authoritative, with strong business acumen and leadership abilities. You have the potential for material success and achievement.",
    9: "You are compassionate and humanitarian, with a desire to help others. Your idealism and generosity make you a force for positive change in the world."
};

const expressionInterpretations = {
    1: "Your expression number reveals your potential for leadership and independence. You communicate with confidence and have the ability to inspire others to action.",
    2: "Your expression number shows your diplomatic nature and ability to mediate. You express yourself through cooperation and creating harmony in relationships.",
    3: "Your expression number highlights your creative and communicative talents. You have a natural ability to inspire, entertain, and bring joy through your words and ideas.",
    4: "Your expression number indicates your practical and organized approach. You express yourself through building structures and systems that provide stability.",
    5: "Your expression number reflects your adventurous and versatile nature. You communicate with freedom and variety, often bringing excitement to conversations.",
    6: "Your expression number shows your nurturing and responsible character. You express care and concern for others, often taking on supportive roles.",
    7: "Your expression number reveals your analytical and thoughtful communication. You prefer deep, meaningful discussions and value intellectual stimulation.",
    8: "Your expression number demonstrates your authoritative and ambitious style. You communicate with confidence and have strong organizational abilities.",
    9: "Your expression number highlights your compassionate and humanitarian outlook. You express yourself through helping others and promoting positive change."
};

const soulUrgeInterpretations = {
    1: "Your soul urges you toward independence and leadership. Deep down, you crave the freedom to pioneer and create your own path in life.",
    2: "Your soul seeks harmony and partnership. You are driven by a desire for cooperation and meaningful connections with others.",
    3: "Your soul craves creative expression and joy. You are motivated by the need to communicate, create, and bring happiness to yourself and others.",
    4: "Your soul desires stability and structure. You are driven by the need for order, security, and tangible results in your life.",
    5: "Your soul yearns for freedom and adventure. You are motivated by change, variety, and the exploration of new experiences.",
    6: "Your soul seeks to nurture and care for others. You are driven by love, responsibility, and service to your family and community.",
    7: "Your soul craves knowledge and understanding. You are motivated by the pursuit of truth, wisdom, and deeper spiritual insights.",
    8: "Your soul desires material success and authority. You are driven by ambition, achievement, and the ability to manifest abundance.",
    9: "Your soul urges you toward compassion and service. You are motivated by helping others and contributing to the greater good of humanity."
};

const personalityInterpretations = {
    1: "You appear independent and self-reliant to others. People see you as a leader who takes initiative and charts your own course.",
    2: "You appear diplomatic and cooperative to others. People see you as someone who values harmony and works well in partnerships.",
    3: "You appear creative and expressive to others. People see you as artistic, communicative, and full of enthusiasm and optimism.",
    4: "You appear practical and reliable to others. People see you as disciplined, organized, and someone they can depend on.",
    5: "You appear adventurous and versatile to others. People see you as a free spirit who embraces change and new experiences.",
    6: "You appear nurturing and responsible to others. People see you as caring, supportive, and someone who puts others' needs first.",
    7: "You appear analytical and introspective to others. People see you as thoughtful, knowledgeable, and somewhat reserved.",
    8: "You appear ambitious and authoritative to others. People see you as confident, successful, and someone who gets things done.",
    9: "You appear compassionate and idealistic to others. People see you as generous, humanitarian, and concerned with social issues."
};

// Helper function to reduce a number to single digit
function reduceNumber(num) {
    while (num > 9) {
        num = num.toString().split('').reduce((sum, digit) => sum + parseInt(digit), 0);
    }
    return num;
}

// Calculate Life Path Number from birth date
function calculateLifePath(birthDate) {
    let sum = 0;
    for (let char of birthDate.replace(/-/g, '')) {
        if (char >= '0' && char <= '9') {
            sum += parseInt(char);
        }
    }
    return reduceNumber(sum);
}

// Calculate Expression Number from full name
function calculateExpression(fullName) {
    const letters = fullName.toUpperCase().replace(/[^A-Z]/g, '');
    let sum = 0;
    for (let char of letters) {
        sum += chaldeanValues[char] || 0;
    }
    return reduceNumber(sum);
}

// Calculate Soul Urge Number from vowels in name
function calculateSoulUrge(fullName) {
    const letters = fullName.toUpperCase().replace(/[^A-Z]/g, '');
    let sum = 0;
    for (let char of letters) {
        if (['A', 'E', 'I', 'O', 'U'].includes(char)) {
            sum += chaldeanValues[char] || 0;
        }
    }
    return reduceNumber(sum);
}

// Calculate Personality Number from consonants in name
function calculatePersonality(fullName) {
    const letters = fullName.toUpperCase().replace(/[^A-Z]/g, '');
    let sum = 0;
    for (let char of letters) {
        if (!['A', 'E', 'I', 'O', 'U'].includes(char)) {
            sum += chaldeanValues[char] || 0;
        }
    }
    return reduceNumber(sum);
}

// Calculate compatibility score based on numbers
function calculateCompatibility(lifePath, expression, soulUrge, personality) {
    // Calculate harmony score based on differences between numbers
    const differences = [
        Math.abs(lifePath - expression),
        Math.abs(lifePath - soulUrge),
        Math.abs(lifePath - personality),
        Math.abs(expression - soulUrge),
        Math.abs(expression - personality),
        Math.abs(soulUrge - personality)
    ];
    
    const avgDifference = differences.reduce((sum, diff) => sum + diff, 0) / differences.length;
    const score = Math.max(0, 100 - avgDifference * 10);
    
    let level;
    if (score >= 90) level = "Excellent";
    else if (score >= 80) level = "Very Good";
    else if (score >= 70) level = "Good";
    else if (score >= 60) level = "Fair";
    else level = "Challenging";
    
    return { score: Math.round(score), level };
}

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

    if (!birthDate || !fullName) return;
    // Also load personal cycles
    loadPersonalCycles(birthDate);
    // Populate compatibility dropdowns
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

async function loadJyotishProfile() {
    const label = document.getElementById('jyProfileSelect').value;
    if (!label) { alert('Please select a person first.'); return; }

    try {
        const res = await fetch(`/api/numerology/profile/${encodeURIComponent(label)}`);
        if (!res.ok) throw new Error('Profile not found');
        const d = await res.json();

        document.getElementById('jyName').textContent = d.name;
        document.getElementById('jyMeta').textContent = `${d.gender} · DOB ${d.dob}`;
        document.getElementById('jyMulank').textContent = d.mulank;
        document.getElementById('jyBhagyank').textContent = d.bhagyank;
        document.getElementById('jyGift').textContent = d.gift_number;
        document.getElementById('jyKua').textContent = d.kua_number;
        document.getElementById('jyNamank').textContent = d.namank;

        // Lo Shu Grid
        renderLoShuGrid(d.lo_shu_grid.grid);
        document.getElementById('jyMissingNums').textContent =
            d.lo_shu_grid.missing.length ? d.lo_shu_grid.missing.join(', ') : 'None';

        // DC Profile
        const dc = d.driver_conductor_profile;
        document.getElementById('jyDcLabel').textContent = `${d.mulank}~${d.bhagyank}`;
        document.getElementById('jyCompatBadge').textContent = `${dc.compatibility}% compatible`;
        document.getElementById('jyDcMode').textContent = dc.mode;
        document.getElementById('jyDcIndustries').textContent = dc.industries.join(' · ');
        document.getElementById('jyDcPros').innerHTML = dc.pros.map(p => `<li>${p}</li>`).join('');
        document.getElementById('jyDcCons').innerHTML = dc.cons.map(c => `<li>${c}</li>`).join('');

        // Missing number remedies
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

        document.getElementById('jyProfilePanel').classList.remove('hidden');
    } catch (e) {
        alert('Could not load profile: ' + e.message);
    }
}

// ── Numerology Functions ──────────────────────────────────────

async function calculateNumerology() {
    const birthDate = document.getElementById('date').value;
    const fullName = document.getElementById('fullName').value;

    if (!birthDate || !fullName) {
        alert('Please provide both birth date and full name');
        return;
    }

    try {
        // Calculate Chaldean numerology numbers
        const lifePathNumber = calculateLifePath(birthDate);
        const expressionNumber = calculateExpression(fullName);
        const soulUrgeNumber = calculateSoulUrge(fullName);
        const personalityNumber = calculatePersonality(fullName);
        const compatibility = calculateCompatibility(lifePathNumber, expressionNumber, soulUrgeNumber, personalityNumber);

        const data = {
            life_path: {
                life_path_number: lifePathNumber,
                interpretation: lifePathInterpretations[lifePathNumber] || "Your life path reveals unique potential and purpose."
            },
            expression: {
                expression_number: expressionNumber,
                interpretation: expressionInterpretations[expressionNumber] || "Your expression shows your natural talents and abilities."
            },
            soul_urge: {
                soul_urge_number: soulUrgeNumber,
                interpretation: soulUrgeInterpretations[soulUrgeNumber] || "Your soul urge reveals your deepest desires and motivations."
            },
            personality: {
                personality_number: personalityNumber,
                interpretation: personalityInterpretations[personalityNumber] || "Your personality reflects how others perceive you."
            },
            compatibility: compatibility,
            summary: `Your numerology reveals a ${compatibility.level.toLowerCase()} balance of energies. Life Path ${lifePathNumber} guides your journey, Expression ${expressionNumber} shows your talents, Soul Urge ${soulUrgeNumber} reveals your inner desires, and Personality ${personalityNumber} is how you appear to others.`
        };

        // Display results
        document.getElementById('lifePathNumber').textContent = data.life_path.life_path_number;
        document.getElementById('lifePathInterpretation').textContent = data.life_path.interpretation;

        document.getElementById('expressionNumber').textContent = data.expression.expression_number;
        document.getElementById('expressionInterpretation').textContent = data.expression.interpretation;

        document.getElementById('soulUrgeNumber').textContent = data.soul_urge.soul_urge_number;
        document.getElementById('soulUrgeInterpretation').textContent = data.soul_urge.interpretation;

        document.getElementById('personalityNumber').textContent = data.personality.personality_number;
        document.getElementById('personalityInterpretation').textContent = data.personality.interpretation;

        document.getElementById('compatibilityScore').textContent = data.compatibility.score + '/100';
        document.getElementById('compatibilityLevel').textContent = data.compatibility.level;

        document.getElementById('numerologySummary').textContent = data.summary;

        // Show numerology section
        document.getElementById('numerologySection').classList.remove('hidden');

    } catch (error) {
        console.error('Numerology calculation error:', error);
        alert('Failed to calculate numerology. Please try again.');
    }
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
        // Mock success for static demo
        const result = { success: true };

        const statusDiv = document.getElementById('feedbackStatus');
        if (result.success) {
            statusDiv.textContent = '✅ Thank you! Your feedback has been submitted and categorized.';
            statusDiv.className = 'feedback-status success';
            statusDiv.classList.remove('hidden');

            // Reset form after successful submission
            setTimeout(() => {
                toggleFeedback();
            }, 2000);
        } else {
            statusDiv.textContent = '❌ Failed to submit feedback: ' + (result.message || 'Unknown error');
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
