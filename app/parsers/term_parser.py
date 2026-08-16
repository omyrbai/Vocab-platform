import re
from app.schemas.parsed_term import ParsedTerm

_TERM_PATTERN = re.compile(
    r"^\d+\.\s+(.+)$"
)

def _extract_term(
    line: str,
) -> str:
    """
    Extract the term from a numbered line.

    Example:
        "23. trennbar" -> "trennbar"
    """
    match = _TERM_PATTERN.match(line)

    if match is None:
        raise ValueError(
            f"Invalid term line: {line}"
        )

    return match.group(1).strip()

def _extract_gender_and_definition(
    definition: str,
) -> tuple[str | None, str]:
    """
    Extract gender from a definition when present.
    """

    if " - " not in definition:
        return None, definition.strip()

    prefix, actual_definition = definition.split(
        " - ",
        1,
    )

    prefix = prefix.strip()

    if prefix in {"M", "F", "N"}:
        return prefix, actual_definition.strip()

    return None, definition.strip()

def parse_terms(
        text: str,
) -> list[ParsedTerm]:
    """
    Parse vocabulary entries from text.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    terms: list[ParsedTerm] = []

    i = 0

    while i < len(lines):
        if i + 3 >= len(lines):
            raise ValueError(
                "Incomplete vocabulary entry."
            )

        if _TERM_PATTERN.match(lines[i]) is None:
            raise ValueError(
                f"Expected numbered term line, got: {lines[i]}"
            )

        gender, definition = _extract_gender_and_definition(
            lines[i+1]
        )

        terms.append(
            ParsedTerm(
                term=_extract_term(lines[i]),
                gender=gender,
                definition=definition,
                example=lines[i + 2],
                translation=lines[i + 3],
            )
        )

        i += 4

    return terms