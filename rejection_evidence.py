from dataclasses import dataclass
from datetime import datetime, timezone

from input_schema import parse_input
from normalization import normalize_input
from validation import validate_input


@dataclass
class RejectionRecord:
    status: str
    stage: str
    reason: str
    timestamp: str


def process_input(raw: dict) -> dict:
    try:
        parsed = parse_input(raw)
        normalized = normalize_input(parsed)
        validation = validate_input(normalized)

        return {
            "status": "accepted",
            "text": normalized.text,
            "text_length": validation.text_length,
            "message": validation.message,
        }

    except ValueError as error:
        rejection = RejectionRecord(
            status="rejected",
            stage="input_processing",
            reason=str(error),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        return {
            "status": rejection.status,
            "stage": rejection.stage,
            "reason": rejection.reason,
            "timestamp": rejection.timestamp,
        }


if __name__ == "__main__":
    print("=== REJECTION EVIDENCE DEMO ===")

    valid_input = { "text": "Plan a monthly sales report" }

    print("\nSuccess case:")
    success_result = process_input(valid_input)

    for key, value in success_result.items():
        print(f"{key}: {value}")

    invalid_input = {"text": "A" * 2001}

    print("\nFailure case:")
    rejection_result = process_input(invalid_input)

    for key, value in rejection_result.items():
        print(f"{key}: {value}")