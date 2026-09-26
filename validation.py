from dataclasses import dataclass

from input_schema import InputRequest, parse_input
from normalization import normalize_input


MAX_TEXT_LENGTH = 2000


@dataclass
class ValidationResult:
    valid: bool
    text_length: int
    message: str


def validate_input(input_request: InputRequest) -> ValidationResult:
    text = input_request.text

    if not isinstance(text, str):
        raise ValueError("text must be a string")

    text_length = len(text)

    if text_length == 0:
        raise ValueError("text is required")

    if text_length > MAX_TEXT_LENGTH:
        raise ValueError(f"text must be <= {MAX_TEXT_LENGTH} characters")

    return ValidationResult(
        valid=True,
        text_length=text_length,
        message="Input passed validation"
    )


if __name__ == "__main__":
    print("=== VALIDATION DEMO ===")

    raw_input = {
        "text": "   Plan a monthly sales report   "
    }

    parsed = parse_input(raw_input)
    normalized = normalize_input(parsed)
    result = validate_input(normalized)

    print("\nSuccess case:")
    print("Text:", normalized.text)
    print("Text length:", result.text_length)
    print("Valid:", result.valid)
    print("Message:", result.message)

    print("\nFailure case:")

    too_long_input = InputRequest(text="A" * 2001)

    try:
        validate_input(too_long_input)
    except ValueError as error:
        print("Text length:", len(too_long_input.text))
        print("Rejected:", error)