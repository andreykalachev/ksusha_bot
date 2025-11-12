from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import statistics
from pages import common
from typing import Tuple
import os


RESET_CALLBACK = "stats_reset"


def _is_admin(update: Update) -> bool:
    admin_user_ids = os.getenv("ADMIN_USER_IDS", "")
    return str(update.effective_user.id) in admin_user_ids


def _build_stats_payload() -> Tuple[str, InlineKeyboardMarkup]:
    text = statistics.get_stats_text()
    keyboard = [
        [InlineKeyboardButton("Reset statistics", callback_data=RESET_CALLBACK)],
        [InlineKeyboardButton("Back", callback_data=common.MainMenuCallback.BACK.value)],
    ]
    return text, InlineKeyboardMarkup(keyboard)


async def statistics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update):
        return

    text, reply_markup = _build_stats_payload()
    await update.message.reply_text(text, reply_markup=reply_markup)


async def statistics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not _is_admin(update) or not query:
        return

    if query.data == RESET_CALLBACK:
        statistics.reset()
        await query.answer()
        text, reply_markup = _build_stats_payload()
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await query.answer()
