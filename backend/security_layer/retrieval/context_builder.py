from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.retrieval.models import ACLSnapshot
from backend.security_layer.retrieval.models import RetrievalACLContext
from backend.security_layer.retrieval.models import RetrievalCandidate
from backend.security_layer.retrieval.models import RetrievalChunk
from backend.security_layer.retrieval.models import RetrievalDocument
from backend.security_layer.retrieval.models import RetrievalSourceType
from backend.security_layer.retrieval.models import RetrievalStage
from backend.security_layer.retrieval.models import RetrievalSubject
from backend.security_layer.retrieval.models import RetrievalTenant
from backend.security_layer.retrieval.models import VectorMetadata
from backend.security_layer.retrieval.models import VectorNamespace

_BLOCKED_METADATA_KEYS = {"document_text", "chunk_text", "source_secret", "secret", "raw_text", "content"}


@dataclass(frozen=True)
class RetrievalContextBuildInput:
    request_id: str
    source_type: RetrievalSourceType
    stage: RetrievalStage
    subject_id: str | None = None
    group_ids: tuple[str, ...] = ()
    role_ids: tuple[str, ...] = ()
    tenant_id: str | None = None
    retrieval_scope: tuple[str, ...] = ()
    expected_vector_namespace: str | None = None
    acl_snapshot: ACLSnapshot | None = None


@dataclass(frozen=True)
class RetrievalContextBuildResult:
    context: RetrievalACLContext
    candidates: tuple[RetrievalCandidate, ...] = ()


def _assert_safe_metadata(metadata: dict[str, object]) -> None:
    for blocked in _BLOCKED_METADATA_KEYS:
        if blocked in metadata:
            raise ValueError(f"unsafe metadata key: {blocked}")


def build_subject_context(input: RetrievalContextBuildInput) -> RetrievalSubject:
    return RetrievalSubject(subject_id=input.subject_id, group_ids=input.group_ids, role_ids=input.role_ids)


def build_tenant_context(input: RetrievalContextBuildInput) -> RetrievalTenant:
    return RetrievalTenant(tenant_id=input.tenant_id)


def build_retrieval_acl_context(input: RetrievalContextBuildInput) -> RetrievalACLContext:
    return RetrievalACLContext(
        subject=build_subject_context(input),
        tenant=build_tenant_context(input),
        stage=input.stage,
        source_type=input.source_type,
        request_id=input.request_id,
        retrieval_scope=input.retrieval_scope,
        expected_vector_namespace=input.expected_vector_namespace,
        acl_snapshot=input.acl_snapshot,
    )


def build_candidate_from_metadata(metadata: dict[str, object]) -> RetrievalCandidate:
    _assert_safe_metadata(metadata)
    document_id = str(metadata.get("document_id", ""))
    chunk_id = str(metadata.get("chunk_id", ""))
    candidate_id = str(metadata.get("candidate_id", f"{document_id}:{chunk_id}"))
    tenant_id = str(metadata.get("tenant_id", ""))
    vector_namespace = str(metadata.get("vector_namespace", ""))

    document = RetrievalDocument(
        document_id=document_id,
        tenant_id=tenant_id,
        allowed_subject_ids=tuple(str(x) for x in metadata.get("document_allowed_subject_ids", ())),
        allowed_group_ids=tuple(str(x) for x in metadata.get("document_allowed_group_ids", ())),
        allowed_role_ids=tuple(str(x) for x in metadata.get("document_allowed_role_ids", ())),
        is_deleted=bool(metadata.get("document_is_deleted", False)),
    )
    chunk = RetrievalChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        tenant_id=tenant_id,
        allowed_subject_ids=tuple(str(x) for x in metadata.get("chunk_allowed_subject_ids", ())),
        allowed_group_ids=tuple(str(x) for x in metadata.get("chunk_allowed_group_ids", ())),
        allowed_role_ids=tuple(str(x) for x in metadata.get("chunk_allowed_role_ids", ())),
    )
    return RetrievalCandidate(
        candidate_id=candidate_id,
        source_type=RetrievalSourceType(str(metadata.get("source_type", RetrievalSourceType.VECTOR.value))),
        document=document,
        chunk=chunk,
        vector_namespace=VectorNamespace(namespace=vector_namespace),
        vector_metadata=VectorMetadata(tenant_id=tenant_id, document_id=document_id, chunk_id=chunk_id),
        provenance_id=str(metadata.get("provenance_id", candidate_id)),
    )


def build_candidates_from_metadata_list(metadata_list: list[dict[str, object]]) -> list[RetrievalCandidate]:
    return [build_candidate_from_metadata(metadata) for metadata in metadata_list]


def validate_context_build_result(result: RetrievalContextBuildResult) -> bool:
    if not result.context.request_id:
        return False
    for candidate in result.candidates:
        if not candidate.candidate_id or not candidate.document.document_id or not candidate.chunk.chunk_id:
            return False
    return True
