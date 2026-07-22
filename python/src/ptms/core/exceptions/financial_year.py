"""
Exceptions related to FinancialYear value objects.
"""

from __future__ import annotations

from ptms.core.exceptions.base import PTMSError


class FinancialYearError(PTMSError):
    """Base class for FinancialYear-related exceptions."""


class InvalidFinancialYearError(FinancialYearError):
    """Raised when an invalid financial year is used to construct the object."""
