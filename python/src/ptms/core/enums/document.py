from enum import StrEnum

"""Document type enumerations used throughout PTMS."""


class DocumentType(StrEnum):
    """Supported document types."""

    FORM16 = "FORM16"
    AIS = "AIS"
    BROKER_STATEMENT = "BROKER_STATEMENT"
    HOME_LOAN_CERTIFICATE = "HOME_LOAN_CERTIFICATE"
    BANK_STATEMENT = "BANK_STATEMENT"
