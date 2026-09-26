from rejection_evidence import process_input


def test_valid_input_is_accepted():
    raw_input = {"text": "Plan a monthly sales report"}

    result = process_input(raw_input)

    assert result["status"] == "accepted"
    assert result["text"] == "Plan a monthly sales report"
    assert result["text_length"] == len("Plan a monthly sales report")


def test_long_input_creates_rejection_evidence():
    raw_input = {"text": "A" * 2001}

    result = process_input(raw_input)

    assert result["status"] == "rejected"
    assert result["stage"] == "input_processing"
    assert result["reason"] == ("text must be <= 2000 characters")
    assert result["timestamp"]


def test_protected_field_creates_rejection_evidence():
    raw_input = {"text": "Plan a report", "tenant": "fake-tenant"}

    result = process_input(raw_input)

    assert result["status"] == "rejected"
    assert result["stage"] == "input_processing"
    assert ("Protected fields cannot be supplied by user" in result["reason"])


def test_empty_input_creates_rejection_evidence():
    raw_input = {"text": ""}

    result = process_input(raw_input)

    assert result["status"] == "rejected"
    assert result["reason"] == "text is required"