from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes
import os
from translation import translation_loader as tl
from .menu import ArticleCallback
from pages import common
from translation.languages import Locale
from utils import statistics
from statistics.page_visits import Page


GUIDE_TELEGRAM_FILE_ID = os.getenv("GUIDE_TELEGRAM_FILE_ID")


async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    locale = common.get_locale(context)
    web_app_url = f"{os.getenv('WEB_APP_URL')}?lang={locale}"

    statistics.increment_page(Page.GUIDE)

    message = tl.load(tl.GUIDE_TEXT, context)

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_QUIZ, context), web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=ArticleCallback.BACK_TO_ARTICLES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_MAIN_MENU, context), callback_data=ArticleCallback.MAIN_MENU.value)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if locale == Locale.EN.value:
        await query.edit_message_text(message, reply_markup=reply_markup)
        return

    await query.message.delete()
    await context.bot.send_document(
        chat_id=query.message.chat_id,
        document=GUIDE_TELEGRAM_FILE_ID,
        caption=message,
        reply_markup=reply_markup
    )
