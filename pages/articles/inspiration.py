from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os
from translation import translation_loader as tl
from .menu import ArticleCallback
from pages import common
from utils import statistics
from statistics.page_visits import Page


async def show_inspiration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    statistics.increment_page(Page.INSPIRATION)

    message = tl.load(tl.INSPIRATION_TEXT, context)

    locale = common.get_locale(context)
    if locale == common.Locale.RU.value:
        inspiration_url = os.getenv("INSPIRATION_URL_RU")
    else:
        inspiration_url = os.getenv("INSPIRATION_URL_EN")

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_INSPIRATION_LINK, context), url=inspiration_url)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=ArticleCallback.BACK_TO_ARTICLES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_MAIN_MENU, context), callback_data=ArticleCallback.MAIN_MENU.value)],
    ]

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
