"""
AssessmentYear value object.

Represents the Indian assessment year as an immutable,
ordered domain primitive.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from ptms.core.exceptions import InvalidAssessmentYearError
from ptms.core.value_objects._year_utils import (
    parse_year_range,
    validate_start_year,
)

if TYPE_CHECKING:
    from ptms.core.value_objects.financial_year import FinancialYear

MIN_SUPPORTED_START_YEAR = 1962
MAX_SUPPORTED_START_YEAR = 9999
INVALID_AY_FORMAT = "Invalid AssessmentYear format. Expected 'AY YYYY-YY'."


@dataclass(
    frozen=True,
    slots=True,
    order=True,
)
class AssessmentYear:
    start_year: int

    @classmethod
    def of(cls, start_year: int) -> Self:
        """Construct AssessmentYear from a start year."""

        return cls(start_year=start_year)

    @classmethod
    def parse(cls, value: object) -> Self:
        """Parse AssessmentYear from a start year value.

        This parser currently supports:
        - 2026 (int)
        - "2026" (str)
        - "AY 2026-27" (str)
        - "2026-2027" (str)
        """

        if type(value) is int:
            return cls.of(value)

        if type(value) is str:
            normalized = value.strip()
            if normalized.isdigit():
                return cls._parse_numeric_year(normalized)

            if normalized.startswith("AY "):
                return cls._parse_ay_string(normalized)

            elif normalized.count("-") == 1:
                return cls._parse_year_range(normalized)

        raise InvalidAssessmentYearError(
            "AssessmentYear.parse currently supports int year values, numeric year strings, "
            "'AY YYYY-YY' strings, and 'YYYY-YYYY' strings; for example 2026, '2026', "
            "'AY 2026-27', or '2026-2027'."
        )

    @classmethod
    def _parse_numeric_year(cls, value: str) -> Self:
        return cls.of(int(value))

    @classmethod
    def _parse_ay_string(cls, value: str) -> Self:
        payload = value.removeprefix("AY ")
        try:
            start_part, end_suffix_part = payload.split("-")
        except ValueError as exc:
            raise InvalidAssessmentYearError(INVALID_AY_FORMAT) from exc

        if len(start_part) != 4 or not start_part.isdigit():
            raise InvalidAssessmentYearError(INVALID_AY_FORMAT)

        if len(end_suffix_part) != 2 or not end_suffix_part.isdigit():
            raise InvalidAssessmentYearError(INVALID_AY_FORMAT)

        start_year = int(start_part)
        expected_suffix = f"{(start_year + 1) % 100:02d}"
        if end_suffix_part != expected_suffix:
            raise InvalidAssessmentYearError(
                "AssessmentYear end-year suffix does not match start year."
            )

        return cls.of(start_year)

    @classmethod
    def _parse_year_range(cls, value: str) -> Self:
        start_year = parse_year_range(value, InvalidAssessmentYearError)
        return cls.of(start_year)

    def __post_init__(self) -> None:
        validate_start_year(
            self.start_year,
            MIN_SUPPORTED_START_YEAR,
            MAX_SUPPORTED_START_YEAR,
            InvalidAssessmentYearError,
            "AssessmentYear",
        )

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def __repr__(self) -> str:
        return f"AssessmentYear({self.start_year})"

    @property
    def end_year(self) -> int:
        return self.start_year + 1

    @property
    def financial_year(self) -> FinancialYear:
        from ptms.core.value_objects.financial_year import FinancialYear

        return FinancialYear.of(self.start_year - 1)
