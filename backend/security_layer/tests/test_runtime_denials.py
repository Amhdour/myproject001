import json

import pytest

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import SafeErrorCode
from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.denials import approval_required_payload
from backend.security_layer.runtime.denials import build_denial_payload
from backend.security_layer.runtime.denials import policy_engine_unavailable_payload
from backend.security_layer.runtime.denials import raise_security_denial
from backend.security_layer.runtime.denials import rate_or_quota_blocked_payload
from backend.security_layer.runtime.denials import redact_for_denial
from backend.security_layer.runtime.denials import safe_admin_summary
from backend.security_layer.runtime.denials import safe_denial_message
from backend.security_layer.runtime.denials import validation_failed_payload


ALL_CATEGORIES = list(DenialCategory)
ALL_SAFE_CODES = set(SafeErrorCode)
SENSITIVE_VALUES = [
    "tenant-123",
    "user-456",
    "confidential-roadmap.pdf",
    "chunk text: merger details",
    "tool_args={'password':'abc'}",
    "tool secret",
    "mcp://internal-prod",
    "/sandbox/private/secret",
    "prompt: summarize private merger",
    "policy graph edge deny_internal",
    "RuntimeError: boom",
    "credential=xyz token=abc api_key=sk-secret",
]


def test_all_denial_categories_have_safe_message_and_error_code() -> None:
    for category in ALL_CATEGORIES:
        payload = build_denial_payload(category)
        assert payload.message == safe_denial_message(category)
        assert payload.error_code in ALL_SAFE_CODES
        assert payload.error_code.value.startswith("security_")


def test_raise_security_denial_for_all_categories() -> None:
    for category in ALL_CATEGORIES:
        with pytest.raises(SecurityDenial) as ex:
            raise_security_denial(category)
        assert ex.value.payload.category == category
        assert ex.value.message == safe_denial_message(category)


def test_safe_admin_summary_redacts_reason() -> None:
    summary = safe_admin_summary(DenialCategory.POLICY_DENIED, reason={"api_key": "secret"})
    assert summary.startswith("safe_denial:policy_denied")
    assert "api_key" not in summary
    assert "secret" not in summary
    assert summary.endswith("[redacted]")


def test_redact_for_denial_filters_supported_types() -> None:
    payload = build_denial_payload(DenialCategory.ACCESS_DENIED)
    assert redact_for_denial(None) == ""
    assert redact_for_denial(Exception("boom")) == "[redacted]"
    assert redact_for_denial(payload) == "[redacted]"
    assert redact_for_denial({"k": "v"}) == "[redacted]"


def test_payload_helpers_structured_and_safe() -> None:
    approval = approval_required_payload({"tool": "internal_admin_tool"})
    validation = validation_failed_payload("api_key=secret")
    unavailable = policy_engine_unavailable_payload(Exception("db password leaked"))
    rate = rate_or_quota_blocked_payload("tenant-123")

    assert approval["approval_required"] is True
    assert approval["approval_status"] == "pending"

    for payload in [approval, validation, unavailable, rate]:
        assert set(["category", "error_code", "message", "admin_summary"]).issubset(payload.keys())
        text = " ".join(str(v) for v in payload.values())
        for sensitive in SENSITIVE_VALUES:
            assert sensitive not in text


def test_payload_helpers_forbidden_detail_filtering_and_json_serializable() -> None:
    payloads = [
        approval_required_payload("credential=abc token=def"),
        validation_failed_payload("password=hunter2"),
        policy_engine_unavailable_payload(RuntimeError("api_key=sk-live")),
        rate_or_quota_blocked_payload({"tenant": "tenant-123", "secret": "x"}),
    ]
    for payload in payloads:
        dumped = json.dumps(payload)
        assert dumped
        assert "api_key" not in dumped
        assert "password" not in dumped
        assert "token=" not in dumped


def test_denial_messages_do_not_leak_sensitive_input_reason() -> None:
    for category in ALL_CATEGORIES:
        for sensitive in SENSITIVE_VALUES:
            payload = build_denial_payload(category, sensitive)
            user_text = payload.message
            assert sensitive not in user_text
            assert payload.admin_summary.endswith("[redacted]")
