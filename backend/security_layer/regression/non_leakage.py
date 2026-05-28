"""Non-leakage checks for isolated regression/demo output."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
import re
from typing import Any

from backend.security_layer.regression.models import RegressionDemoResult
from backend.security_layer.regression.models import RegressionDemoRunSummary

_FORBIDDEN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b", re.IGNORECASE),
    re.compile(r"\b(api[_-]?key|token|password|passwd)\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"raw[_ -]?(prompt|document|chunk)\s*[:=]", re.IGNORECASE),
    re.compile(r"tenant[_ -]?internal\s*[:=]", re.IGNORECASE),
    re.compile(r"policy[_ -]?internal\s*[:=]", re.IGNORECASE),
    re.compile(r"source[_ -]?internal\s*[:=]", re.IGNORECASE),
)


def _stringify(value: Any) -> str:
    if is_dataclass(value):
        return str(asdict(value))
    return str(value)


def detect_forbidden_demo_output(value: object) -> bool:
    text = _stringify(value)
    return any(pattern.search(text) for pattern in _FORBIDDEN_PATTERNS)


def sanitize_demo_attack_output(value: object) -> str:
    text = _stringify(value)
    for pattern in _FORBIDDEN_PATTERNS:
        text = pattern.sub("[REDACTED_DEMO_OUTPUT]", text)
    return text


def validate_regression_result_non_leakage(result: RegressionDemoResult) -> bool:
    return result.non_leakage_validated and not detect_forbidden_demo_output(result)


def validate_summary_non_leakage(summary: RegressionDemoRunSummary) -> bool:
    return summary.non_leakage_validated and not detect_forbidden_demo_output(summary)


def sanitize_regression_demo_result_model(
    result: RegressionDemoResult,
) -> RegressionDemoResult:
    return replace(
        result,
        sanitized_summary=sanitize_demo_attack_output(result.sanitized_summary),
        non_leakage_validated=not detect_forbidden_demo_output(
            result.sanitized_summary
        ),
    )
