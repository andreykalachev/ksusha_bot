from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from pages import common
from translation import translation_loader as tl
from translation.languages import Locale
from utils import statistics
from statistics.page_visits import Page

TG_URL = "https://t.me/kseniialf"
TG_CHANNEL_URL = "https://t.me/kseniialfs"
INSTAGRAM_RU = "https://www.instagram.com/kseniialf"
INSTAGRAM_EN = "https://www.instagram.com/kseniialf.art"
BEHANCE_URL = "https://www.behance.net/kseniialf"
EMAIL_COMPOSE_URL = "https://mail.google.com/mail/?view=cm&fs=1&to=kseniiaalferova@gmail.com"


def _build_contacts_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.CONTACTS)

    locale = common.get_locale(context)
    instagram = INSTAGRAM_RU if locale == Locale.RU.value else INSTAGRAM_EN

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_TELEGRAM, context), url=TG_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_CHANNEL, context), url=TG_CHANNEL_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_INSTAGRAM, context), url=instagram)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_BEHANCE, context), url=BEHANCE_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_EMAIL, context), url=EMAIL_COMPOSE_URL)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.CONTACTS_TEXT, context)
    return text, reply_markup


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, reply_markup = _build_contacts_payload(context)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, reply_markup = _build_contacts_payload(context)
    await update.message.reply_text(text, reply_markup=reply_markup)
