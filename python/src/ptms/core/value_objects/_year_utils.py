"""Internal year validation and parsing utilities.

Shared helpers for AssessmentYear and FinancialYear value objects.
Not a public API — prefixed with underscore.
"""

from __future__ import annotations


def validate_start_year(
    start_year: int,
    min_year: int,
    max_year: int,
    error_cls: type[Exception],
    class_name: str,
) -> None:
    if type(start_year) is not int:
        raise error_cls(f"{class_name}.start_year must be an int.")

    if start_year < min_year:
        raise error_cls(f"{class_name}.start_year must be >= {min_year}.")

    if start_year > max_year:
        raise error_cls(f"{class_name}.start_year must be <= {max_year}.")


def validate_consecutive_years(start_year: int, end_year: int, error_cls: type[Exception]) -> None:
    if end_year != start_year + 1:
        raise error_cls("End year must be exactly one year after the start year.")


def parse_year_range(value: str, error_cls: type[Exception]) -> int:
    try:
        start_part, end_part = value.split("-")
    except ValueError as exc:
        raise error_cls("Invalid year range. Expected 'YYYY-YYYY'.") from exc

    if len(start_part) != 4 or not start_part.isdigit():
        raise error_cls("Invalid year range. Expected 'YYYY-YYYY'.")

    if len(end_part) != 4 or not end_part.isdigit():
        raise error_cls("Invalid year range. Expected 'YYYY-YYYY'.")

    start_year = int(start_part)
    end_year = int(end_part)
    validate_consecutive_years(start_year, end_year, error_cls)
    return start_year
