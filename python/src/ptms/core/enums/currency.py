from enum import StrEnum

"""Currency code enumerations used throughout PTMS."""


class CurrencyCode(StrEnum):
    """ISO 4217 currency codes."""

    AUD = "AUD"
    CAD = "CAD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"
    NZD = "NZD"
    SGD = "SGD"
    USD = "USD"
