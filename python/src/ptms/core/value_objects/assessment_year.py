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

        This incremental parser currently supports:
        - 2026 (int)
        - "2026" (str)
        - "AY 2026-27" (str)
        """

        if type(value) is int:
            return cls.of(value)

        if type(value) is str:
            normalized = value.strip()
            if normalized.isdigit():
                return cls.of(int(normalized))

            if normalized.startswith("AY "):
                payload = normalized.removeprefix("AY ")
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

        raise InvalidAssessmentYearError(
            "AssessmentYear.parse currently supports int year values, numeric year strings, "
            "and 'AY YYYY-YY' strings; for example 2026, '2026', or 'AY 2026-27'."
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

    @property
    def end_year(self) -> int:
        return self.start_year + 1
