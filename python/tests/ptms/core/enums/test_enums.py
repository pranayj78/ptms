from enum import StrEnum

import pytest
from ptms.core.enums import (
    AssetClass,
    CountryCode,
    CurrencyCode,
    DocumentType,
    EventType,
    TaxRegime,
)


@pytest.mark.parametrize(
    ("enum_cls", "expected_values"),
    [
        (CountryCode, {"IN", "US", "GB", "AU", "CA", "SG", "NZ"}),
        (CurrencyCode, {"INR", "USD", "GBP", "EUR", "AUD", "CAD", "SGD", "NZD"}),
        (
            DocumentType,
            {
                "FORM16",
                "AIS",
                "BROKER_STATEMENT",
                "HOME_LOAN_CERTIFICATE",
                "BANK_STATEMENT",
            },
        ),
        (EventType, {"GRANT", "VEST", "RELEASE", "SALE", "DIVIDEND"}),
        (TaxRegime, {"OLD", "NEW"}),
        (AssetClass, {"RSU", "EQUITY", "MUTUAL_FUND", "PROPERTY", "CASH"}),
    ],
)
def test_enum_values(enum_cls: type[StrEnum], expected_values: set[str]) -> None:
    actual_values = {item.value for item in enum_cls}
    assert actual_values == expected_values


@pytest.mark.parametrize(
    ("enum_cls", "valid_value", "invalid_value"),
    [
        (CountryCode, "IN", "XX"),
        (CurrencyCode, "INR", "ABC"),
        (DocumentType, "FORM16", "PAN"),
        (EventType, "VEST", "BONUS"),
        (TaxRegime, "OLD", "DEFAULT"),
        (AssetClass, "RSU", "BOND"),
    ],
)
def test_enum_lookup_and_invalid_value(
    enum_cls: type[StrEnum], valid_value: str, invalid_value: str
) -> None:
    member = enum_cls(valid_value)
    assert member.value == valid_value
    assert isinstance(member, str)

    with pytest.raises(ValueError):
        enum_cls(invalid_value)
