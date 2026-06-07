from __future__ import annotations

from collections.abc import Iterator
from collections.abc import Mapping
from contextlib import contextmanager
import importlib
import importlib.util
from typing import Protocol

AttributeValue = str | bool | int | float


class SecuritySpan(Protocol):
    def set_attribute(self, key: str, value: AttributeValue) -> None:
        pass


def _load_opentelemetry_trace() -> object | None:
    if importlib.util.find_spec("opentelemetry") is None:
        return None
    if importlib.util.find_spec("opentelemetry.trace") is None:
        return None
    return importlib.import_module("opentelemetry.trace")


_OPENTELEMETRY_TRACE = _load_opentelemetry_trace()
_TRACER_NAME = "onyx.security_layer"


def opentelemetry_available() -> bool:
    return _OPENTELEMETRY_TRACE is not None


def _normalize_attribute_value(value: object) -> AttributeValue | None:
    if value is None:
        return None
    if isinstance(value, str | bool | int | float):
        return value
    return str(value)


def set_security_span_attributes(
    span: SecuritySpan | None,
    attributes: Mapping[str, object | None],
) -> None:
    if span is None:
        return

    for key, value in attributes.items():
        normalized_value = _normalize_attribute_value(value)
        if normalized_value is not None:
            span.set_attribute(key, normalized_value)


@contextmanager
def security_span(
    name: str,
    attributes: Mapping[str, object | None] | None = None,
) -> Iterator[SecuritySpan | None]:
    if _OPENTELEMETRY_TRACE is None:
        yield None
        return

    get_tracer = getattr(_OPENTELEMETRY_TRACE, "get_tracer")
    tracer = get_tracer(_TRACER_NAME)
    with tracer.start_as_current_span(name) as span:
        set_security_span_attributes(span, attributes or {})
        yield span
