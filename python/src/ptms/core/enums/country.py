from enum import StrEnum


class CountryCode(StrEnum):
    """ISO 3166-1 alpha-2 country codes supported by PTMS."""

    IN = "IN"
    US = "US"
    GB = "GB"
    AU = "AU"
    CA = "CA"
    SG = "SG"
    NZ = "NZ"
