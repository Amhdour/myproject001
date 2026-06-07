from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any

import pytest

from onyx.security_layer import redaction
from onyx.security_layer.redaction import redact_mapping
from onyx.security_layer.redaction import redact_security_payload
from onyx.security_layer.redaction import redact_text
from onyx.security_layer.redaction import safe_metadata


@pytest.fixture(autouse=True)
def force_regex_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_find_spec(name: str, *args: object, **kwargs: object) -> object | None:
        return None

    monkeypatch.setattr(redaction, "_PRESIDIO_ENGINES", None)
    monkeypatch.setattr(redaction, "_PRESIDIO_UNAVAILABLE", False)
    monkeypatch.setattr(redaction.importlib.util, "find_spec", fake_find_spec)


def test_redact_text_redacts_email_with_fallback() -> None:
    redacted = redact_text("Contact admin@example.com for review")

    assert redacted == "Contact [REDACTED] for review"


def test_redact_text_redacts_tokens_with_fallback() -> None:
    redacted = redact_text("Authorization: Bearer abc.def.ghi")

    assert redacted == "Authorization: [REDACTED]"


def test_redact_mapping_redacts_nested_values_without_mutating_input() -> None:
    payload: dict[str, object] = {
        "owner": "owner@example.com",
        "headers": {"Authorization": "Bearer abc.def.ghi"},
        "nested": [
            {"phone": "+1 (415) 555-1234"},
            "token=abc123456789",
            {"api_key": "sk-test-12345678901234567890"},
        ],
    }

    redacted = redact_mapping(payload)

    assert payload["owner"] == "owner@example.com"
    assert payload["headers"] == {"Authorization": "Bearer abc.def.ghi"}
    assert redacted["owner"] == "[REDACTED]"
    assert redacted["headers"] == {"Authorization": "[REDACTED]"}
    nested = redacted["nested"]
    assert isinstance(nested, list)
    assert nested[0] == {"phone": "[REDACTED]"}
    assert nested[1] == "[REDACTED]"
    assert nested[2] == {"api_key": "[REDACTED]"}


def test_safe_metadata_preserves_allowlisted_metadata() -> None:
    metadata: dict[str, object] = {
        "correlation_id": "corr-admin@example.com",
        "decision": "allow",
        "policy_package": "onyx.security.retrieval_acl",
        "fallback_used": False,
        "enforcement_enabled": True,
        "reviewer_email": "reviewer@example.com",
        "auth_token": "Bearer abc.def.ghi",
    }

    redacted = safe_metadata(metadata)

    assert redacted["correlation_id"] == "corr-admin@example.com"
    assert redacted["decision"] == "allow"
    assert redacted["policy_package"] == "onyx.security.retrieval_acl"
    assert redacted["fallback_used"] is False
    assert redacted["enforcement_enabled"] is True
    assert redacted["reviewer_email"] == "[REDACTED]"
    assert redacted["auth_token"] == "[REDACTED]"


def test_missing_presidio_dependency_uses_regex_fallback() -> None:
    assert redaction._get_presidio_engines() is None
    assert redact_text("api_key=sk-test-12345678901234567890") == "[REDACTED]"


def test_redact_security_payload_backward_compatible_wrapper() -> None:
    payload: dict[str, Any] = {
        "api_key": "sk-test-123456789",
        "headers": {"Authorization": "Bearer abc.def.ghi"},
        "nested": [{"password": "p@ss"}, "token=abc", {"jwt": "eyJabc.def.ghi"}],
        "aws": "AKIAABCDEFGHIJKLMNOP",
        "pem": "-----BEGIN PRIVATE KEY-----\na\n-----END PRIVATE KEY-----",
        "demo": "demo_secret",
    }

    out = redact_security_payload(payload)

    assert out["api_key"] == "[REDACTED]"
    assert out["headers"]["Authorization"] == "[REDACTED]"
    assert out["nested"][0]["password"] == "[REDACTED]"
    assert "[REDACTED]" in out["nested"][1]
    assert out["nested"][2]["jwt"] == "[REDACTED]"
    assert out["aws"] == "[REDACTED]"
    assert out["pem"] == "[REDACTED]"
    assert out["demo"] == "[REDACTED]"


class FakeAnalyzer:
    def analyze(self, *, text: str, language: str) -> list[object]:
        assert language == "en"
        assert text == "Presidio sees jane@example.com"
        return [object()]


class FakeAnonymizer:
    def anonymize(self, *, text: str, analyzer_results: list[object]) -> object:
        assert text == "Presidio sees jane@example.com"
        assert analyzer_results
        return type("Anonymized", (), {"text": "Presidio sees <EMAIL_ADDRESS>"})()


def test_presidio_is_used_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    analyzer_module = ModuleType("presidio_analyzer")
    analyzer_module.AnalyzerEngine = FakeAnalyzer  # type: ignore[attr-defined]
    anonymizer_module = ModuleType("presidio_anonymizer")
    anonymizer_module.AnonymizerEngine = FakeAnonymizer  # type: ignore[attr-defined]

    def fake_find_spec(name: str, *args: object, **kwargs: object) -> object | None:
        if name in {"presidio_analyzer", "presidio_anonymizer"}:
            return object()
        return None

    def fake_import_module(name: str) -> ModuleType:
        if name == "presidio_analyzer":
            return analyzer_module
        if name == "presidio_anonymizer":
            return anonymizer_module
        return importlib.import_module(name)

    monkeypatch.setattr(redaction, "_PRESIDIO_ENGINES", None)
    monkeypatch.setattr(redaction, "_PRESIDIO_UNAVAILABLE", False)
    monkeypatch.setattr(redaction.importlib.util, "find_spec", fake_find_spec)
    monkeypatch.setattr(redaction.importlib, "import_module", fake_import_module)

    assert redact_text("Presidio sees jane@example.com") == "Presidio sees <EMAIL_ADDRESS>"
