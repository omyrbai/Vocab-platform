from pydantic import BaseModel


class ParsedTerm(BaseModel):
    """
    Represents a single parsed vocabulary entry extracted
    from an external source (Telegram, PDF, CSV, etc.).
    """

    term: str
    definition: str
    example: str
    translation: str

