import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from translation import translation_loader as tl
from pages import common
from utils import statistics
from statistics.page_visits import Page

async def show_inspiration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    statistics.increment_page(Page.INSPIRATION)
    query = update.callback_query
    
    # Load static text
    intro_text = tl.load(tl.INSPIRATION_INTRO, context)
    outro_text = tl.load(tl.INSPIRATION_OUTRO, context)
    
    # Load cards
    cards = tl.load(tl.INSPIRATION_CARDS, context)
    
    if not isinstance(cards, list) or not cards:
        # Fallback if something is wrong with translations
        text = intro_text + "\n\n(No inspiration cards found)"
    else:
        card = random.choice(cards)
        color = card.get('color') or card.get('Color', '')
        quote = card.get('quote') or card.get('Quote', '')
        exercise = card.get('exercise') or card.get('Exercise', '')
        
        text = (
            f"{intro_text}\n\n"
            f"-------------------------\n"
            f"🎨 *{color}*\n\n"
            f"_{quote}_\n\n"
            f"🧘‍♀️ {exercise}\n"
            f"-------------------------\n\n\n"
            f"{outro_text}"
        )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(tl.load(tl.LABEL_INSPIRATION_NEW, context), callback_data=common.MainMenuCallback.INSPIRATION.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)]
    ])
    
    # If called from menu, edit message. If called via command (if we add one), send message.
    if query:
        try:
            await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode='Markdown')
        except Exception:
            pass
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard, parse_mode='Markdown')

async def inspiration_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_inspiration(update, context)

async def inspiration_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_inspiration(update, context)
    else:
        await inspiration_command(update, context)
