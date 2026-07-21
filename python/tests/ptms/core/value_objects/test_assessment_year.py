from dataclasses import FrozenInstanceError, fields
from typing import Any, cast

import pytest
from ptms.core.exceptions import InvalidAssessmentYearError
from ptms.core.value_objects import AssessmentYear
from ptms.core.value_objects.assessment_year import (
    MAX_SUPPORTED_START_YEAR,
    MIN_SUPPORTED_START_YEAR,
)


def test_construction_with_valid_start_year() -> None:
    ay = AssessmentYear(start_year=2026)

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_factory_construction_with_valid_start_year() -> None:
    ay = AssessmentYear.of(2026)

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_repr_contains_start_year() -> None:
    ay = AssessmentYear.of(2026)

    assert "2026" in repr(ay)


def test_end_year_is_derived_and_not_stored_field() -> None:
    ay_fields = fields(AssessmentYear)

    assert len(ay_fields) == 1
    assert ay_fields[0].name == "start_year"


def test_start_year_must_be_int() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear(start_year=cast(Any, "2026"))


def test_bool_is_rejected_as_start_year() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear(start_year=cast(Any, True))


def test_factory_rejects_bool_start_year() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.of(cast(Any, True))


def test_start_year_must_be_greater_than_or_equal_to_minimum_supported() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear(start_year=MIN_SUPPORTED_START_YEAR - 1)


def test_start_year_equal_to_minimum_supported_is_valid() -> None:
    ay = AssessmentYear(start_year=MIN_SUPPORTED_START_YEAR)

    assert ay.start_year == MIN_SUPPORTED_START_YEAR
    assert ay.end_year == MIN_SUPPORTED_START_YEAR + 1


def test_start_year_must_be_less_than_or_equal_to_maximum_supported() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear(start_year=MAX_SUPPORTED_START_YEAR + 1)


def test_factory_respects_bounds_validation() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.of(MAX_SUPPORTED_START_YEAR + 1)


def test_start_year_equal_to_maximum_supported_is_valid() -> None:
    ay = AssessmentYear(start_year=MAX_SUPPORTED_START_YEAR)

    assert ay.start_year == MAX_SUPPORTED_START_YEAR
    assert ay.end_year == MAX_SUPPORTED_START_YEAR + 1


def test_object_is_immutable() -> None:
    ay = AssessmentYear(start_year=2026)
    mutable_ref = cast(Any, ay)

    with pytest.raises(FrozenInstanceError):
        mutable_ref.start_year = 2030


def test_equality_uses_start_year() -> None:
    left = AssessmentYear(start_year=2026)
    right = AssessmentYear(start_year=2026)

    assert left == right
    assert hash(left) == hash(right)


def test_ordering_is_chronological() -> None:
    previous = AssessmentYear(start_year=2025)
    current = AssessmentYear(start_year=2026)

    assert previous < current
    assert current > previous
