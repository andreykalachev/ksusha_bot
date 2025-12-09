from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.error import BadRequest
from telegram.ext import ContextTypes
import os
from pages import common

from translation import translation_loader as tl
from enum import Enum
from utils import statistics
from statistics.page_visits import Page


class ArticleCallback(str, Enum):
    SHOW_GUIDE = 'show_guide'
    SHOW_INSPIRATION = 'show_inspiration'
    BACK_TO_ARTICLES = 'back_to_articles'
    MAIN_MENU = 'main_menu'


def _build_articles_payload(context: ContextTypes.DEFAULT_TYPE):
    locale = common.get_locale(context)
    web_app_url = f"{os.getenv('WEB_APP_URL')}?lang={locale}"
    artist_day_url = os.getenv("ARTIST_DAY_URL")

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_QUIZ, context), web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(tl.load(tl.LABEL_GUIDE, context), callback_data=ArticleCallback.SHOW_GUIDE.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_INSPIRATION, context), callback_data=ArticleCallback.SHOW_INSPIRATION.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_ARTIST_DAY, context), url=artist_day_url)],
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

    if data == ArticleCallback.SHOW_INSPIRATION.value:
        from pages.articles.inspiration import show_inspiration
        await show_inspiration(update, context)
        return

    if data == ArticleCallback.MAIN_MENU.value:
        statistics.increment_page(Page.MAIN)
        greeting = tl.load(tl.ABOUT_TEXT, context)
        keyboard = common.get_main_keyboard(context)
        try:
            await query.edit_message_text(greeting, reply_markup=keyboard)
        except BadRequest:
            await query.message.delete()
            await context.bot.send_message(chat_id=query.message.chat_id, text=greeting, reply_markup=keyboard)
        return

    text, reply_markup = _build_articles_payload(context)

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    except BadRequest:
        await query.message.delete()
        await context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=reply_markup)
    except Exception:
        pass


async def show_articles_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, reply_markup = _build_articles_payload(context)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def articles_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, reply_markup = _build_articles_payload(context)
    await update.message.reply_text(text, reply_markup=reply_markup)
