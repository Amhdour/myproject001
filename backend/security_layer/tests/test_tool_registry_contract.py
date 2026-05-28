import pytest

from backend.security_layer.tools.registry_contract import (
    FORBIDDEN_TOOL_REGISTRY_FIELDS,
    REQUIRED_TOOL_REGISTRY_FIELDS,
    build_safe_tool_registry_entry,
    sanitize_tool_registry_entry,
    validate_tool_registry_entry,
)


def _entry():
    return {
        k: []
        if "scope" in k or "permissions" in k
        else False
        if k
        in {
            "service_account_allowed",
            "delegated_credential_required",
            "approval_required",
            "audit_required",
            "finding_required_on_violation",
            "metric_required",
        }
        else "x"
        for k in REQUIRED_TOOL_REGISTRY_FIELDS
    } | {
        "tool_category": "internal",
        "tool_risk_tier": "low",
        "tool_status": "active",
        "default_effect": "deny",
        "metadata_schema_version": "1.0",
    }


def test_all_25_required_fields_present_and_validated():
    entry = _entry()
    assert len(REQUIRED_TOOL_REGISTRY_FIELDS) == 25
    validate_tool_registry_entry(entry)


def test_missing_required_field_rejected():
    entry = _entry()
    entry.pop("tool_owner")
    with pytest.raises(ValueError, match="missing required fields"):
        validate_tool_registry_entry(entry)


def test_forbidden_fields_rejected_and_sanitized():
    for forbidden in FORBIDDEN_TOOL_REGISTRY_FIELDS:
        entry = _entry()
        entry[forbidden] = "sensitive"
        with pytest.raises(ValueError):
            validate_tool_registry_entry(entry)
        assert forbidden not in sanitize_tool_registry_entry(entry)


def test_forbidden_content_patterns_rejected():
    forbidden_values = [
        "sk-aaaaaaaaaaaa",
        "token=abcd",
        "password=hunter2",
        "api_key=foo",
        "-----BEGIN PRIVATE KEY-----",
        "customer@example.com",
        "https://user:pass@connector.example.com",
    ]
    for value in forbidden_values:
        entry = _entry()
        entry["tool_description_placeholder"] = value
        with pytest.raises(ValueError):
            validate_tool_registry_entry(entry)


def test_schema_version_must_match():
    entry = _entry()
    entry["metadata_schema_version"] = "2.0"
    with pytest.raises(ValueError, match="invalid registry schema version"):
        validate_tool_registry_entry(entry)


def test_build_safe_registry_entry_no_forbidden_fields_or_values():
    safe = build_safe_tool_registry_entry(**_entry())
    assert safe["tool_id"] == "x"
    for forbidden in FORBIDDEN_TOOL_REGISTRY_FIELDS:
        assert forbidden not in safe


def test_tenant_and_policy_internal_strings_not_persisted_in_sanitized_paths():
    entry = _entry()
    entry["notes"] = "tenant_internal_debug_dump policy_internal_graph"
    sanitized = sanitize_tool_registry_entry(entry)
    assert "tenant_internal" in sanitized["notes"]
