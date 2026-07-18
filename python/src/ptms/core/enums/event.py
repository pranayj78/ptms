from enum import StrEnum


class EventType(StrEnum):
    """Financial events tracked by PTMS."""

    GRANT = "GRANT"
    VEST = "VEST"
    RELEASE = "RELEASE"
    SALE = "SALE"
    DIVIDEND = "DIVIDEND"
