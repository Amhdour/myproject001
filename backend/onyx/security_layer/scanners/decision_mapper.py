from __future__ import annotations

import os

from onyx.security_layer.scanners.models import RAGInjectionScannerDecision

RAG_INJECTION_SCANNER_MODE_ENV = "SECURITY_RAG_INJECTION_SCANNER_MODE"
RAG_INJECTION_SCANNER_FAILURE_MODE_ENV = "SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE"

_HIGH_RISK_THRESHOLD = 0.8
_VALID_MODES = {
    RAGInjectionScannerDecision.ALLOW,
    RAGInjectionScannerDecision.DENY,
    RAGInjectionScannerDecision.SANITIZE,
    RAGInjectionScannerDecision.MONITOR,
    RAGInjectionScannerDecision.SHADOW_DENY,
}
_FAILURE_MODES = {
    RAGInjectionScannerDecision.MONITOR,
    RAGInjectionScannerDecision.DENY,
}


def _configured_decision(
    *,
    env_name: str,
    default: RAGInjectionScannerDecision,
    valid: set[RAGInjectionScannerDecision],
) -> RAGInjectionScannerDecision:
    raw_value = os.getenv(env_name, default.value).lower()
    try:
        decision = RAGInjectionScannerDecision(raw_value)
    except ValueError:
        return default
    return decision if decision in valid else default


def configured_rag_injection_mode() -> RAGInjectionScannerDecision:
    return _configured_decision(
        env_name=RAG_INJECTION_SCANNER_MODE_ENV,
        default=RAGInjectionScannerDecision.DENY,
        valid=_VALID_MODES,
    )


def configured_rag_injection_failure_mode() -> RAGInjectionScannerDecision:
    return _configured_decision(
        env_name=RAG_INJECTION_SCANNER_FAILURE_MODE_ENV,
        default=RAGInjectionScannerDecision.MONITOR,
        valid=_FAILURE_MODES,
    )


def map_risk_to_decision(risk_score: float) -> RAGInjectionScannerDecision:
    if risk_score < _HIGH_RISK_THRESHOLD:
        return RAGInjectionScannerDecision.ALLOW
    configured_mode = configured_rag_injection_mode()
    if configured_mode == RAGInjectionScannerDecision.ALLOW:
        return RAGInjectionScannerDecision.ALLOW
    return configured_mode


def map_failure_to_decision() -> RAGInjectionScannerDecision:
    return configured_rag_injection_failure_mode()
