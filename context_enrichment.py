from dataclasses import dataclass
from uuid import uuid4

from input_schema import InputRequest
from validation import validate_input


@dataclass
class TrustedContext:
    tenant: str
    user: str
    locale: str
    policy: str


@dataclass
class EnrichedInput:
    request_id: str
    text: str
    tenant: str
    user: str
    locale: str
    policy: str
    provenance: dict[str, str]


def enrich_context(input_request: InputRequest, trusted_context: TrustedContext) -> EnrichedInput:

    validate_input(input_request)

    if not trusted_context.tenant:
        raise ValueError("trusted tenant is required")

    if not trusted_context.user:
        raise ValueError("trusted user is required")

    if not trusted_context.locale:
        raise ValueError("trusted locale is required")

    if not trusted_context.policy:
        raise ValueError("trusted policy is required")

    request_id = str(uuid4())

    provenance = {
        "text": "user_input",
        "request_id": "system_generated",
        "tenant": "trusted_context",
        "user": "trusted_context",
        "locale": "trusted_context",
        "policy": "trusted_context",
    }

    return EnrichedInput(
        request_id=request_id,
        text=input_request.text,
        tenant=trusted_context.tenant,
        user=trusted_context.user,
        locale=trusted_context.locale,
        policy=trusted_context.policy,
        provenance=provenance,
    )


if __name__ == "__main__":
    print("=== CONTEXT ENRICHMENT DEMO ===")

    input_request = InputRequest(
        text="Plan a monthly sales report"
    )

    trusted_context = TrustedContext(
        tenant="demo-tenant",
        user="user-101",
        locale="en-IN",
        policy="standard-policy"
    )

    enriched = enrich_context(input_request, trusted_context)

    print("\nSuccess case:")
    print("Request ID:", enriched.request_id)
    print("Text:", enriched.text)
    print("Tenant:", enriched.tenant)
    print("User:", enriched.user)
    print("Locale:", enriched.locale)
    print("Policy:", enriched.policy)

    print("\nProvenance:")
    for field, source in enriched.provenance.items():
        print(f"{field}: {source}")

    print("\nFailure case:")

    invalid_context = TrustedContext(
        tenant="",
        user="user-101",
        locale="en-IN",
        policy="standard-policy"
    )

    try:
        enrich_context(input_request, invalid_context)
    except ValueError as error:
        print("Rejected:", error)