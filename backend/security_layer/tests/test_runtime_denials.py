import pytest

from backend.security_layer.runtime.denials import SecurityDenial, raise_security_denial, safe_denial_message


def test_safe_denial_does_not_leak_sensitive_details() -> None:
    message = safe_denial_message("tenant_abc secret prompt text")
    assert "tenant_abc" not in message
    assert "secret" not in message


def test_raise_security_denial() -> None:
    with pytest.raises(SecurityDenial):
        raise_security_denial("missing_subject")
