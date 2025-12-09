from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import statistics
from pages import common
from typing import Tuple
import os


RESET_CALLBACK = "stats_reset"
MORE_CALLBACK_PREFIX = "stats_more_"


async def _build_stats_payload(context: ContextTypes.DEFAULT_TYPE, offset: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
    text = await statistics.get_stats_text(context.bot, offset=offset)
    
    keyboard = []
    
    # Check if we can show more (previous users)
    total_users = statistics.get_unique_users_count()
    # If we are showing [start_index:end_index], end_index = total - offset.
    # start_index = max(0, end_index - 10).
    # If start_index > 0, we have more users before this page.

    nav_buttons = []
    if total_users - offset - 10 > 0:
        nav_buttons.append(InlineKeyboardButton("⬆️ Show previous", callback_data=f"{MORE_CALLBACK_PREFIX}{offset + 10}"))
    if offset > 0:
        nav_buttons.append(InlineKeyboardButton("⬇️ Show newer", callback_data=f"{MORE_CALLBACK_PREFIX}{max(0, offset - 10)}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("Reset statistics", callback_data=RESET_CALLBACK)])
    keyboard.append([InlineKeyboardButton("Back", callback_data=common.MainMenuCallback.BACK.value)])
    
    return text, InlineKeyboardMarkup(keyboard)


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not common.is_admin(update.effective_user.id):
        return

    text, reply_markup = await _build_stats_payload(context)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


async def statistics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_statistics(update, context)


async def statistics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not common.is_admin(update.effective_user.id) or not query:
        return

    if query.data == RESET_CALLBACK:
        statistics.reset()
        await query.answer()
        text, reply_markup = await _build_stats_payload(context)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    elif query.data.startswith(MORE_CALLBACK_PREFIX):
        offset = int(query.data.replace(MORE_CALLBACK_PREFIX, ""))
        await query.answer()
        text, reply_markup = await _build_stats_payload(context, offset=offset)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await query.answer()
