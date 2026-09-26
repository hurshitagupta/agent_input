import pytest

from input_schema import InputRequest
from normalization import normalize_input, normalize_text


def test_text_is_normalized():
    input_request = InputRequest(text="   Plan    a\nreport\tfor   sales   ")

    result = normalize_input(input_request)

    assert result.text == "Plan a report for sales"


def test_normalization_preserves_normal_text():
    input_request = InputRequest(text="Plan a sales report")

    result = normalize_input(input_request)

    assert result.text == "Plan a sales report"


def test_empty_text_after_normalization_is_rejected():
    with pytest.raises(ValueError, match="text is empty after normalization"):
        normalize_text("   \n\t   ")