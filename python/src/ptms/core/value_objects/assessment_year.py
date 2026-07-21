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
