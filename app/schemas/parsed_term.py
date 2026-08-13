from pydantic import BaseModel


class ParsedTerm(BaseModel):
    """
    Represents a single parsed vocabulary entry extracted
    from an external source (Telegram, PDF, CSV, etc.).
    """

    term: str
    gender: str | None = None
    definition: str
    example: str
    translation: str

