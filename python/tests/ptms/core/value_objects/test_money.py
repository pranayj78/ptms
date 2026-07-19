from dataclasses import FrozenInstanceError
from decimal import Decimal
from typing import Any, cast

import pytest
from ptms.core.enums import CurrencyCode
from ptms.core.exceptions import CurrencyMismatchError, InvalidMoneyError
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


class TestMoneyArithmetic:
    def test_addition_returns_new_instance(self) -> None:
        left = Money.of("100.00", CurrencyCode.USD)
        right = Money.of("50.00", CurrencyCode.USD)

        result = left + right

        assert isinstance(result, Money)
        assert result is not left
        assert result is not right
        assert result.amount == Decimal("150.00")
        assert result.currency is CurrencyCode.USD

    def test_subtraction_returns_new_instance(self) -> None:
        left = Money.of("100.00", CurrencyCode.USD)
        right = Money.of("40.00", CurrencyCode.USD)

        result = left - right

        assert isinstance(result, Money)
        assert result is not left
        assert result is not right
        assert result.amount == Decimal("60.00")
        assert result.currency is CurrencyCode.USD

    def test_operations_do_not_mutate_operands(self) -> None:
        left = Money.of("100.00", CurrencyCode.USD)
        right = Money.of("25.00", CurrencyCode.USD)

        _ = left + right
        _ = left - right

        assert left.amount == Decimal("100.00")
        assert right.amount == Decimal("25.00")
        assert left.currency is CurrencyCode.USD
        assert right.currency is CurrencyCode.USD

    def test_addition_correctness(self) -> None:
        left = Money.of("0.10", CurrencyCode.USD)
        right = Money.of("0.20", CurrencyCode.USD)

        result = left + right

        assert result.amount == Decimal("0.30")

    def test_subtraction_correctness(self) -> None:
        left = Money.of("1000", CurrencyCode.INR)
        right = Money.of("333", CurrencyCode.INR)

        result = left - right

        assert result.amount == Decimal("667")

    def test_addition_requires_matching_currency(self) -> None:
        left = Money.of("10", CurrencyCode.USD)
        right = Money.of("10", CurrencyCode.INR)

        with pytest.raises(CurrencyMismatchError):
            _ = left + right

    def test_subtraction_requires_matching_currency(self) -> None:
        left = Money.of("10", CurrencyCode.USD)
        right = Money.of("10", CurrencyCode.INR)

        with pytest.raises(CurrencyMismatchError):
            _ = left - right

    def test_addition_rejects_unsupported_operand(self) -> None:
        left = Money.of("10", CurrencyCode.USD)

        with pytest.raises(TypeError):
            _ = left + 5

    def test_subtraction_rejects_unsupported_operand(self) -> None:
        left = Money.of("10", CurrencyCode.USD)

        with pytest.raises(TypeError):
            _ = left - 5
