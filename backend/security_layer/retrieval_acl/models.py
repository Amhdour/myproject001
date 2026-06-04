from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class RetrievalACLReason(str, Enum):
    ALLOWED = "allowed"
    MISSING_ACL_CONTEXT = "missing_acl_context"
    MALFORMED_ACL_CONTEXT = "malformed_acl_context"
    CROSS_TENANT_RESULT = "cross_tenant_result"
    UNAUTHORIZED_DOCUMENT_ID = "unauthorized_document_id"
    DOCUMENT_ACL_MISMATCH = "document_acl_mismatch"


RetrievalACLDecisionStatus = Literal["allow", "deny", "filter"]


@dataclass(frozen=True)
class RetrievalACLContext:
    """Requester authorization context for isolated retrieval ACL proof checks."""

    tenant_id: str
    subject_id: str
    allowed_document_ids: frozenset[str]
    group_ids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class RetrievalDocumentACL:
    """Document ACL snapshot carried by an isolated retrieval result."""

    tenant_id: str
    document_id: str
    allowed_subject_ids: frozenset[str]
    allowed_group_ids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class RetrievalResultChunk:
    """Minimal retrieval chunk/document result used by the isolated helper."""

    chunk_id: str
    document_id: str
    tenant_id: str
    document_acl: RetrievalDocumentACL


@dataclass(frozen=True)
class RetrievalACLDenial:
    chunk_id: str | None
    document_id: str | None
    reason: RetrievalACLReason


@dataclass(frozen=True)
class RetrievalACLDecision:
    status: RetrievalACLDecisionStatus
    allowed_chunks: tuple[RetrievalResultChunk, ...]
    denials: tuple[RetrievalACLDenial, ...]

    @property
    def denied_count(self) -> int:
        return len(self.denials)
