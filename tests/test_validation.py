import pytest

from input_schema import InputRequest
from validation import MAX_TEXT_LENGTH, validate_input


def test_valid_input_passes_validation():
    input_request = InputRequest(text="Plan a monthly sales report")

    result = validate_input(input_request)

    assert result.valid is True
    assert result.text_length == len(input_request.text)
    assert result.message == "Input passed validation"


def test_maximum_length_is_allowed():
    input_request = InputRequest(text="A" * MAX_TEXT_LENGTH)

    result = validate_input(input_request)

    assert result.valid is True
    assert result.text_length == MAX_TEXT_LENGTH


def test_text_over_limit_is_rejected():
    input_request = InputRequest(text="A" * (MAX_TEXT_LENGTH + 1))

    with pytest.raises(ValueError, match="text must be <= 2000 characters"):
        validate_input(input_request)


def test_empty_text_is_rejected():
    input_request = InputRequest(text="")

    with pytest.raises(ValueError, match="text is required"):
        validate_input(input_request)