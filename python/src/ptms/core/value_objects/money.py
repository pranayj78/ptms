"""
Money value object.

Represents an immutable monetary amount
associated with a specific currency.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from types import NotImplementedType
from typing import Self

from ptms.core.enums import CurrencyCode
from ptms.core.exceptions import CurrencyMismatchError, InvalidMoneyError


@dataclass(frozen=True, slots=True)
class Money:
    """
    Immutable monetary value.

    A Money object consists of:

    - amount
    - currency

    and forms the foundation of all financial
    calculations inside PTMS.
    """

    # Future enhancement:
    # replace with Money.zero(CurrencyCode.USD)

    amount: Decimal
    currency: CurrencyCode

    def __post_init__(self) -> None:
        """
        Normalize and validate construction.
        """

        if not isinstance(self.amount, Decimal):
            raise InvalidMoneyError("Money.amount must be a Decimal.")

        if not isinstance(self.currency, CurrencyCode):
            raise InvalidMoneyError("Money.currency must be a CurrencyCode.")

    # -----------------------------
    # Factory Methods
    # -----------------------------

    @classmethod
    def of(
        cls,
        amount: str | int | Decimal,
        currency: CurrencyCode,
    ) -> Self:
        """
        Construct Money from supported scalar types.
        """

        if isinstance(amount, float):
            raise InvalidMoneyError("Money.of does not accept float. Use str or Decimal instead.")

        try:
            decimal_amount = Decimal(amount)
        except (InvalidOperation, TypeError) as exc:
            raise InvalidMoneyError(f"Invalid monetary amount: {amount!r}") from exc

        return cls(
            amount=decimal_amount,
            currency=currency,
        )

    # -----------------------------
    # Arithmetic
    # -----------------------------

    def __add__(self, other: object) -> Self | NotImplementedType:
        """
        Return the sum of two Money values.

        Example:
            >>> salary = Money.of(amount="100", currency=CurrencyCode.USD)
            >>> bonus = Money.of(amount="50", currency=CurrencyCode.USD)
            >>> (salary + bonus).amount
            Decimal("150")
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)

        return self.__class__(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def __sub__(self, other: object) -> Self | NotImplementedType:
        """
        Return the difference between two Money values.

        Example:
            >>> salary = Money.of(amount="100", currency=CurrencyCode.USD)
            >>> tax = Money.of(amount="30", currency=CurrencyCode.USD)
            >>> (salary - tax).amount
            Decimal("70")
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)

        return self.__class__(
            amount=self.amount - other.amount,
            currency=self.currency,
        )

    # -----------------------------
    # Unary Operations
    # -----------------------------

    def __neg__(self) -> Self:
        """
        Return the additive inverse of Money.
        """

        return self.__class__(
            amount=-self.amount,
            currency=self.currency,
        )

    def __abs__(self) -> Self:
        """
        Return Money with absolute amount.
        """

        return self.__class__(
            amount=abs(self.amount),
            currency=self.currency,
        )

    # -----------------------------
    # Comparison
    # -----------------------------

    def __lt__(self, other: object) -> bool | NotImplementedType:
        """
        Return True if this monetary value is less than the other.
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: object) -> bool | NotImplementedType:
        """
        Return True if this monetary value is less than or equal to the other.
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: object) -> bool | NotImplementedType:
        """
        Return True if this monetary value is greater than the other.
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: object) -> bool | NotImplementedType:
        """
        Return True if this monetary value is greater than or equal to the other.
        """

        if not isinstance(other, Money):
            return NotImplemented

        self._assert_same_currency(other)
        return self.amount >= other.amount

    # -----------------------------
    # Internal Helpers
    # -----------------------------

    def _assert_same_currency(
        self,
        other: Money,
    ) -> None:
        """
        Ensure both Money objects use the same currency.
        """

        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "Money operations require matching currencies: "
                f"{self.currency.value} != {other.currency.value}"
            )
