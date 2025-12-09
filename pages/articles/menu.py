from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes
from pages import common

from translation import translation_loader as tl
from enum import Enum


class ArticleCallback(str, Enum):
    SHOW_GUIDE = 'show_guide'
    BACK_TO_ARTICLES = 'back_to_articles'
    MAIN_MENU = 'main_menu'


def _build_articles_payload(context: ContextTypes.DEFAULT_TYPE):
    # This function is used by commands, ensuring consistency
    locale = common.get_locale(context)
    web_app_url = f"https://andreykalachev.github.io/ksusha_bot/index.html?lang={locale}"

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_GUIDE, context), callback_data=ArticleCallback.SHOW_GUIDE.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_QUIZ, context), web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=ArticleCallback.MAIN_MENU.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.ARTICLES_MENU_GREETING, context)
    return text, reply_markup


async def articles_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == ArticleCallback.SHOW_GUIDE.value:
        from pages.articles.guide import show_guide
        await show_guide(update, context)
        return

    if data == ArticleCallback.MAIN_MENU.value:
        greeting = tl.load(tl.ABOUT_TEXT, context)
        keyboard = common.get_main_keyboard(context)
        await query.edit_message_text(greeting, reply_markup=keyboard)
        return

    text, reply_markup = _build_articles_payload(context)

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    except Exception:
        # Ignore if message is not modified
        pass


async def show_articles_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, reply_markup = _build_articles_payload(context)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def articles_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, reply_markup = _build_articles_payload(context)
    await update.message.reply_text(text, reply_markup=reply_markup)
