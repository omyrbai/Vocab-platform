from pydantic import BaseModel
from app.enums.import_action import ImportAction
from app.schemas.term import TermRead

class UpsertResult(BaseModel):
    """
    Result of a single upsert operation.
    """

    term: TermRead
    action: ImportAction