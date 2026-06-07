from __future__ import annotations

import os
import re
from dataclasses import is_dataclass
from dataclasses import replace
from typing import Final

from onyx.security_layer.langfuse_evidence import emit_rag_injection_langfuse_evidence
from onyx.security_layer.redaction import safe_metadata
from onyx.security_layer.scanners.decision_mapper import map_failure_to_decision
from onyx.security_layer.scanners.decision_mapper import map_risk_to_decision
from onyx.security_layer.scanners.models import RAGInjectionRiskType
from onyx.security_layer.scanners.models import RAGInjectionScanner
from onyx.security_layer.scanners.models import RAGInjectionScannerDecision
from onyx.security_layer.scanners.models import RAGInjectionScanRequest
from onyx.security_layer.scanners.models import RAGInjectionScanResult
from onyx.security_layer.scanners.models import RetrievedChunk
from onyx.security_layer.scanners.models import RetrievedSection
from onyx.security_layer.tracing import security_span
from onyx.security_layer.tracing import set_security_span_attributes

RAG_INJECTION_SCANNER_ENABLED_ENV: Final[str] = "SECURITY_RAG_INJECTION_SCANNER_ENABLED"
RAG_INJECTION_SCANNER_SPAN_NAME: Final[str] = "security.rag_injection.scan"
_SANITIZED_PLACEHOLDER: Final[str] = (
    "[Potential prompt-injection instructions removed from retrieved context.]"
)

_INJECTION_PATTERNS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    (
        "ignore_previous_instructions",
        re.compile(
            r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
            re.IGNORECASE,
        ),
    ),
    (
        "reveal_system_prompt",
        re.compile(
            r"\b(?:reveal|show|print|dump|expose)\s+(?:the\s+)?system\s+prompt\b",
            re.IGNORECASE,
        ),
    ),
    (
        "override_security_policy",
        re.compile(
            r"\boverride\s+(?:the\s+)?security\s+polic(?:y|ies)\b", re.IGNORECASE
        ),
    ),
    (
        "exfiltrate_hidden_documents",
        re.compile(
            r"\b(?:exfiltrate|leak|export|copy)\s+(?:all\s+)?hidden\s+documents\b",
            re.IGNORECASE,
        ),
    ),
    (
        "call_unauthorized_tools",
        re.compile(
            r"\b(?:call|invoke|use|run)\s+unauthorized\s+tools?\b", re.IGNORECASE
        ),
    ),
)


def rag_injection_scanner_enabled() -> bool:
    return os.getenv(RAG_INJECTION_SCANNER_ENABLED_ENV, "false").lower() == "true"


class HeuristicRAGInjectionScanner:
    @property
    def scanner_name(self) -> str:
        return "local_heuristic_rag_injection_scanner"

    def scan(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        matched_patterns: list[re.Pattern[str]] = []
        matched_names: list[str] = []
        for name, pattern in _INJECTION_PATTERNS:
            if pattern.search(request.content):
                matched_names.append(name)
                matched_patterns.append(pattern)

        if not matched_patterns:
            return RAGInjectionScanResult(
                scanner_name=self.scanner_name,
                scanner_decision=RAGInjectionScannerDecision.ALLOW,
                risk_type=RAGInjectionRiskType.NONE,
                risk_score=0.0,
                sanitized=False,
                resource_chunk_id=request.resource_chunk_id,
                correlation_id=request.correlation_id,
            )

        risk_score = min(1.0, 0.8 + (0.05 * (len(matched_patterns) - 1)))
        decision = map_risk_to_decision(risk_score)
        sanitized_content: str | None = None
        sanitized = decision == RAGInjectionScannerDecision.SANITIZE
        if sanitized:
            sanitized_content = request.content
            for pattern in matched_patterns:
                sanitized_content = pattern.sub(
                    _SANITIZED_PLACEHOLDER, sanitized_content
                )

        return RAGInjectionScanResult(
            scanner_name=self.scanner_name,
            scanner_decision=decision,
            risk_type=RAGInjectionRiskType.PROMPT_INJECTION,
            risk_score=risk_score,
            sanitized=sanitized,
            resource_chunk_id=request.resource_chunk_id,
            correlation_id=request.correlation_id,
            sanitized_content=sanitized_content,
            reason=",".join(matched_names),
        )


class LlamaFirewallRAGInjectionScannerAdapter:
    @property
    def scanner_name(self) -> str:
        return "llamafirewall_adapter_unimplemented"

    def scan(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        raise NotImplementedError(
            "LlamaFirewall/PurpleLlama adapter is a planned extension point and is not implemented yet."
        )


class AgentShieldRAGInjectionScannerAdapter:
    @property
    def scanner_name(self) -> str:
        return "agentshield_adapter_unimplemented"

    def scan(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        raise NotImplementedError(
            "AgentShield adapter is a planned extension point and is not implemented yet."
        )


def _scan_evidence_attributes(
    result: RAGInjectionScanResult,
) -> dict[str, object | None]:
    return safe_metadata(
        {
            "scanner_name": result.scanner_name,
            "scanner_decision": result.scanner_decision.value,
            "risk_type": result.risk_type.value,
            "risk_score": result.risk_score,
            "sanitized": result.sanitized,
            "resource_chunk_id": result.resource_chunk_id,
            "correlation_id": result.correlation_id,
            "fallback_used": result.fallback_used,
        }
    )


def _failure_result(
    *,
    scanner_name: str,
    request: RAGInjectionScanRequest,
) -> RAGInjectionScanResult:
    decision = map_failure_to_decision()
    return RAGInjectionScanResult(
        scanner_name=scanner_name,
        scanner_decision=decision,
        risk_type=RAGInjectionRiskType.SCANNER_FAILURE,
        risk_score=1.0 if decision == RAGInjectionScannerDecision.DENY else 0.0,
        sanitized=False,
        resource_chunk_id=request.resource_chunk_id,
        correlation_id=request.correlation_id,
        reason="scanner failure fallback",
        fallback_used=True,
    )


def _scan_chunk(
    *,
    chunk: RetrievedChunk,
    correlation_id: str,
    scanner: RAGInjectionScanner,
) -> RAGInjectionScanResult:
    request = RAGInjectionScanRequest(
        content=chunk.content,
        resource_chunk_id=str(chunk.chunk_id),
        resource_document_id=chunk.document_id,
        correlation_id=correlation_id,
    )
    with security_span(
        RAG_INJECTION_SCANNER_SPAN_NAME,
        {
            "correlation_id": correlation_id,
            "resource_chunk_id": str(chunk.chunk_id),
            "scanner_name": scanner.scanner_name,
        },
    ) as span:
        try:
            result = scanner.scan(request)
        except Exception:
            result = _failure_result(scanner_name=scanner.scanner_name, request=request)
        attributes = _scan_evidence_attributes(result)
        set_security_span_attributes(span, attributes)
        emit_rag_injection_langfuse_evidence(attributes)
        return result


def _chunk_with_sanitized_content(
    chunk: RetrievedChunk, sanitized_content: str
) -> RetrievedChunk:
    update = {"content": sanitized_content, "blurb": sanitized_content}
    model_copy = getattr(chunk, "model_copy", None)
    if callable(model_copy):
        copied_chunk = model_copy(update=update)
        return copied_chunk
    if is_dataclass(chunk) and not isinstance(chunk, type):
        return replace(chunk, **update)
    chunk_attributes = dict(getattr(chunk, "__dict__", {}))
    chunk_attributes.update(update)
    return chunk.__class__(**chunk_attributes)


def _section_with_scanned_chunks(
    section: RetrievedSection,
    center_chunk: RetrievedChunk,
    scanned_chunks: list[RetrievedChunk],
) -> RetrievedSection:
    update = {
        "center_chunk": center_chunk,
        "chunks": scanned_chunks,
        "combined_content": "\n".join(chunk.content for chunk in scanned_chunks),
    }
    model_copy = getattr(section, "model_copy", None)
    if callable(model_copy):
        copied_section = model_copy(update=update)
        return copied_section
    if is_dataclass(section) and not isinstance(section, type):
        return replace(section, **update)
    section_attributes = dict(getattr(section, "__dict__", {}))
    section_attributes.update(update)
    return section.__class__(**section_attributes)


def _apply_scan_result(
    *, chunk: RetrievedChunk, result: RAGInjectionScanResult
) -> RetrievedChunk | None:
    if result.scanner_decision == RAGInjectionScannerDecision.DENY:
        return None
    if result.scanner_decision == RAGInjectionScannerDecision.SANITIZE:
        return _chunk_with_sanitized_content(
            chunk, result.sanitized_content or _SANITIZED_PLACEHOLDER
        )
    return chunk


def scan_sections_for_rag_injection(
    *,
    sections: list[RetrievedSection],
    correlation_id: str,
    scanner: RAGInjectionScanner | None = None,
) -> tuple[list[RetrievedSection], tuple[RAGInjectionScanResult, ...]]:
    resolved_scanner = scanner or HeuristicRAGInjectionScanner()
    scanned_sections: list[RetrievedSection] = []
    results: list[RAGInjectionScanResult] = []

    for section in sections:
        scanned_chunks: list[RetrievedChunk] = []
        for chunk in section.chunks:
            result = _scan_chunk(
                chunk=chunk,
                correlation_id=f"{correlation_id}:{chunk.document_id}:{chunk.chunk_id}",
                scanner=resolved_scanner,
            )
            results.append(result)
            scanned_chunk = _apply_scan_result(chunk=chunk, result=result)
            if scanned_chunk is not None:
                scanned_chunks.append(scanned_chunk)

        if scanned_chunks:
            center_chunk = next(
                (chunk for chunk in scanned_chunks if chunk == section.center_chunk),
                scanned_chunks[0],
            )
            scanned_sections.append(
                _section_with_scanned_chunks(
                    section=section,
                    center_chunk=center_chunk,
                    scanned_chunks=scanned_chunks,
                )
            )

    return scanned_sections, tuple(results)
