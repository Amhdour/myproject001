import pytest

from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.denials import raise_security_denial
from backend.security_layer.runtime.denials import safe_denial_message


def test_safe_denial_does_not_leak_sensitive_details() -> None:
    message = safe_denial_message("tenant_abc secret prompt text")
    assert "tenant_abc" not in message
    assert "secret" not in message


def test_denial_message_no_tenant_leak() -> None:
    message = safe_denial_message("missing_tenant")
    assert "tenant-123" not in message


def test_denial_message_no_document_name_leak() -> None:
    message = safe_denial_message("doc confidential-roadmap.pdf")
    assert "confidential-roadmap.pdf" not in message


def test_denial_message_no_tool_name_leak() -> None:
    message = safe_denial_message("tool_call internal_admin_tool")
    assert "internal_admin_tool" not in message


def test_denial_message_no_mcp_server_leak() -> None:
    message = safe_denial_message("mcp server prod-internal-mcp")
    assert "prod-internal-mcp" not in message


def test_denial_message_no_raw_prompt_leak() -> None:
    message = safe_denial_message("prompt: summarize merger strategy")
    assert "summarize merger strategy" not in message


def test_raise_security_denial() -> None:
    with pytest.raises(SecurityDenial):
        raise_security_denial("missing_subject")
