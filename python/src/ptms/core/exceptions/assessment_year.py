"""
Exceptions related to AssessmentYear value objects.
"""

from __future__ import annotations

from ptms.core.exceptions.base import PTMSError


class AssessmentYearError(PTMSError):
    """Base class for AssessmentYear-related exceptions."""


class InvalidAssessmentYearError(AssessmentYearError):
    """Raised when an invalid assessment year is used to construct the object."""
