"""
Exceptions related to monetary value objects.
"""

from __future__ import annotations

from ptms.core.exceptions.base import PTMSError


class MoneyError(PTMSError):
    """Base class for money-related exceptions."""


class CurrencyMismatchError(MoneyError):
    """
    Raised when attempting operations on Money
    instances with different currencies.
    """


class InvalidMoneyError(MoneyError):
    """
    Raised when an invalid monetary amount
    is used to construct a Money object.
    """
