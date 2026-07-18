from enum import StrEnum


class TaxRegime(StrEnum):
    """Indian income tax regimes."""

    OLD = "OLD"
    NEW = "NEW"
