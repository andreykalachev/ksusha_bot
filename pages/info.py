from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from utils import statistics
from statistics.page_visits import Page

INFO_PDF_FILE_ID = os.getenv("INFO_PDF_FILE_ID")


def _build_info_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.INFO)
    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.INFO_TEXT, context)
    return text, reply_markup


async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text, reply_markup = _build_info_payload(context)
    
    await query.message.delete()
    await context.bot.send_document(
        chat_id=query.message.chat_id,
        document=INFO_PDF_FILE_ID,
        caption=text,
        reply_markup=reply_markup
    )


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = _build_info_payload(context)
    await update.message.reply_document(
        document=INFO_PDF_FILE_ID,
        caption=text,
        reply_markup=reply_markup
    )
