"""
Base exception hierarchy for PTMS.

All domain-specific exceptions should inherit from PTMSError.
"""

from __future__ import annotations


class PTMSError(Exception):
    """Base class for all PTMS domain exceptions."""
