import json
import os
from typing import List, Dict, Tuple
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from pages.states import ARTICLES_MENU
from translation import translation_loader as tl
from pages.common import get_locale

QUIZ_DATA_DIR = "pages/articles/quiz/data"


def load_quiz_data(lang: str = "ru") -> Tuple[List[Dict], List[Dict]]:
    """Load questions and answers from JSON files for specified language."""
    questions_file = os.path.join(QUIZ_DATA_DIR, f"questions_{lang}.json")
    answers_file = os.path.join(QUIZ_DATA_DIR, f"answers_{lang}.json")
    
    with open(questions_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    with open(answers_file, 'r', encoding='utf-8') as f:
        answers = json.load(f)
    
    return questions, answers


def calculate_result(user_answers: List[int], questions: List[Dict], lang: str = "ru") -> Dict:
    """Calculate quiz result based on user answers.
    
    Example: If user selects option 1 (weights=[1,2]) for Q1 
    and option 2 (weights=[0,2,0]) for Q2,
    total weights = [1, 4, 0], so result is answer index 1.
    """
    _, answers = load_quiz_data(lang)
    
    # Initialize weights for each answer
    weights = [0] * len(answers)
    
    # Sum up weights from user choices
    for question_idx, option_idx in enumerate(user_answers):
        if question_idx < len(questions):
            option = questions[question_idx]["options"][option_idx]
            for i, weight in enumerate(option["weights"]):
                if i < len(weights):
                    weights[i] += weight
    
    # Find answer with highest weight
    max_weight = max(weights)
    result_idx = weights.index(max_weight)
    
    result = answers[result_idx].copy()
    result["weight"] = max_weight
    result["all_weights"] = weights
    
    return result


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initial quiz entry point - show Mini App immediately."""
    query = update.callback_query
    await query.answer()
    
    locale = get_locale(context)
    
    # Replace this with your actual deployed quiz Mini App URL
    web_app_url = f"https://andreykalachev.github.io/ksusha-quiz-miniapp/static/quiz.html?lang={locale}"
    
    texts = {
        "ru": {
            "button": "🎨 Начать квиз об искусстве",
            "message": "✨ Узнайте, какой стиль искусства вам подходит!\n\nПройдите быстрый квиз, чтобы выяснить, какой тип произведений резонирует с вашей личностью."
        },
        "en": {
            "button": "🎨 Start Art Quiz",
            "message": "✨ Discover which art style suits you best!\n\nTake our quick quiz to find out what type of artwork resonates with your personality."
        }
    }
    
    text = texts.get(locale, texts["ru"])
    
    keyboard = [
        [InlineKeyboardButton(
            text["button"],
            web_app=WebAppInfo(url=web_app_url)
        )],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data="back_to_articles")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text["message"],
        reply_markup=reply_markup
    )
    
    return ARTICLES_MENU


async def process_quiz_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process quiz result from Mini App."""
    if update.message and update.message.web_app_data:
        result_text = update.message.web_app_data.data
        await update.message.reply_text(result_text, parse_mode="Markdown")
