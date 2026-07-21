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


def test_parse_accepts_int_start_year() -> None:
    ay = AssessmentYear.parse(2026)

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_parse_accepts_numeric_string_start_year() -> None:
    ay = AssessmentYear.parse("2026")

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_parse_accepts_canonical_ay_string() -> None:
    ay = AssessmentYear.parse("AY 2026-27")

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_parse_accepts_full_year_range_string() -> None:
    ay = AssessmentYear.parse("2026-2027")

    assert ay.start_year == 2026
    assert ay.end_year == 2027


def test_parse_accepts_minimum_supported_year_range_string() -> None:
    ay = AssessmentYear.parse("1962-1963")

    assert ay.start_year == 1962
    assert ay.end_year == 1963


def test_parse_accepts_century_wrap_year_range_string() -> None:
    ay = AssessmentYear.parse("2099-2100")

    assert ay.start_year == 2099
    assert ay.end_year == 2100


def test_parse_accepts_minimum_supported_ay_string() -> None:
    ay = AssessmentYear.parse("AY 1962-63")

    assert ay.start_year == 1962
    assert ay.end_year == 1963


def test_parse_accepts_century_wrap_ay_string() -> None:
    ay = AssessmentYear.parse("AY 2099-00")

    assert ay.start_year == 2099
    assert ay.end_year == 2100


def test_parse_rejects_missing_space_after_ay_prefix() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse("AY2026-27")


@pytest.mark.parametrize(
    "value",
    [
        "AY2026-27",
        "AY 2026/27",
        "AY2026",
        "AY 26-27",
        "AY 2026-2027",
    ],
)
def test_parse_rejects_invalid_ay_string_formats(value: str) -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse(value)


def test_parse_rejects_ay_string_with_mismatched_suffix() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse("AY 2026-28")


def test_parse_rejects_year_range_with_non_consecutive_end_year() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse("2026-2028")


def test_parse_rejects_year_range_with_short_start_year() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse("26-2027")


def test_parse_rejects_bool() -> None:
    with pytest.raises(InvalidAssessmentYearError):
        _ = AssessmentYear.parse(True)


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
