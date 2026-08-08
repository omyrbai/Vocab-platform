from telegram import Update
from telegram.ext import ContextTypes

from app.db.database import SessionLocal

from app.dependencies import (
    get_language_service,
    get_term_service,
    get_topic_service,
)

from app.importers.telegram_importer import TelegramImporter
from app.services.flashcard_service import FlashcardService

async def channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    importer: TelegramImporter,
    flashcard_service: FlashcardService,
) -> None:
    """
    Handle new channel posts.
    """

    if update.channel_post is None:
        return

    text = update.channel_post.text

    if text is None:
        return

    with SessionLocal() as session:
        try:
            term_service = get_term_service(
                session,
            )

            language_service = get_language_service(
                session,
            )

            topic_service = get_topic_service(
                session,
            )

            result = importer.import_message(
                text=text,
                term_service=term_service,
                language_service=language_service,
                topic_service=topic_service,
            )
        except Exception:
            session.rollback()
            raise

        session.commit()

    flashcard_results = (
            result.created
            + result.updated
    )

    if flashcard_results:
        output_path = "flashcard.docx"

        flashcard_service.create_docx(
            terms=[
                item.term
                for item in flashcard_results
            ],
            output_path=output_path,
        )

        await context.bot.send_document(
            chat_id=update.channel_post.chat_id,
            document=output_path,
        )


    print("=" * 60)
    print(
        f"Created : {result.created_count}"
    )
    print(
        f"Updated : {result.updated_count}"
    )
    print(
        f"Skipped : {result.skipped_count}"
    )
    print(
        f"Total   : {result.total_count}"
    )
    print("=" * 60)