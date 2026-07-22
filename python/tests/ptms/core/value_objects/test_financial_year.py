from dataclasses import FrozenInstanceError
from typing import Any, cast

import pytest
from ptms.core.exceptions import InvalidFinancialYearError
from ptms.core.value_objects import AssessmentYear, FinancialYear
from ptms.core.value_objects.financial_year import (
    MAX_SUPPORTED_START_YEAR,
    MIN_SUPPORTED_START_YEAR,
)


def test_construction_with_valid_start_year() -> None:
    fy = FinancialYear(start_year=2025)

    assert fy.start_year == 2025
    assert fy.end_year == 2026


def test_factory_construction_with_valid_start_year() -> None:
    fy = FinancialYear.of(2025)

    assert fy.start_year == 2025
    assert fy.end_year == 2026


def test_end_year_is_derived() -> None:
    fy = FinancialYear.of(2025)

    assert fy.end_year == fy.start_year + 1


def test_parse_accepts_int_start_year() -> None:
    fy = FinancialYear.parse(2025)

    assert fy.start_year == 2025
    assert fy.end_year == 2026


def test_parse_accepts_numeric_string() -> None:
    fy = FinancialYear.parse("2025")

    assert fy.start_year == 2025


def test_parse_accepts_full_year_range_string() -> None:
    fy = FinancialYear.parse("2025-2026")

    assert fy.start_year == 2025
    assert fy.end_year == 2026


def test_parse_rejects_non_consecutive_years() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear.parse("2025-2027")


def test_parse_rejects_invalid_format() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear.parse("2025/2026")


def test_parse_rejects_bool() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear.parse(True)


def test_start_year_must_be_int() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear(start_year=cast(Any, "2025"))


def test_bool_rejected_as_start_year() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear(start_year=cast(Any, True))


def test_minimum_start_year_respected() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear(start_year=MIN_SUPPORTED_START_YEAR - 1)


def test_minimum_start_year_is_valid() -> None:
    fy = FinancialYear(start_year=MIN_SUPPORTED_START_YEAR)

    assert fy.start_year == MIN_SUPPORTED_START_YEAR


def test_maximum_start_year_respected() -> None:
    with pytest.raises(InvalidFinancialYearError):
        FinancialYear(start_year=MAX_SUPPORTED_START_YEAR + 1)


def test_maximum_start_year_is_valid() -> None:
    fy = FinancialYear(start_year=MAX_SUPPORTED_START_YEAR)

    assert fy.start_year == MAX_SUPPORTED_START_YEAR


def test_object_is_immutable() -> None:
    fy = FinancialYear(start_year=2025)
    mutable_ref = cast(Any, fy)

    with pytest.raises(FrozenInstanceError):
        mutable_ref.start_year = 2030


def test_equality_uses_start_year() -> None:
    left = FinancialYear(start_year=2025)
    right = FinancialYear(start_year=2025)

    assert left == right
    assert hash(left) == hash(right)


def test_ordering_is_chronological() -> None:
    previous = FinancialYear(start_year=2024)
    current = FinancialYear(start_year=2025)

    assert previous < current
    assert current > previous


class TestFinancialYearConversion:
    def test_financial_year_to_assessment_year(self) -> None:
        fy = FinancialYear.of(2025)

        ay = fy.assessment_year

        assert ay == AssessmentYear.of(2026)

    def test_assessment_year_to_financial_year(self) -> None:
        ay = AssessmentYear.of(2026)

        fy = ay.financial_year

        assert fy == FinancialYear.of(2025)

    def test_round_trip_from_financial_year(self) -> None:
        fy = FinancialYear.of(2025)

        assert fy.assessment_year.financial_year == fy

    def test_round_trip_from_assessment_year(self) -> None:
        ay = AssessmentYear.of(2026)

        assert ay.financial_year.assessment_year == ay

    def test_conversion_at_minimum_year(self) -> None:
        fy = FinancialYear.of(1962)

        ay = fy.assessment_year

        assert ay.start_year == 1963

    def test_conversion_at_maximum_year(self) -> None:
        ay = AssessmentYear.of(9998)

        fy = ay.financial_year

        assert fy.start_year == 9997

    def test_conversion_does_not_mutate_original(self) -> None:
        fy = FinancialYear.of(2025)
        ay = AssessmentYear.of(2026)

        _ = fy.assessment_year
        _ = ay.financial_year

        assert fy == FinancialYear.of(2025)
        assert ay == AssessmentYear.of(2026)
