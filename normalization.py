import re
import unicodedata

from input_schema import InputRequest, parse_input


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    # Convert Unicode text into a consistent form.
    text = unicodedata.normalize("NFKC", text)

    text = text.strip()

    # Replace repeated spaces, tabs, and newlines with one space.
    text = re.sub(r"\s+", " ", text)

    if not text:
        raise ValueError("text is empty after normalization")

    return text


def normalize_input(input_request: InputRequest) -> InputRequest:
    normalized_text = normalize_text(input_request.text)

    return InputRequest(text=normalized_text)


if __name__ == "__main__":
    print("=== NORMALIZATION DEMO ===")

    raw_input = {"text": "   Plan    a\nreport\tfor   sales   "}

    print("\nRaw input:")
    print(repr(raw_input["text"]))

    parsed = parse_input(raw_input)
    normalized = normalize_input(parsed)

    print("\nNormalized input:")
    print(normalized)

    print("\nFailure case:")

    try:
        normalize_text("   \n\t   ")
    except ValueError as error:
        print("Rejected:", error)