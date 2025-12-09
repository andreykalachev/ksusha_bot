from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from utils import statistics
from statistics.page_visits import Page

REVIEWS_URL = os.getenv("REVIEWS_URL")

def _build_reviews_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.REVIEWS)
    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_REVIEWS_LINK, context), url=REVIEWS_URL)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.REVIEWS_TEXT, context)
    return text, reply_markup

async def show_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text, reply_markup = _build_reviews_payload(context)
    await query.edit_message_text(text=text, reply_markup=reply_markup)


async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = _build_reviews_payload(context)
    await update.message.reply_text(text=text, reply_markup=reply_markup)
