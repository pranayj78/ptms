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


def test_invalid_currency_rejected() -> None:
    with pytest.raises(InvalidMoneyError):
        Money.of("10.00", cast(Any, "USD"))


def test_frozen_dataclass() -> None:
    money = Money.of("100.00", CurrencyCode.USD)
    mutable_ref = cast(Any, money)

    with pytest.raises(FrozenInstanceError):
        mutable_ref.amount = Decimal("200.00")


def test_decimal_preserved() -> None:
    money = Money.of("0.10", CurrencyCode.USD)

    assert money.amount == Decimal("0.10")
    assert money.amount.as_tuple().exponent == -2


def test_no_implicit_rounding_on_construction() -> None:
    money = Money.of("1.2300", CurrencyCode.USD)

    assert money.amount == Decimal("1.2300")
    assert money.amount.as_tuple().exponent == -4


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

    def test_no_implicit_rounding_in_arithmetic(self) -> None:
        left = Money.of("1.2300", CurrencyCode.USD)
        right = Money.of("2.100", CurrencyCode.USD)

        result = left + right

        assert result.amount == Decimal("3.3300")
        assert result.amount.as_tuple().exponent == -4

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

    def test_addition_rejects_decimal_operand(self) -> None:
        left = Money.of("10", CurrencyCode.USD)

        with pytest.raises(TypeError):
            _ = left + Decimal("1.5")


class TestScalarArithmetic:
    def test_money_can_be_multiplied_by_integer(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        result = salary * 2
        assert result == Money.of("200000", CurrencyCode.INR)
        assert salary * 1 == salary
        assert salary.amount == Decimal("100000")
        assert result.amount == Decimal("200000")

    def test_money_can_be_multiplied_by_zero(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert salary * 0 == Money.of("0", CurrencyCode.INR)

    def test_money_can_be_multiplied_by_negative_integer(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert salary * -1 == Money.of("-100000", CurrencyCode.INR)

    def test_money_can_be_multiplied_by_decimal(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert salary * Decimal("2") == Money.of("200000", CurrencyCode.INR)
        assert salary * Decimal("1.5") == Money.of("150000", CurrencyCode.INR)
        assert salary * Decimal("0") == Money.of("0", CurrencyCode.INR)
        assert salary * Decimal("-1") == Money.of("-100000", CurrencyCode.INR)

    def test_money_supports_reflected_integer_multiplication(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert 2 * salary == Money.of("200000", CurrencyCode.INR)
        assert 1 * salary == salary

    def test_money_supports_reflected_decimal_multiplication(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert Decimal("2") * salary == Money.of("200000", CurrencyCode.INR)
        assert Decimal("1.5") * salary == Money.of("150000", CurrencyCode.INR)
        assert Decimal("0") * salary == Money.of("0", CurrencyCode.INR)
        assert Decimal("-1") * salary == Money.of("-100000", CurrencyCode.INR)

    def test_money_decimal_multiplication_preserves_precision(self) -> None:
        price = Money.of("99.99", CurrencyCode.INR)

        assert price * Decimal("1.25") == Money.of("124.9875", CurrencyCode.INR)

    def test_money_decimal_multiplication_preserves_currency(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        result = salary * Decimal("1.5")

        assert result.currency is CurrencyCode.INR

    def test_money_decimal_multiplication_does_not_mutate_operand(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        _ = salary * Decimal("1.5")

        assert salary.amount == Decimal("100000")
        assert salary.currency is CurrencyCode.INR

    def test_money_cannot_be_multiplied_by_bool(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = salary * True

    def test_money_cannot_be_multiplied_by_float(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = salary * cast(Any, 2.5)

    def test_money_cannot_be_multiplied_by_money(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)
        factor = Money.of("2", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = salary * factor

    def test_money_cannot_be_reflected_multiplied_by_bool(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = True * salary

    def test_money_cannot_be_reflected_multiplied_by_float(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = 2.5 * salary

    def test_money_multiplication_preserves_currency(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        result = salary * 2

        assert result.currency is CurrencyCode.INR

    def test_money_can_be_divided_by_integer(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        assert salary / 12 == Money.of("10000", CurrencyCode.INR)
        assert salary / 1 == salary
        assert salary / -2 == Money.of("-60000", CurrencyCode.INR)

    def test_money_can_be_divided_by_decimal(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert salary / Decimal("2") == Money.of("50000", CurrencyCode.INR)
        assert salary / Decimal("0.5") == Money.of("200000", CurrencyCode.INR)
        assert salary / Decimal("-2") == Money.of("-50000", CurrencyCode.INR)

    def test_money_division_by_zero_raises_zero_division_error(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        with pytest.raises(ZeroDivisionError):
            _ = salary / 0

    def test_money_division_by_decimal_zero_raises_zero_division_error(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        with pytest.raises(ZeroDivisionError):
            _ = salary / Decimal("0")

    def test_money_cannot_be_divided_by_bool(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = salary / True

    def test_money_cannot_be_divided_by_float(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        with pytest.raises(TypeError):
            _ = salary / cast(Any, 2.5)

    def test_money_divided_by_money_returns_decimal_ratio(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)
        divisor = Money.of("2", CurrencyCode.INR)

        assert salary / divisor == Decimal("60000")

    def test_money_can_be_divided_by_money_to_produce_ratio(self) -> None:
        bonus = Money.of("10000", CurrencyCode.INR)
        salary = Money.of("100000", CurrencyCode.INR)

        bonus_percentage = bonus / salary

        assert bonus_percentage == Decimal("0.1")

    def test_money_can_be_divided_by_money_to_produce_decimal_completion(self) -> None:
        tax_paid = Money.of("25000", CurrencyCode.INR)
        tax_due = Money.of("50000", CurrencyCode.INR)

        completion = tax_paid / tax_due

        assert completion == Decimal("0.5")

    def test_money_divided_by_itself_returns_one(self) -> None:
        salary = Money.of("100000", CurrencyCode.INR)

        assert salary / salary == Decimal("1")

    def test_money_ratio_preserves_precision(self) -> None:
        one = Money.of("1", CurrencyCode.INR)
        three = Money.of("3", CurrencyCode.INR)

        assert one / three == Decimal("0.3333333333333333333333333333")

    def test_money_ratio_requires_matching_currency(self) -> None:
        paid = Money.of("25000", CurrencyCode.INR)
        due = Money.of("50000", CurrencyCode.USD)

        with pytest.raises(CurrencyMismatchError):
            _ = paid / due

    def test_money_ratio_zero_divisor_raises_zero_division_error(self) -> None:
        paid = Money.of("25000", CurrencyCode.INR)
        due = Money.of("0", CurrencyCode.INR)

        with pytest.raises(ZeroDivisionError):
            _ = paid / due

    def test_money_division_preserves_currency(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        result = salary / 12

        assert isinstance(result, Money)
        assert result.currency is CurrencyCode.INR

    def test_money_division_preserves_precision(self) -> None:
        salary = Money.of("100", CurrencyCode.INR)

        result = salary / Decimal("3")

        assert isinstance(result, Money)
        assert result.amount == Decimal("33.33333333333333333333333333")

    def test_money_division_does_not_mutate_operand(self) -> None:
        salary = Money.of("120000", CurrencyCode.INR)

        # Perform the operation to verify that the original instance remains unchanged.
        _ = salary / 12

        assert salary.amount == Decimal("120000")
        assert salary.currency is CurrencyCode.INR


class TestMoneyComparison:
    def test_less_than(self) -> None:
        smaller = Money.of("10.00", CurrencyCode.USD)
        larger = Money.of("20.00", CurrencyCode.USD)

        assert smaller < larger

    def test_greater_than(self) -> None:
        larger = Money.of("20.00", CurrencyCode.USD)
        smaller = Money.of("10.00", CurrencyCode.USD)

        assert larger > smaller

    def test_equal(self) -> None:
        first = Money.of("10.00", CurrencyCode.USD)
        second = Money.of(Decimal("10.00"), CurrencyCode.USD)

        assert first == second

    def test_hash_semantics_for_equal_values(self) -> None:
        first = Money.of("10.00", CurrencyCode.USD)
        second = Money.of("10.00", CurrencyCode.USD)

        assert hash(first) == hash(second)
        assert len({first, second}) == 1

    def test_same_currency_required(self) -> None:
        usd = Money.of("10.00", CurrencyCode.USD)
        inr = Money.of("10.00", CurrencyCode.INR)

        with pytest.raises(CurrencyMismatchError):
            _ = usd < inr

        with pytest.raises(CurrencyMismatchError):
            _ = usd > inr

    def test_less_than_or_equal_for_same_amount(self) -> None:
        first = Money.of("10.00", CurrencyCode.USD)
        second = Money.of("10.00", CurrencyCode.USD)

        assert first <= second

    def test_greater_than_or_equal_for_same_amount(self) -> None:
        first = Money.of("10.00", CurrencyCode.USD)
        second = Money.of("10.00", CurrencyCode.USD)

        assert first >= second


class TestMoneyUnaryOperations:
    def test_unary_minus(self) -> None:
        money = Money.of("10.00", CurrencyCode.USD)

        result = -money

        assert result.amount == Decimal("-10.00")
        assert result.currency is CurrencyCode.USD
        assert result is not money

    def test_absolute_value(self) -> None:
        money = Money.of("-10.00", CurrencyCode.USD)

        result = abs(money)

        assert result.amount == Decimal("10.00")
        assert result.currency is CurrencyCode.USD
        assert result is not money

    def test_unary_operations_do_not_mutate_operand(self) -> None:
        money = Money.of("-10.00", CurrencyCode.USD)

        _ = -money
        _ = abs(money)

        assert money.amount == Decimal("-10.00")


class TestMoneyInvariants:
    def test_money_is_immutable(self) -> None:
        money = Money.of("100.00", CurrencyCode.USD)
        mutable_ref = cast(Any, money)

        with pytest.raises(FrozenInstanceError):
            mutable_ref.amount = Decimal("200.00")

    def test_money_preserves_precision(self) -> None:
        money = Money.of("1.2300", CurrencyCode.USD)

        assert money.amount == Decimal("1.2300")
        assert money.amount.as_tuple().exponent == -4

    def test_currency_is_validated(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money.of("10.00", cast(Any, "USD"))

    def test_float_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money.of(cast(Any, 12.34), CurrencyCode.USD)

    def test_hash_and_equality(self) -> None:
        first = Money.of("10.00", CurrencyCode.USD)
        second = Money.of(Decimal("10.00"), CurrencyCode.USD)

        assert first == second
        assert hash(first) == hash(second)
        assert len({first, second}) == 1
