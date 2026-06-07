from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class RAGInjectionScannerDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    SANITIZE = "sanitize"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"


class RAGInjectionRiskType(str, Enum):
    NONE = "none"
    PROMPT_INJECTION = "prompt_injection"
    SCANNER_FAILURE = "scanner_failure"


@dataclass(frozen=True)
class RAGInjectionScanRequest:
    content: str
    resource_chunk_id: str
    resource_document_id: str | None
    correlation_id: str


@dataclass(frozen=True)
class RAGInjectionScanResult:
    scanner_name: str
    scanner_decision: RAGInjectionScannerDecision
    risk_type: RAGInjectionRiskType
    risk_score: float
    sanitized: bool
    resource_chunk_id: str
    correlation_id: str
    sanitized_content: str | None = None
    reason: str | None = None
    fallback_used: bool = False


class RAGInjectionScanner(Protocol):
    @property
    def scanner_name(self) -> str:
        pass

    def scan(self, request: RAGInjectionScanRequest) -> RAGInjectionScanResult:
        pass
