import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from translation import translation_loader as tl
from translation.languages import Language, Locale, LOCALE
from telegram.ext import ContextTypes
from enum import Enum


class MainMenuCallback(str, Enum):
    SERVICES = 'services'
    PAINTINGS = 'paintings'
    CONTACTS = 'contacts'
    ARTICLES = 'articles'
    BACK = 'back'
    SET_LANG_EN = 'set_lang_en'
    SET_LANG_RU = 'set_lang_ru'


def get_locale(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get(LOCALE, Locale.RU.value)


def get_main_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    locale = get_locale(context)
    if locale == Locale.RU.value:
        lang_row = [InlineKeyboardButton(Language.ENGLISH.value, callback_data=MainMenuCallback.SET_LANG_EN.value)]
    else:
        lang_row = [InlineKeyboardButton(Language.RUSSIAN.value    , callback_data=MainMenuCallback.SET_LANG_RU.value)]

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tl.load(tl.LABEL_SERVICES, context), callback_data=MainMenuCallback.SERVICES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_PAINTINGS, context), callback_data=MainMenuCallback.PAINTINGS.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_ARTICLES, context), callback_data=MainMenuCallback.ARTICLES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_CONTACTS, context), callback_data=MainMenuCallback.CONTACTS.value)],
        lang_row
    ])


def get_back_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=MainMenuCallback.BACK.value)],
    ])


async def main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = get_main_keyboard(context)
    await update.message.reply_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)

async def admin_file_handler(update, context):
    admin_user_ids = os.getenv("ADMIN_USER_IDS", "")
    if str(update.effective_user.id) in admin_user_ids:
        await update.message.reply_text(str(update.message.document.file_id))