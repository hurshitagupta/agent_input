import pytest

from input_schema import InputRequest, parse_input


def test_valid_input_is_parsed():
    raw = {"text": "Plan a report"}

    result = parse_input(raw)

    assert isinstance(result, InputRequest)
    assert result.text == "Plan a report"


def test_protected_field_is_rejected():
    raw = {"text": "Plan a report", "tenant": "fake-tenant"}

    with pytest.raises(ValueError, match="Protected fields cannot be supplied by user"):
        parse_input(raw)


def test_empty_text_is_rejected():
    raw = {"text": "   "}

    with pytest.raises(ValueError,match="text is required"):
        parse_input(raw)