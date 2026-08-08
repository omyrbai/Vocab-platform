import re

from app.enums.import_message_type import ImportMessageType

from app.parsers.term_parser import parse_terms

from app.schemas.import_result import ImportResult
from app.schemas.term import TermCreate, TermRead
from app.schemas.topic import TopicCreate
from app.schemas.upsert_result import UpsertResult


from app.services.language_service import LanguageService
from app.services.term_service import TermService
from app.services.topic_service import TopicService

TERM_PATTERN = re.compile(
    r"^\d+\.\s+"
)


class TelegramImporter:

    def __init__(
        self,
        source_language_code: str,
        target_language_code: str,
    ):
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

        self.current_topic_id: int | None = None

    def import_message(
            self,
            text: str,
            term_service: TermService,
            language_service: LanguageService,
            topic_service: TopicService,
    ) -> ImportResult:
        """
        Import a Telegram channel message.
        """

        text = text.strip()

        if not text:
            return ImportResult()

        message_type = self._detect_message_type(
            text,
        )

        match message_type:

            case ImportMessageType.TOPIC:
                return self._import_topic(
                    text,
                    topic_service,
                )

            case ImportMessageType.TERMS:
                return self._import_terms(
                    text,
                    term_service,
                    language_service,
                )

            case ImportMessageType.IGNORE:
                return ImportResult()
        raise AssertionError(
            "Unhandled import message type."
        )

    def _detect_message_type(
            self,
            text: str,
    ) -> ImportMessageType:
        """
        Detect the type of Telegram message.
        """

        first_line = text.splitlines()[0].strip()

        if first_line.startswith("#"):
            return ImportMessageType.TOPIC

        if TERM_PATTERN.match(first_line):
            return ImportMessageType.TERMS

        return ImportMessageType.IGNORE

    def _import_topic(
            self,
            text: str,
            topic_service: TopicService,
    ) -> ImportResult:
        """
        Import a topic message and make it the current topic.
        """

        topic_name = text.removeprefix("#").strip()

        if not topic_name:
            raise ValueError(
                "Topic name cannot be empty."
            )

        topic = topic_service.get_by_parent_and_name(
            parent_topic_id=None,
            name=topic_name,
        )

        if topic is None:
            create_data = TopicCreate(
                parent_topic_id=None,
                name=topic_name,
            )
            topic = topic_service.create(
                create_data,
            )

        self.current_topic_id = topic.topic_id

        return ImportResult()

    def _import_terms(
            self,
            text: str,
            term_service: TermService,
            language_service: LanguageService,
    ) -> ImportResult:
        """
        Import vocabulary terms from a Telegram message.
        """

        if self.current_topic_id is None:
            raise ValueError(
                "No active topic. Send a '#Topic' message first."
            )
        topic_id = self.current_topic_id

        parsed_terms = parse_terms(text)

        src_lang = language_service.get_by_code(
            self.source_language_code,
        )

        if src_lang is None:
            raise ValueError(
                f"Language '{self.source_language_code}' not found."
            )

        trg_lang = language_service.get_by_code(
            self.target_language_code,
        )

        if trg_lang is None:
            raise ValueError(
                f"Language '{self.target_language_code}' not found."
            )

        result = ImportResult()

        for parsed_term in parsed_terms:
            create_data = TermCreate(
                topic_id=topic_id,
                src_lang_id=src_lang.lang_id,
                trg_lang_id=trg_lang.lang_id,
                term=parsed_term.term,
                pronunciation=None,
                definition=parsed_term.definition,
                example=parsed_term.example,
                translation=parsed_term.translation,
            )

            db_term, action = term_service.upsert(
                create_data,
            )

            upsert_result = UpsertResult(
                term=TermRead.model_validate(db_term),
                action=action,
            )

            result.add(
                upsert_result,
            )

        return result
