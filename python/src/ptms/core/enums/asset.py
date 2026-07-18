from enum import StrEnum


class AssetClass(StrEnum):
    """Supported financial asset classes."""

    RSU = "RSU"
    EQUITY = "EQUITY"
    MUTUAL_FUND = "MUTUAL_FUND"
    PROPERTY = "PROPERTY"
    CASH = "CASH"
