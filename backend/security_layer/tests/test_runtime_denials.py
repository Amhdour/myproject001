import pytest

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.denials import approval_required_payload
from backend.security_layer.runtime.denials import build_denial_payload
from backend.security_layer.runtime.denials import policy_engine_unavailable_payload
from backend.security_layer.runtime.denials import raise_security_denial
from backend.security_layer.runtime.denials import rate_or_quota_blocked_payload
from backend.security_layer.runtime.denials import safe_denial_message
from backend.security_layer.runtime.denials import validation_failed_payload


ALL_CATEGORIES = list(DenialCategory)
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
        assert payload.error_code.value.startswith("security_")


def test_raise_security_denial_for_all_categories() -> None:
    for category in ALL_CATEGORIES:
        with pytest.raises(SecurityDenial) as ex:
            raise_security_denial(category)
        assert ex.value.payload.category == category
        assert ex.value.message == safe_denial_message(category)


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


def test_denial_messages_do_not_leak_sensitive_input_reason() -> None:
    for category in ALL_CATEGORIES:
        for sensitive in SENSITIVE_VALUES:
            payload = build_denial_payload(category, sensitive)
            user_text = payload.message
            assert sensitive not in user_text
            assert payload.admin_summary.endswith("[redacted]")
