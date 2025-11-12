from telegram import Update
from telegram.ext import ContextTypes
from pages.commands import articles_wrapper, contacts_wrapper, paintings_wrapper, services_wrapper
from pages import common
from translation import translation_loader as tl
from pages.states import MENU, ARTICLES_MENU
from translation.languages import Locale, LOCALE

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == common.MainMenuCallback.SERVICES.value:
        await services_wrapper(update, context)
        return MENU
    elif data == common.MainMenuCallback.PAINTINGS.value:
        await paintings_wrapper(update, context)
        return MENU
    elif data == common.MainMenuCallback.ARTICLES.value:
        await articles_wrapper(update, context)
        return ARTICLES_MENU
    elif data == common.MainMenuCallback.CONTACTS.value:
        await contacts_wrapper(update, context)
        return MENU
    elif data == common.MainMenuCallback.BACK.value:
        greeting = tl.load(tl.ABOUT_TEXT, context)
        keyboard = common.get_main_keyboard(context)
        await query.edit_message_text(greeting, reply_markup=keyboard)
        return MENU
    elif data == common.MainMenuCallback.SET_LANG_EN.value:
        context.user_data[LOCALE] = Locale.EN.value
        keyboard = common.get_main_keyboard(context)
        await query.edit_message_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)
        return MENU
    elif data == common.MainMenuCallback.SET_LANG_RU.value:
        context.user_data[LOCALE] = Locale.RU.value
        keyboard = common.get_main_keyboard(context)
        await query.edit_message_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)
        return MENU
