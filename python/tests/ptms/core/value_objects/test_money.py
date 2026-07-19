from dataclasses import FrozenInstanceError
from decimal import Decimal
from typing import Any, cast

import pytest
from ptms.core.enums import CurrencyCode
from ptms.core.exceptions import InvalidMoneyError
from ptms.core.value_objects import Money


def test_construction_from_string() -> None:
    money = Money.of("100.25", CurrencyCode.USD)

    assert money.amount == Decimal("100.25")
    assert money.currency is CurrencyCode.USD


def test_decimal_construction() -> None:
    money = Money.of(Decimal("2500.50"), CurrencyCode.INR)

    assert money.amount == Decimal("2500.50")
    assert money.currency is CurrencyCode.INR


def test_integer_construction() -> None:
    money = Money.of(5000, CurrencyCode.GBP)

    assert money.amount == Decimal("5000")
    assert money.currency is CurrencyCode.GBP


def test_invalid_string() -> None:
    with pytest.raises(InvalidMoneyError):
        Money.of("not-a-number", CurrencyCode.USD)


def test_float_rejected() -> None:
    with pytest.raises(InvalidMoneyError):
        Money.of(cast(Any, 12.34), CurrencyCode.USD)


def test_frozen_dataclass() -> None:
    money = Money.of("100.00", CurrencyCode.USD)
    mutable_ref = cast(Any, money)

    with pytest.raises(FrozenInstanceError):
        mutable_ref.amount = Decimal("200.00")


def test_decimal_preserved() -> None:
    money = Money.of("0.10", CurrencyCode.USD)

    assert money.amount == Decimal("0.10")
    assert money.amount.as_tuple().exponent == -2
