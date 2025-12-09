import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from pages.commands import start, unknown, help_command
from pages.common import admin_file_handler, main_menu_command
from utils.logging_config import configure_logging
from pages.main_menu import menu_handler
from pages.articles.menu import articles_handler
from pages.commands import contacts_wrapper, articles_wrapper, paintings_wrapper, services_wrapper
from pages.statistics import statistics_command, statistics_callback


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logger = configure_logging()


def main() -> None:
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not set")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    logger.info("ApplicationBuilder created")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern=r"^(services|paintings|contacts|articles|back|set_lang_en|set_lang_ru)$"))
    app.add_handler(CallbackQueryHandler(articles_handler, pattern=r"^(show_guide|back_to_articles|main_menu)$"))

    app.add_handler(CallbackQueryHandler(statistics_callback, pattern=r"^stats_"))

    app.add_handler(CommandHandler('services', services_wrapper))
    app.add_handler(CommandHandler('paintings', paintings_wrapper))
    app.add_handler(CommandHandler('articles', articles_wrapper))
    app.add_handler(CommandHandler('contacts', contacts_wrapper))
    app.add_handler(CommandHandler('main', main_menu_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("statistics", statistics_command))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, admin_file_handler))
    

    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Starting bot")
    try:
        app.run_polling()
    except Exception:
        logger.exception("Bot crashed with an exception")


if __name__ == "__main__":
    main()
