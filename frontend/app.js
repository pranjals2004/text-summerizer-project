const state = {
    apiKey: sessionStorage.getItem('gemini_api_key') || '',
    currentArticleText: '',
    currentArticleTitle: '',
    selectedDemoId: 'tech',
    chatHistory: [],
    nlpStats: null,
    analysisResults: null,
    isCustomMode: false
};

const DEMO_TITLES = {
    tech: "AI Evolution: Quantum-Neural System Breaks Turing Threshold in Logical Reasoning",
    space: "NASA's Lunar Explorer Confirms Vast Subsurface Water Ice on Moon's South Pole",
    business: "Global Renewable Energy Production Overtakes Coal for First Time in History",
    science: "Deep-Ocean Expedition Discovers 50 New Species Near Mariana Trench"
};

const elements = {
    modeBadge: document.getElementById('mode-badge'),
    toggleSettingsBtn: document.getElementById('toggle-settings-btn'),
    settingsPanel: document.getElementById('settings-panel'),
    apiKeyInput: document.getElementById('api-key-input'),
    saveKeyBtn: document.getElementById('save-key-btn'),
    
    demoCards: document.querySelectorAll('.demo-card'),
    articleTitleInput: document.getElementById('article-title-input'),
    articleTextInput: document.getElementById('article-text-input'),
    charCountBadge: document.getElementById('char-count-badge'),
    wordCountBadge: document.getElementById('word-count-badge'),
    
    resetBtn: document.getElementById('reset-btn'),
    analyzeBtn: document.getElementById('analyze-btn'),
    
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    loadingOverlay: document.getElementById('loading-overlay'),
    
    summaryText: document.getElementById('summary-text'),
    gaugeFill: document.getElementById('gauge-fill'),
    sentimentScoreNum: document.getElementById('sentiment-score-num'),
    sentimentLabelText: document.getElementById('sentiment-label-text'),
    emotionJoy: document.getElementById('emotion-joy'),
    emotionJoyVal: document.getElementById('emotion-joy-val'),
    emotionTrust: document.getElementById('emotion-trust'),
    emotionTrustVal: document.getElementById('emotion-trust-val'),
    emotionFear: document.getElementById('emotion-fear'),
    emotionFearVal: document.getElementById('emotion-fear-val'),
    emotionAnger: document.getElementById('emotion-anger'),
    emotionAngerVal: document.getElementById('emotion-anger-val'),
    emotionSadness: document.getElementById('emotion-sadness'),
    emotionSadnessVal: document.getElementById('emotion-sadness-val'),
    sentimentExplanationText: document.getElementById('sentiment-explanation-text'),
    
    statChars: document.getElementById('stat-chars'),
    statWords: document.getElementById('stat-words'),
    statSentences: document.getElementById('stat-sentences'),
    statDiversity: document.getElementById('stat-diversity'),
    posChartContainer: document.getElementById('pos-chart-container'),
    readabilityScore: document.getElementById('readability-score'),
    readabilityProgress: document.getElementById('readability-progress'),
    readabilityGrade: document.getElementById('readability-grade'),
    tokensList: document.getElementById('tokens-list'),
    
    entitiesContainer: document.getElementById('entities-container'),
    keywordsCloud: document.getElementById('keywords-cloud'),
    
    chatMessages: document.getElementById('chat-messages'),
    chatInput: document.getElementById('chat-input'),
    chatSendBtn: document.getElementById('chat-send-btn')
};

document.addEventListener('DOMContentLoaded', () => {
    initSettings();
    initArticleInput();
    initTabs();
    initChat();
    loadDemoArticle('tech');
});

function initSettings() {
    if (state.apiKey) {
        elements.apiKeyInput.value = state.apiKey;
        updateModeBadge(true);
    } else {
        updateModeBadge(false);
    }

    elements.toggleSettingsBtn.addEventListener('click', () => {
        elements.settingsPanel.classList.toggle('hidden');
    });

    elements.saveKeyBtn.addEventListener('click', () => {
        const key = elements.apiKeyInput.value.trim();
        state.apiKey = key;
        sessionStorage.setItem('gemini_api_key', key);
        updateModeBadge(!!key);
        elements.settingsPanel.classList.add('hidden');
        showToast(key ? "API Key saved! Ready for Live AI Mode." : "API Key cleared. Switched to Local NLP Mode.");
    });
}

function updateModeBadge(hasKey) {
    if (hasKey) {
        elements.modeBadge.className = 'mode-badge ai-mode';
        elements.modeBadge.querySelector('.mode-label').textContent = 'Live AI Mode';
    } else {
        elements.modeBadge.className = 'mode-badge local-mode';
        elements.modeBadge.querySelector('.mode-label').textContent = 'Local NLP Mode';
    }
}

function initTabs() {
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            elements.tabBtns.forEach(b => b.classList.remove('active'));
            elements.tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

function initArticleInput() {
    elements.articleTextInput.addEventListener('input', () => {
        state.isCustomMode = true;
        state.selectedDemoId = null;
        elements.demoCards.forEach(c => c.classList.remove('active'));
        updateCounters();
    });

    elements.articleTitleInput.addEventListener('input', () => {
        state.isCustomMode = true;
        state.selectedDemoId = null;
        elements.demoCards.forEach(c => c.classList.remove('active'));
    });

    elements.demoCards.forEach(card => {
        card.addEventListener('click', () => {
            const demoId = card.getAttribute('data-id');
            loadDemoArticle(demoId);
        });
    });

    elements.resetBtn.addEventListener('click', () => {
        elements.articleTitleInput.value = '';
        elements.articleTextInput.value = '';
        state.isCustomMode = true;
        state.selectedDemoId = null;
        elements.demoCards.forEach(c => c.classList.remove('active'));
        updateCounters();
        elements.articleTitleInput.focus();
    });

    elements.analyzeBtn.addEventListener('click', () => {
        runPipeline();
    });
}

function updateCounters() {
    const text = elements.articleTextInput.value;
    const charCount = text.length;
    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    elements.charCountBadge.textContent = `${charCount} characters`;
    elements.wordCountBadge.textContent = `${wordCount} words`;
}

async function loadDemoArticle(demoId) {
    state.isCustomMode = false;
    state.selectedDemoId = demoId;
    
    elements.demoCards.forEach(c => {
        if (c.getAttribute('data-id') === demoId) {
            c.classList.add('active');
        } else {
            c.classList.remove('active');
        }
    });

    toggleLoading(true);
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: '', demoId: demoId })
        });
        const data = await response.json();
        
        let textVal = "";
        if (demoId === 'tech') {
            textVal = "A consortium of researchers from MIT and Google DeepMind has announced a breakthrough in artificial intelligence. They developed a 'Quantum-Neural' hybrid network that successfully passed a new suite of complex logical reasoning tests, dubbed the 'Turing Threshold'. Unlike traditional large language models which rely on statistical pattern matching, this hybrid architecture uses quantum-inspired bits to solve abstract mathematical proofs and multi-step logic problems with 99.8% accuracy. Dr. Helena Vance, leading the research at MIT, stated that this marks the transition from simple semantic prediction to genuine cognitive reasoning. The research team plans to open-source the model weights next month for academic collaborators. Tech giants have already expressed interest, with Microsoft reportedly bidding for an exclusive commercial license.";
        } else if (demoId === 'space') {
            textVal = "NASA's VIPER lunar explorer has successfully mapped a massive underground deposit of water ice in the Shackleton Crater at the Moon's South Pole. Data transmitted from the rover indicates the ice sheet is located just 1.5 meters beneath the surface and spans over 150 square kilometers. The discovery is a major triumph for the Artemis Program, which aims to establish a sustainable human presence on the Moon. Project Director Marcus Thorne confirmed that this ice can be harvested to produce drinking water, breathable oxygen, and liquid hydrogen rocket fuel. This eliminates the need to transport water from Earth, slashing mission costs by billions. However, international space agencies are already raising concerns about lunar resource rights under the Outer Space Treaty, prompting calls for an urgent diplomatic summit.";
        } else if (demoId === 'business') {
            textVal = "In a historic milestone for the global climate transition, renewable energy sources—primarily solar, wind, and hydro—generated more electricity than coal globally in the last fiscal year. According to the International Energy Agency (IEA) annual report, renewables accounted for 31.5% of total power generation, compared to coal's 30.2%. This transition was accelerated by massive solar installations in China, a wind surge in Europe, and tax incentives in the United States. IEA Director Fatih Birol called it an irreversible turning point for the power sector. Despite the positive news, energy analysts warn that grid infrastructure is struggling to keep pace with this green surge, leading to frequent curtailment where clean power is wasted because transmission lines cannot support the load. Furthermore, coal-dependent communities are facing severe job losses, sparking protests in several regions.";
        } else if (demoId === 'science') {
            textVal = "A research expedition led by the Schmidt Ocean Institute has returned from a 30-day mission near the Mariana Trench with findings that have shocked the scientific community. Utilizing the robotic underwater vehicle 'SuBastian', scientists mapped previously unexplored hydrothermal vent fields and discovered at least 50 new marine species. Among the discoveries is a glowing bioluminescent jellyfish with fractal-like tentacles and an unusual species of 'ghost crab' that feeds on sulfur-eating bacteria. Dr. Jyotika Virmani, the expedition's chief scientist, stated that these findings reveal how little we understand about deep-ocean ecosystems. However, researchers noted with alarm that microplastic fibers were recovered in water samples taken at depths of 8,000 meters. This discovery proves that human pollution has penetrated even the deepest and most remote ecosystems on the planet.";
        }
        
        elements.articleTitleInput.value = DEMO_TITLES[demoId];
        elements.articleTextInput.value = textVal;
        updateCounters();
        
        const preRes = await fetch('/api/preprocess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textVal })
        });
        const preData = await preRes.json();
        
        state.nlpStats = preData;
        state.analysisResults = data;
        
        renderResults();
        resetChat();
        
    } catch (e) {
        console.error(e);
        showToast("Error loading demo article.");
    } finally {
        toggleLoading(false);
    }
}

async function runPipeline() {
    const text = elements.articleTextInput.value.trim();
    if (!text) {
        showToast("Please enter article text to analyze.");
        return;
    }
    
    toggleLoading(true);
    try {
        const preResponse = await fetch('/api/preprocess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        if (!preResponse.ok) throw new Error("Preprocessing failed.");
        const preData = await preResponse.json();
        state.nlpStats = preData;

        const analysisResponse = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                apiKey: state.apiKey,
                demoId: state.selectedDemoId
            })
        });
        if (!analysisResponse.ok) throw new Error("Analysis failed.");
        const analysisData = await analysisResponse.json();
        state.analysisResults = analysisData;
        
        renderResults();
        resetChat();
        
        elements.tabBtns[0].click();
        
        if (analysisData.warning) {
            showToast(analysisData.warning);
        } else {
            showToast("Intelligence pipeline executed successfully!");
        }
    } catch (err) {
        console.error(err);
        showToast(`Pipeline execution failed: ${err.message}`);
    } finally {
        toggleLoading(false);
    }
}

function renderResults() {
    const stats = state.nlpStats;
    const analysis = state.analysisResults;
    
    if (!stats || !analysis) return;

    elements.summaryText.textContent = analysis.summary;
    if (analysis.warning) {
        const warningBox = document.createElement('div');
        warningBox.className = 'local-warning';
        warningBox.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> <span>${analysis.warning}</span>`;
        elements.summaryText.appendChild(warningBox);
    }

    const score = analysis.sentiment.score;
    const label = analysis.sentiment.label;
    elements.sentimentScoreNum.textContent = `${score}%`;
    elements.sentimentLabelText.textContent = label;
    
    elements.sentimentLabelText.className = label.toLowerCase();
    
    const circumference = 251.2;
    const offset = circumference - (circumference * score) / 100;
    elements.gaugeFill.style.strokeDashoffset = offset;
    elements.gaugeFill.className = `gauge-fill ${label.toLowerCase()}`;

    const emotions = analysis.sentiment.emotions;
    animateProgress(elements.emotionJoy, elements.emotionJoyVal, emotions.Joy || 0);
    animateProgress(elements.emotionTrust, elements.emotionTrustVal, emotions.Trust || 0);
    animateProgress(elements.emotionFear, elements.emotionFearVal, emotions.Fear || 0);
    animateProgress(elements.emotionAnger, elements.emotionAngerVal, emotions.Anger || 0);
    animateProgress(elements.emotionSadness, elements.emotionSadnessVal, emotions.Sadness || 0);

    elements.sentimentExplanationText.textContent = analysis.sentiment.explanation || "No explanation provided.";

    elements.statChars.textContent = formatNumber(stats.char_count);
    elements.statWords.textContent = formatNumber(stats.word_count);
    elements.statSentences.textContent = formatNumber(stats.sentence_count);
    elements.statDiversity.textContent = `${stats.lexical_diversity}%`;

    elements.posChartContainer.innerHTML = '';
    const pos = stats.pos_distribution;
    const totalPos = Object.values(pos).reduce((a, b) => a + b, 0);
    
    const sortedPos = Object.entries(pos).sort((a, b) => b[1] - a[1]);
    sortedPos.forEach(([tag, count]) => {
        if (count === 0 && totalPos > 0) return;
        const pct = totalPos > 0 ? ((count / totalPos) * 100).toFixed(1) : 0;
        
        const row = document.createElement('div');
        row.className = 'pos-bar-row';
        row.innerHTML = `
            <span class="pos-bar-label">${tag}</span>
            <div class="pos-bar-track">
                <div class="pos-bar-fill" style="width: 0%"></div>
            </div>
            <span class="pos-bar-count">${count} (${pct}%)</span>
        `;
        elements.posChartContainer.appendChild(row);
        
        setTimeout(() => {
            row.querySelector('.pos-bar-fill').style.width = `${pct}%`;
        }, 100);
    });

    elements.readabilityScore.textContent = stats.readability_score;
    elements.readabilityProgress.style.width = `${stats.readability_score}%`;
    elements.readabilityGrade.textContent = stats.readability_grade;

    elements.tokensList.innerHTML = '';
    if (stats.filtered_tokens && stats.filtered_tokens.length > 0) {
        stats.filtered_tokens.forEach(tok => {
            const span = document.createElement('span');
            span.className = 'token-tag';
            span.textContent = tok;
            elements.tokensList.appendChild(span);
        });
    } else {
        elements.tokensList.innerHTML = `<span class="placeholder-text">No tokens available.</span>`;
    }

    elements.entitiesContainer.innerHTML = '';
    if (analysis.entities && analysis.entities.length > 0) {
        analysis.entities.forEach(ent => {
            const div = document.createElement('div');
            div.className = 'entity-row';
            div.innerHTML = `
                <div class="entity-meta">
                    <span class="entity-name">${ent.name}</span>
                    <span class="entity-type-badge ${ent.type.toLowerCase()}">${ent.type}</span>
                </div>
                <span class="entity-relevance">${ent.relevance}</span>
            `;
            elements.entitiesContainer.appendChild(div);
        });
    } else {
        elements.entitiesContainer.innerHTML = `<p class="placeholder-text">No entities extracted.</p>`;
    }

    elements.keywordsCloud.innerHTML = '';
    if (stats.word_frequencies && stats.word_frequencies.length > 0) {
        const maxCount = stats.word_frequencies[0].count;
        stats.word_frequencies.forEach(item => {
            const fontScale = maxCount > 1 ? 0.85 + (item.count / maxCount) * 0.5 : 1.0;
            const badge = document.createElement('span');
            badge.className = 'keyword-badge';
            badge.style.transform = `scale(${fontScale})`;
            badge.style.margin = '2px';
            badge.innerHTML = `
                ${item.word}
                <span class="keyword-count">${item.count}</span>
            `;
            elements.keywordsCloud.appendChild(badge);
        });
    } else {
        elements.keywordsCloud.innerHTML = `<p class="placeholder-text">No keywords extracted.</p>`;
    }
}

function initChat() {
    elements.chatSendBtn.addEventListener('click', sendChatMessage);
    elements.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
}

function resetChat() {
    state.chatHistory = [];
    elements.chatMessages.innerHTML = `
        <div class="message system-msg">
            <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-content">
                <p>Hello! I have loaded the article. Ask me any questions about its details, quotes, or implications.</p>
            </div>
        </div>
    `;
    elements.chatInput.disabled = false;
    elements.chatSendBtn.disabled = false;
}

async function sendChatMessage() {
    const text = elements.articleTextInput.value.trim();
    const query = elements.chatInput.value.trim();
    if (!query) return;

    appendMessage("user", query);
    elements.chatInput.value = '';
    elements.chatInput.disabled = true;
    elements.chatSendBtn.disabled = true;

    const loadingMsgId = appendMessage("system", "Thinking...");

    try {
        const response = await fetch('/api/qa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                question: query,
                chatHistory: state.chatHistory,
                apiKey: state.apiKey,
                demoId: state.selectedDemoId
            })
        });
        
        const data = await response.json();
        
        const loadingEl = document.getElementById(loadingMsgId);
        if (loadingEl) loadingEl.remove();
        
        appendMessage("system", data.answer);
        
        state.chatHistory.push({ role: 'user', content: query });
        state.chatHistory.push({ role: 'model', content: data.answer });
        
    } catch (err) {
        console.error(err);
        const loadingEl = document.getElementById(loadingMsgId);
        if (loadingEl) loadingEl.remove();
        appendMessage("system", "Failed to get response. Please check network connection or verify API Key.");
    } finally {
        elements.chatInput.disabled = false;
        elements.chatSendBtn.disabled = false;
        elements.chatInput.focus();
    }
}

function appendMessage(role, content) {
    const msgId = `msg-${Date.now()}`;
    const div = document.createElement('div');
    div.id = msgId;
    div.className = `message ${role === 'user' ? 'user-msg' : 'system-msg'}`;
    
    const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
    div.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid ${avatarIcon}"></i></div>
        <div class="msg-content">
            <p>${content}</p>
        </div>
    `;
    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    
    return msgId;
}

function toggleLoading(isLoading) {
    if (isLoading) {
        elements.loadingOverlay.classList.remove('hidden');
        elements.analyzeBtn.disabled = true;
    } else {
        elements.loadingOverlay.classList.add('hidden');
        elements.analyzeBtn.disabled = false;
    }
}

function animateProgress(barEl, valEl, targetVal) {
    barEl.style.width = '0%';
    valEl.textContent = '0%';
    setTimeout(() => {
        barEl.style.width = `${targetVal}%`;
        valEl.textContent = `${targetVal}%`;
    }, 100);
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.style.position = 'fixed';
    toast.style.bottom = '2rem';
    toast.style.right = '2rem';
    toast.style.background = 'rgba(16, 22, 38, 0.95)';
    toast.style.border = '1px solid var(--accent-indigo)';
    toast.style.boxShadow = '0 0 15px rgba(99, 102, 241, 0.3)';
    toast.style.color = '#fff';
    toast.style.padding = '0.75rem 1.5rem';
    toast.style.borderRadius = '8px';
    toast.style.zIndex = '1000';
    toast.style.fontFamily = 'var(--font-header)';
    toast.style.fontSize = '0.85rem';
    toast.style.animation = 'fadeIn 0.3s ease-out';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
