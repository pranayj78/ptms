"""
FinancialYear value object.

Represents the Indian financial year as an immutable,
ordered domain primitive.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from ptms.core.exceptions import InvalidFinancialYearError
from ptms.core.value_objects._year_utils import (
    parse_year_range,
    validate_start_year,
)

if TYPE_CHECKING:
    from ptms.core.value_objects.assessment_year import AssessmentYear

MIN_SUPPORTED_START_YEAR = 1961
MAX_SUPPORTED_START_YEAR = 9998


@dataclass(
    frozen=True,
    slots=True,
    order=True,
)
class FinancialYear:
    start_year: int

    @classmethod
    def of(cls, start_year: int) -> Self:
        """Construct FinancialYear from a start year."""

        return cls(start_year=start_year)

    @classmethod
    def parse(cls, value: object) -> Self:
        """Parse FinancialYear from a start year value.

        This parser currently supports:
        - 2025 (int)
        - "2025" (str)
        - "2025-2026" (str)
        """

        if type(value) is int:
            return cls.of(value)

        if type(value) is str:
            normalized = value.strip()
            if normalized.isdigit():
                return cls._parse_numeric_year(normalized)

            elif normalized.count("-") == 1:
                return cls._parse_year_range(normalized)

        raise InvalidFinancialYearError(
            "FinancialYear.parse currently supports int year values, numeric year strings, "
            "and 'YYYY-YYYY' strings; for example 2025, '2025', or '2025-2026'."
        )

    @classmethod
    def _parse_numeric_year(cls, value: str) -> Self:
        return cls.of(int(value))

    @classmethod
    def _parse_year_range(cls, value: str) -> Self:
        start_year = parse_year_range(value, InvalidFinancialYearError)
        return cls.of(start_year)

    def __post_init__(self) -> None:
        validate_start_year(
            self.start_year,
            MIN_SUPPORTED_START_YEAR,
            MAX_SUPPORTED_START_YEAR,
            InvalidFinancialYearError,
            "FinancialYear",
        )

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def __repr__(self) -> str:
        return f"FinancialYear({self.start_year})"

    @property
    def end_year(self) -> int:
        return self.start_year + 1

    @property
    def assessment_year(self) -> AssessmentYear:
        from ptms.core.value_objects.assessment_year import AssessmentYear

        return AssessmentYear.of(self.start_year + 1)
