from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence
import importlib
import importlib.util
import re
from typing import Any

_REDACTED = "[REDACTED]"
_PRESIDIO_LANGUAGE = "en"

_SAFE_METADATA_KEYS = frozenset(
    {
        "correlation_id",
        "decision",
        "policy_package",
        "fallback_used",
        "enforcement_enabled",
    }
)

_SECRET_KEYWORDS = frozenset(
    {
        "api_key",
        "apikey",
        "access_key",
        "access_token",
        "auth_token",
        "authorization",
        "bearer",
        "client_secret",
        "cookie",
        "credential",
        "jwt",
        "key_secret",
        "passcode",
        "passwd",
        "password",
        "private_key",
        "refresh_token",
        "secret",
        "session_token",
        "token",
    }
)

_EMAIL_RE = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
_PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
_BEARER_RE = re.compile(r"\bbearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
_OPENAI_KEY_RE = re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}\b")
_AWS_ACCESS_KEY_RE = re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")
_GITHUB_TOKEN_RE = re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")
_SLACK_TOKEN_RE = re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")
_JWT_RE = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)
_SECRET_ASSIGNMENT_RE = re.compile(
    r"\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|bearer|client[_-]?secret|"
    r"password|passwd|private[_-]?key|refresh[_-]?token|secret|session[_-]?token|token)"
    r"\s*[:=]\s*[^\s,;]+",
    re.IGNORECASE,
)
_DEMO_SECRET_RE = re.compile(
    r"\b(?:demo|fake|test)[_-]?(?:secret|token|key)\b",
    re.IGNORECASE,
)

_FALLBACK_PATTERNS = (
    _BEARER_RE,
    _EMAIL_RE,
    _PHONE_RE,
    _OPENAI_KEY_RE,
    _AWS_ACCESS_KEY_RE,
    _GITHUB_TOKEN_RE,
    _SLACK_TOKEN_RE,
    _JWT_RE,
    _SECRET_ASSIGNMENT_RE,
    _DEMO_SECRET_RE,
)

_PRESIDIO_ENGINES: tuple[Any, Any] | None = None
_PRESIDIO_UNAVAILABLE = False


def _presidio_installed() -> bool:
    return (
        importlib.util.find_spec("presidio_analyzer") is not None
        and importlib.util.find_spec("presidio_anonymizer") is not None
    )


def _get_presidio_engines() -> tuple[Any, Any] | None:
    global _PRESIDIO_ENGINES
    global _PRESIDIO_UNAVAILABLE

    if _PRESIDIO_ENGINES is not None:
        return _PRESIDIO_ENGINES
    if _PRESIDIO_UNAVAILABLE or not _presidio_installed():
        _PRESIDIO_UNAVAILABLE = True
        return None

    analyzer_module = importlib.import_module("presidio_analyzer")
    anonymizer_module = importlib.import_module("presidio_anonymizer")
    analyzer = analyzer_module.AnalyzerEngine()
    anonymizer = anonymizer_module.AnonymizerEngine()
    _PRESIDIO_ENGINES = (analyzer, anonymizer)
    return _PRESIDIO_ENGINES


def _redact_with_presidio(value: str) -> str | None:
    engines = _get_presidio_engines()
    if engines is None:
        return None

    analyzer, anonymizer = engines
    analyzer_results = analyzer.analyze(text=value, language=_PRESIDIO_LANGUAGE)
    anonymized = anonymizer.anonymize(text=value, analyzer_results=analyzer_results)
    return str(anonymized.text)


def _redact_with_fallback(value: str) -> str:
    if "-----BEGIN" in value and "PRIVATE KEY-----" in value:
        return _REDACTED

    redacted = value
    for pattern in _FALLBACK_PATTERNS:
        redacted = pattern.sub(_REDACTED, redacted)
    return redacted


def _key_requires_value_redaction(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(keyword in normalized for keyword in _SECRET_KEYWORDS)


def redact_text(value: str) -> str:
    """Redact sensitive text using Presidio when available, otherwise regexes.

    Presidio is intentionally optional for lightweight security evidence smoke
    checks. The built-in fallback is conservative and targets common evidence
    export risks including email addresses, phone-like values, bearer tokens,
    API-key-shaped values, and obvious secret assignments.
    """

    presidio_redacted = _redact_with_presidio(value)
    if presidio_redacted is not None:
        return _redact_with_fallback(presidio_redacted)
    return _redact_with_fallback(value)


def _redact_value(value: object) -> object:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return _redact_mapping(value, preserve_safe_keys=False)
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact_value(item) for item in value)
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray | str):
        return [_redact_value(item) for item in value]
    return value


def _redact_mapping(
    data: Mapping[str, object],
    *,
    preserve_safe_keys: bool,
) -> dict[str, object]:
    redacted: dict[str, object] = {}
    for key, value in data.items():
        if preserve_safe_keys and key in _SAFE_METADATA_KEYS:
            redacted[key] = value
        elif _key_requires_value_redaction(key):
            redacted[key] = _REDACTED
        else:
            redacted[key] = _redact_value(value)
    return redacted


def redact_mapping(data: dict[str, object]) -> dict[str, object]:
    """Return a redacted copy of a mapping without mutating the input."""

    return _redact_mapping(data, preserve_safe_keys=False)


def safe_metadata(data: dict[str, object]) -> dict[str, object]:
    """Return evidence metadata with known-safe identifiers preserved.

    The explicit metadata allowlist preserves stable, low-risk evidence fields
    such as correlation and OPA decision identifiers. All other fields are copied
    through the same redaction path used by ``redact_mapping``.
    """

    return _redact_mapping(data, preserve_safe_keys=True)


def redact_security_payload(value: Any) -> Any:
    """Backward-compatible wrapper for existing security evidence exporters."""

    if isinstance(value, Mapping):
        return _redact_mapping(value, preserve_safe_keys=False)
    return _redact_value(value)
