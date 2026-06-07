from __future__ import annotations

import onyx.security_layer.tracing as security_tracing


class RecordingSpan:
    def __init__(self) -> None:
        self.attributes: dict[str, str | bool | int | float] = {}

    def set_attribute(self, key: str, value: str | bool | int | float) -> None:
        self.attributes[key] = value


def test_security_tracing_helper_noops_when_opentelemetry_is_unavailable(
    monkeypatch,
) -> None:
    monkeypatch.setattr(security_tracing, "_OPENTELEMETRY_TRACE", None)

    with security_tracing.security_span(
        "security.test", {"correlation_id": "corr"}
    ) as span:
        security_tracing.set_security_span_attributes(span, {"decision": "allow"})

    assert span is None


def test_security_tracing_helper_sets_only_safe_scalar_attributes() -> None:
    span = RecordingSpan()

    security_tracing.set_security_span_attributes(
        span,
        {
            "correlation_id": "corr",
            "fallback_used": False,
            "decision_count": 1,
            "ignored_none": None,
            "coerced_value": {"not": "otel scalar"},
        },
    )

    assert span.attributes == {
        "correlation_id": "corr",
        "fallback_used": False,
        "decision_count": 1,
        "coerced_value": "{'not': 'otel scalar'}",
    }
