from enum import Enum, auto


class ImportMessageType(Enum):
    TOPIC = auto()
    TERMS = auto()
    IGNORE = auto()