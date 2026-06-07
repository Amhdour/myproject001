from __future__ import annotations

import importlib
import importlib.metadata
import importlib.util
import os
from dataclasses import replace
from typing import Any
from typing import Final
from typing import NamedTuple

from onyx.security_layer.scanners.decision_mapper import map_risk_to_decision
from onyx.security_layer.scanners.models import RAGInjectionRiskType
from onyx.security_layer.scanners.models import RAGInjectionScannerDecision
from onyx.security_layer.scanners.models import RAGInjectionScanRequest
from onyx.security_layer.scanners.models import RAGInjectionScanResult

RAG_SCANNER_PROVIDER_ENV: Final[str] = "SECURITY_RAG_SCANNER_PROVIDER"
RAG_SCANNER_FALLBACK_PROVIDER_ENV: Final[str] = "SECURITY_RAG_SCANNER_FALLBACK_PROVIDER"

HEURISTIC_PROVIDER: Final[str] = "heuristic"
LLAMAFIREWALL_PROVIDER: Final[str] = "llamafirewall"
MONITOR_FALLBACK_PROVIDER: Final[str] = "monitor"
DENY_FALLBACK_PROVIDER: Final[str] = "deny"

_VALID_PROVIDERS: Final[frozenset[str]] = frozenset(
    {HEURISTIC_PROVIDER, LLAMAFIREWALL_PROVIDER}
)
_VALID_FALLBACK_PROVIDERS: Final[frozenset[str]] = frozenset(
    {HEURISTIC_PROVIDER, MONITOR_FALLBACK_PROVIDER, DENY_FALLBACK_PROVIDER}
)
_CANDIDATE_MODULES: Final[tuple[str, ...]] = (
    "llamafirewall",
    "llama_firewall",
    "PurpleLlama.llama_firewall",
    "purple_llama.llama_firewall",
)
_CANDIDATE_DISTRIBUTIONS: Final[tuple[str, ...]] = (
    "llamafirewall",
    "llama-firewall",
    "purplellama",
    "purple-llama",
    "PurpleLlama",
)


class _Backend(NamedTuple):
    module: Any
    version: str | None


def configured_rag_scanner_provider() -> str:
    raw_provider = os.getenv(RAG_SCANNER_PROVIDER_ENV, HEURISTIC_PROVIDER).lower()
    if raw_provider in _VALID_PROVIDERS:
        return raw_provider
    return HEURISTIC_PROVIDER


def configured_rag_scanner_fallback_provider() -> str:
    raw_provider = os.getenv(
        RAG_SCANNER_FALLBACK_PROVIDER_ENV, HEURISTIC_PROVIDER
    ).lower()
    if raw_provider in _VALID_FALLBACK_PROVIDERS:
        return raw_provider
    return HEURISTIC_PROVIDER


def _distribution_version() -> str | None:
    for distribution_name in _CANDIDATE_DISTRIBUTIONS:
        try:
            return importlib.metadata.version(distribution_name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def _load_backend() -> _Backend | None:
    for module_name in _CANDIDATE_MODULES:
        if importlib.util.find_spec(module_name) is None:
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception:
            return None
        return _Backend(module=module, version=_distribution_version())
    return None


def _numeric_score(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return max(0.0, min(1.0, float(value)))
    return None


def _value_from_backend_result(result: object, *names: str) -> object | None:
    if isinstance(result, dict):
        for name in names:
            if name in result:
                return result[name]
    for name in names:
        if hasattr(result, name):
            return getattr(result, name)
    return None


def _backend_risk_score(result: object) -> float:
    explicit_score = _value_from_backend_result(
        result, "risk_score", "score", "confidence", "probability"
    )
    score = _numeric_score(explicit_score)
    if score is not None:
        return score

    label = _value_from_backend_result(result, "label", "risk_type", "decision")
    if isinstance(label, str) and label.lower() in {
        "prompt_injection",
        "injection",
        "malicious",
        "block",
        "deny",
    }:
        return 1.0

    flagged = _value_from_backend_result(
        result, "is_injection", "is_malicious", "flagged", "unsafe"
    )
    if flagged is True:
        return 1.0
    return 0.0


def _call_backend(module: Any, content: str) -> object:
    for factory_name in ("LlamaFirewall", "PromptInjectionScanner", "Scanner"):
        factory = getattr(module, factory_name, None)
        if factory is None:
            continue
        scanner = factory()
        for method_name in ("scan", "evaluate", "detect", "classify"):
            method = getattr(scanner, method_name, None)
            if callable(method):
                return method(content)

    for function_name in ("scan", "evaluate", "detect", "classify"):
        function = getattr(module, function_name, None)
        if callable(function):
            return function(content)

    raise RuntimeError("no supported LlamaFirewall/PurpleLlama scan entry point found")


class LlamaFirewallRAGInjectionScannerAdapter:
    """Optional adapter for a runtime-installed LlamaFirewall/PurpleLlama backend.

    The dependency is intentionally not imported at module import time and is not
    required for the local heuristic scanner. If the backend is unavailable or
    its runtime API cannot be called safely, this adapter follows
    ``SECURITY_RAG_SCANNER_FALLBACK_PROVIDER``.
    """

    def __init__(self) -> None:
        self._backend = _load_backend()

    @property
    def scanner_name(self) -> str:
        return "llamafirewall_rag_injection_scanner_adapter"

    @property
    def backend_available(self) -> bool:
        return self._backend is not None

    @property
    def backend_version(self) -> str | None:
        if self._backend is None:
            return None
        return self._backend.version

    def _heuristic_fallback(
        self, request: RAGInjectionScanRequest
    ) -> RAGInjectionScanResult:
        from onyx.security_layer.scanners.rag_injection_scanner import (
            HeuristicRAGInjectionScanner,
        )

        result = HeuristicRAGInjectionScanner().scan(request)
        return replace(
            result,
            scanner_name=self.scanner_name,
            scanner_provider=LLAMAFIREWALL_PROVIDER,
            scanner_backend_available=False,
            scanner_backend_version=self.backend_version,
            fallback_used=True,
            reason=(
                f"llamafirewall backend unavailable; heuristic fallback; "
                f"heuristic_reason={result.reason}"
            ),
        )

    def _monitor_or_deny_fallback(
        self,
        request: RAGInjectionScanRequest,
        decision: RAGInjectionScannerDecision,
    ) -> RAGInjectionScanResult:
        return RAGInjectionScanResult(
            scanner_name=self.scanner_name,
            scanner_provider=LLAMAFIREWALL_PROVIDER,
            scanner_backend_available=False,
            scanner_backend_version=self.backend_version,
            scanner_decision=decision,
            risk_type=RAGInjectionRiskType.SCANNER_FAILURE,
            risk_score=1.0 if decision == RAGInjectionScannerDecision.DENY else 0.0,
            sanitized=False,
            resource_chunk_id=request.resource_chunk_id,
            correlation_id=request.correlation_id,
            reason="llamafirewall backend unavailable",
            fallback_used=True,
        )

    def _fallback_result(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        fallback_provider = configured_rag_scanner_fallback_provider()
        if fallback_provider == HEURISTIC_PROVIDER:
            return self._heuristic_fallback(request)
        if fallback_provider == DENY_FALLBACK_PROVIDER:
            return self._monitor_or_deny_fallback(
                request, RAGInjectionScannerDecision.DENY
            )
        return self._monitor_or_deny_fallback(
            request, RAGInjectionScannerDecision.MONITOR
        )

    def scan(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        if self._backend is None:
            return self._fallback_result(request)

        try:
            backend_result = _call_backend(self._backend.module, request.content)
        except Exception:
            return self._fallback_result(request)

        risk_score = _backend_risk_score(backend_result)
        risk_type = (
            RAGInjectionRiskType.PROMPT_INJECTION
            if risk_score > 0.0
            else RAGInjectionRiskType.NONE
        )
        return RAGInjectionScanResult(
            scanner_name=self.scanner_name,
            scanner_provider=LLAMAFIREWALL_PROVIDER,
            scanner_backend_available=True,
            scanner_backend_version=self.backend_version,
            scanner_decision=map_risk_to_decision(risk_score),
            risk_type=risk_type,
            risk_score=risk_score,
            sanitized=False,
            resource_chunk_id=request.resource_chunk_id,
            correlation_id=request.correlation_id,
            reason="llamafirewall backend result mapped to scanner decision",
        )
