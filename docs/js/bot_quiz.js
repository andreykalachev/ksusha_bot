// Telegram WebApp
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.expand();
}

// State
let quizData = null;
let currentQuestionIndex = 0;
let scores = {};
let lang = 'ru';

// DOM Elements
const app = document.getElementById('app');
const loadingScreen = document.getElementById('loading');
const mainPage = document.getElementById('main-page');
const questionPage = document.getElementById('question-page');
const resultPage = document.getElementById('result-page');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    // Get language from URL
    const urlParams = new URLSearchParams(window.location.search);
    lang = urlParams.get('lang') || 'ru';
    
    // Load Data
    try {
        const response = await fetch(`data/quiz.${lang}.yaml`);
        if (!response.ok) throw new Error('Failed to load quiz data');
        const yamlText = await response.text();
        quizData = jsyaml.load(yamlText);
        
        // Initialize scores
        if (quizData.results) {
            quizData.results.forEach(r => scores[r.id] = 0);
        }

        showMainPage();
    } catch (error) {
        console.error(error);
        alert('Error loading quiz. Please try again.');
    }
});

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
    window.scrollTo(0, 0);
}

function showMainPage() {
    const { title, description, image, button } = quizData.main_page;
    
    mainPage.innerHTML = `
        <img src="assets/quiz/${image}" class="hero-image-original" alt="${title}">
        <h1>${title}</h1>
        <p>${description}</p>
        <button class="btn" onclick="startQuiz()">${button}</button>
    `;
    
    showScreen('main-page');
}

function startQuiz() {
    currentQuestionIndex = 0;
    // Reset scores
    Object.keys(scores).forEach(key => scores[key] = 0);
    showQuestion();
}

function showQuestion() {
    const question = quizData.questions[currentQuestionIndex];
    const totalQuestions = quizData.questions.length;
    const progress = ((currentQuestionIndex) / totalQuestions) * 100;

    let answersHtml = '';
    question.answers.forEach((answer, index) => {
        answersHtml += `
            <div class="answer-card" onclick="handleAnswer(${index})">
                <img src="assets/quiz/${answer.image}" class="answer-image" loading="lazy">
                <div class="answer-text">${answer.text}</div>
            </div>
        `;
    });

    questionPage.innerHTML = `
        <div class="progress-container">
            <div class="progress-bar" style="width: ${progress}%"></div>
        </div>
        <h1>${question.text}</h1>
        <div class="answers-grid">
            ${answersHtml}
        </div>
    `;

    showScreen('question-page');
}

function handleAnswer(answerIndex) {
    const question = quizData.questions[currentQuestionIndex];
    const answer = question.answers[answerIndex];
    
    // Update scores
    if (answer.weights) {
        for (const [key, value] of Object.entries(answer.weights)) {
            // Handle string values like "+3" if present, though YAML has numbers
            const weight = parseInt(value); 
            if (!isNaN(weight)) {
                if (!scores[key]) scores[key] = 0;
                scores[key] += weight;
            }
        }
    }

    currentQuestionIndex++;
    
    if (currentQuestionIndex < quizData.questions.length) {
        showQuestion();
    } else {
        showResult();
    }
}

function showResult() {
    // Calculate winner
    let maxScore = -Infinity;
    let winnerId = null;
    
    for (const [id, score] of Object.entries(scores)) {
        if (score > maxScore) {
            maxScore = score;
            winnerId = id;
        }
    }
    
    const result = quizData.results.find(r => r.id === winnerId);
    
    if (!result) {
        alert('Error calculating result');
        return;
    }

    let closeText = lang === 'ru' ? "Закрыть" : "Close";

    // Determine colors
    let resultColor = result.color || 'var(--button-color)';
    if (tg && tg.colorScheme === 'dark' && result.color_dark) {
        resultColor = result.color_dark;
    }

    resultPage.innerHTML = `
        <img src="assets/quiz/${result.image}" class="hero-image" alt="${result.title}">
        <h1 class="result-title" style="color: ${resultColor}">${result.title}</h1>
        <div class="result-comment" style="border-left-color: ${resultColor}">
            <p class="result-summary" style="font-style: italic; font-weight: bold; margin-bottom: 10px; color: ${resultColor};">${result.short_summary}</p>
            <p class="result-description" style="white-space: pre-wrap; font-style: normal; color: ${resultColor};">${result.description}</p>
        </div>
        <div class="final-words">
            <p>${quizData.final_words}</p>
        </div>
        <button class="btn" onclick="closeQuiz()">${closeText}</button>
    `;

    showScreen('result-page');
}

function closeQuiz() {
    if (tg) {
        tg.close();
    }
}
