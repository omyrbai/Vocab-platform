from app.schemas.import_result import ImportResult
from app.schemas.parsed_term import ParsedTerm
from app.services.term_service import TermService


class GermanImporter:

    def __init__(
        self,
        term_service: TermService,
    ):
        self.term_service = term_service