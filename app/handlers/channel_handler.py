import re

from telegram import Update
from telegram.ext import ContextTypes

from app.ai.vocabulary_generator import VocabularyGenerator
from app.db.database import SessionLocal

from app.dependencies import (
    get_language_service,
    get_term_service,
    get_topic_service,
)

from app.importers.telegram_importer import TelegramImporter
from app.services.flashcard_service import FlashcardService

def _is_raw_vocabulary_list(
    text: str,
) -> bool:
    """
    Check whether the message is a raw vocabulary list.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return False

    # A topic is handled by TelegramImporter.
    if lines[0].startswith("#"):
        return False

    # Every non-empty line must be a numbered bold term.
    if any(
        re.match(r"^\d+\.\s+\*\*.+\*\*$", line)
        for line in lines
    ):
        return False

    return True

async def channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    importer: TelegramImporter,
    generator: VocabularyGenerator,
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

    text = text.strip()
    if not text:
        return

    if _is_raw_vocabulary_list(text):
        print("Raw vocabulary list detected.")

        with SessionLocal() as session:
            term_service = get_term_service(
                session,
            )

            latest_term = term_service.get_latest()

            if latest_term is None:
                start_number = 1
            else:
                start_number = latest_term.term_id + 1

        print(f"Generating vocabulary with AI starting from {start_number}...")

        generated_text = generator.generate(
            text,
            start_number=start_number,
        )

        print("AI generation completed.")
        print("-" * 60)
        print(generated_text)
        print("-" * 60)

        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,
            text=generated_text,
            parse_mode="HTML",
        )

        print("Generated vocabulary posted to channel.")

        text = generated_text

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