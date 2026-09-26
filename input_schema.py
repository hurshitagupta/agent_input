from dataclasses import dataclass
from typing import Any


PROTECTED_FIELDS = {"tenant", "user", "locale", "policy"}


@dataclass
class InputRequest:
    text: str


def parse_input(raw: dict[str, Any]) -> InputRequest:
    if not isinstance(raw, dict):
        raise ValueError("Input must be a dictionary")

    protected_found = PROTECTED_FIELDS.intersection(raw.keys())

    if protected_found:
        raise ValueError(
            f"Protected fields cannot be supplied by user: "
            f"{sorted(protected_found)}"
        )

    text = raw.get("text")

    if not isinstance(text, str):
        raise ValueError("text must be a string")

    text = text.strip()

    if not text:
        raise ValueError("text is required")

    return InputRequest(text=text)


if __name__ == "__main__":
    print("=== INPUT SCHEMA DEMO ===")

    valid_input = {"text": "Plan a report"}

    print("\nValid input:")
    print(valid_input)

    parsed = parse_input(valid_input)

    print("Parsed input:")
    print(parsed)

    invalid_input = {"text": "Plan a report", "tenant": "fake-tenant"}

    print("\nInvalid input:")
    print(invalid_input)

    try:
        parse_input(invalid_input)
    except ValueError as error:
        print("Rejected:", error)