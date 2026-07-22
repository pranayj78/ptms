"""
AssessmentYear value object.

Represents the Indian assessment year as an immutable,
ordered domain primitive.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from ptms.core.exceptions import InvalidAssessmentYearError

# Earliest supported AY start year in PTMS.
MIN_SUPPORTED_START_YEAR = 1962
# Explicit upper bound for supported AY start year.
MAX_SUPPORTED_START_YEAR = 9999
INVALID_AY_FORMAT = "Invalid AssessmentYear format. Expected 'AY YYYY-YY'."
INVALID_YEAR_RANGE_FORMAT = "Invalid AssessmentYear format. Expected 'YYYY-YYYY'."


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
        try:
            start_part, end_part = value.split("-")
        except ValueError as exc:
            raise InvalidAssessmentYearError(INVALID_YEAR_RANGE_FORMAT) from exc

        if len(start_part) != 4 or not start_part.isdigit():
            raise InvalidAssessmentYearError(INVALID_YEAR_RANGE_FORMAT)

        if len(end_part) != 4 or not end_part.isdigit():
            raise InvalidAssessmentYearError(INVALID_YEAR_RANGE_FORMAT)

        start_year = int(start_part)
        end_year = int(end_part)
        cls._validate_year_range(start_year, end_year)
        return cls.of(start_year)

    @staticmethod
    def _validate_year_range(start_year: int, end_year: int) -> None:
        if end_year != start_year + 1:
            raise InvalidAssessmentYearError(
                "AssessmentYear end year must be exactly one year after the start year."
            )

    def __post_init__(self) -> None:
        if type(self.start_year) is not int:
            raise InvalidAssessmentYearError("AssessmentYear.start_year must be an int.")

        if self.start_year < MIN_SUPPORTED_START_YEAR:
            raise InvalidAssessmentYearError(
                "AssessmentYear.start_year must be greater than or equal to "
                f"{MIN_SUPPORTED_START_YEAR}."
            )

        if self.start_year > MAX_SUPPORTED_START_YEAR:
            raise InvalidAssessmentYearError(
                "AssessmentYear.start_year must be less than or equal to "
                f"{MAX_SUPPORTED_START_YEAR}."
            )

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def __repr__(self) -> str:
        return f"AssessmentYear({self.start_year})"

    @property
    def end_year(self) -> int:
        return self.start_year + 1
