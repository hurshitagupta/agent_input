import pytest

from input_schema import InputRequest
from context_enrichment import (TrustedContext, enrich_context)


def test_context_is_added_successfully():
    input_request = InputRequest(text="Plan a monthly sales report")

    trusted_context = TrustedContext(
        tenant="demo-tenant",
        user="user-101",
        locale="en-IN",
        policy="standard-policy"
    )

    result = enrich_context(input_request, trusted_context)

    assert result.text == "Plan a monthly sales report"
    assert result.tenant == "demo-tenant"
    assert result.user == "user-101"
    assert result.locale == "en-IN"
    assert result.policy == "standard-policy"
    assert result.request_id


def test_provenance_is_recorded():
    input_request = InputRequest( text="Plan a report" )

    trusted_context = TrustedContext(
        tenant="demo-tenant",
        user="user-101",
        locale="en-IN",
        policy="standard-policy"
    )

    result = enrich_context(input_request, trusted_context)

    assert result.provenance["text"] == "user_input"
    assert result.provenance["request_id"] == "system_generated"
    assert result.provenance["tenant"] == "trusted_context"
    assert result.provenance["user"] == "trusted_context"
    assert result.provenance["locale"] == "trusted_context"
    assert result.provenance["policy"] == "trusted_context"


def test_missing_trusted_tenant_is_rejected():
    input_request = InputRequest(text="Plan a report")

    trusted_context = TrustedContext(
        tenant="",
        user="user-101",
        locale="en-IN",
        policy="standard-policy"
    )

    with pytest.raises(ValueError, match="trusted tenant is required"):
        enrich_context(input_request, trusted_context)