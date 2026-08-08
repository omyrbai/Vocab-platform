from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

from app.core.settings import settings
from app.handlers.channel_handler import channel_post

from functools import partial

from app.importers.telegram_importer import TelegramImporter
from app.services.flashcard_service import FlashcardService

def main() -> None:
    """
    Start the Telegram bot.
    """
    importer = TelegramImporter(
        source_language_code="de",
        target_language_code="en",
    )

    flashcard_service = FlashcardService()

    application = (
        Application.builder()
        .token(settings.BOT_TOKEN)
        .build()
    )

    application.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            partial(
                channel_post,
                importer=importer,
                flashcard_service=flashcard_service,
            ),
        )
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()