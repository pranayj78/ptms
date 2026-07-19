"""
Money value object.

Represents an immutable monetary amount
associated with a specific currency.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from ptms.core.enums import CurrencyCode
from ptms.core.exceptions import InvalidMoneyError


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

    amount: Decimal
    currency: CurrencyCode

    def __post_init__(self) -> None:
        """
        Normalize and validate construction.
        """

        if not isinstance(self.amount, Decimal):
            raise InvalidMoneyError("Money.amount must be a Decimal.")

    @classmethod
    def of(
        cls,
        amount: str | int | Decimal,
        currency: CurrencyCode,
    ) -> Money:
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
