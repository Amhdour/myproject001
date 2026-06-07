from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from typing import Protocol

from onyx.context.search.models import InferenceChunk
from onyx.context.search.models import InferenceSection
from onyx.security_layer.opa.decision_mapper import OPADecision
from onyx.security_layer.opa.decision_mapper import OPADecisionValue
from onyx.security_layer.opa.input_builder import build_retrieval_acl_input
from onyx.security_layer.opa.opa_client import evaluate_retrieval_acl_with_fallback
from onyx.security_layer.opa.opa_client import OPAClient
from onyx.security_layer.tracing import security_span
from onyx.security_layer.tracing import set_security_span_attributes

OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT_ENV = (
    "SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT"
)


class RetrievalACLEvaluator(Protocol):
    def evaluate_retrieval_acl(self, opa_input: dict[str, Any]) -> OPADecision:
        pass


@dataclass(frozen=True)
class RetrievalContextOPAFilterResult:
    sections: list[InferenceSection]
    decisions: tuple[OPADecision, ...]

    @property
    def denied_decisions(self) -> tuple[OPADecision, ...]:
        return tuple(
            decision
            for decision in self.decisions
            if decision.decision != OPADecisionValue.ALLOW
        )


def opa_retrieval_acl_context_enforcement_enabled() -> bool:
    return (
        os.getenv(OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT_ENV, "false").lower() == "true"
    )


def _metadata_string(chunk: InferenceChunk, key: str) -> str | None:
    value = chunk.metadata.get(key)
    if value is None:
        return None
    if isinstance(value, list):
        return str(value[0]) if value else None
    return str(value)


def _metadata_string_list(chunk: InferenceChunk, key: str) -> list[str]:
    value = chunk.metadata.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return sorted({str(item) for item in value if str(item)})
    return [str(value)] if str(value) else []


def _embedded_acl(chunk: InferenceChunk) -> dict[str, Any]:
    value = chunk.metadata.get("onyx_acl")
    return value if isinstance(value, dict) else {}


def _embedded_acl_string(chunk: InferenceChunk, key: str) -> str | None:
    value = _embedded_acl(chunk).get(key)
    if value is None:
        return None
    return str(value)


def _embedded_acl_string_list(chunk: InferenceChunk, key: str) -> list[str]:
    value = _embedded_acl(chunk).get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return sorted({str(item) for item in value if str(item)})
    return [str(value)] if str(value) else []


def _resource_deleted(chunk: InferenceChunk) -> bool:
    embedded_deleted = _embedded_acl(chunk).get("deleted")
    if isinstance(embedded_deleted, bool):
        return embedded_deleted

    metadata_deleted = chunk.metadata.get("deleted")
    if isinstance(metadata_deleted, bool):
        return metadata_deleted
    if isinstance(metadata_deleted, str):
        return metadata_deleted.lower() == "true"
    return False


def build_chunk_context_opa_input(
    *,
    chunk: InferenceChunk,
    subject_user_id: str | None,
    subject_tenant_id: str | None,
    subject_groups: list[str] | tuple[str, ...] | set[str] | None,
    correlation_id: str,
) -> dict[str, Any]:
    """Build the OPA input for the exact chunk about to enter final RAG context."""

    resource_tenant_id = _embedded_acl_string(chunk, "tenant_id") or _metadata_string(
        chunk, "tenant_id"
    )
    resource_allowed_users = _embedded_acl_string_list(
        chunk, "user_ids"
    ) or _metadata_string_list(chunk, "allowed_users")
    resource_allowed_groups = _embedded_acl_string_list(
        chunk, "group_ids"
    ) or _metadata_string_list(chunk, "allowed_groups")
    resource_connector_id = _embedded_acl_string(
        chunk, "connector_id"
    ) or _metadata_string(chunk, "connector_id")
    resource_permission_version = _embedded_acl_string(
        chunk, "permission_version"
    ) or _metadata_string(chunk, "permission_version")

    return build_retrieval_acl_input(
        subject_user_id=subject_user_id,
        subject_tenant_id=subject_tenant_id,
        subject_groups=subject_groups,
        resource_document_id=chunk.document_id,
        resource_chunk_id=chunk.chunk_id,
        resource_tenant_id=resource_tenant_id,
        resource_allowed_users=resource_allowed_users,
        resource_allowed_groups=resource_allowed_groups,
        resource_connector_id=resource_connector_id,
        resource_deleted=_resource_deleted(chunk),
        resource_permission_version=resource_permission_version,
        correlation_id=correlation_id,
    )


def _opa_input_security_attributes(
    opa_input: dict[str, Any],
) -> dict[str, object | None]:
    subject = opa_input.get("subject", {})
    resource = opa_input.get("resource", {})
    subject_attributes = subject if isinstance(subject, dict) else {}
    resource_attributes = resource if isinstance(resource, dict) else {}
    return {
        "correlation_id": opa_input.get("correlation_id"),
        "subject_user_id": subject_attributes.get("user_id"),
        "subject_tenant_id": subject_attributes.get("tenant_id"),
        "resource_document_id": resource_attributes.get("document_id"),
        "resource_chunk_id": resource_attributes.get("chunk_id"),
        "resource_tenant_id": resource_attributes.get("tenant_id"),
        "enforcement_enabled": opa_retrieval_acl_context_enforcement_enabled(),
    }


def _opa_decision_security_attributes(
    decision: OPADecision,
) -> dict[str, object | None]:
    return {
        "correlation_id": decision.correlation_id,
        "subject_user_id": decision.subject_user_id,
        "subject_tenant_id": decision.subject_tenant_id,
        "resource_document_id": decision.resource_document_id,
        "resource_chunk_id": decision.resource_chunk_id,
        "resource_tenant_id": decision.resource_tenant_id,
        "policy_package": decision.policy_package,
        "decision": decision.decision.value,
        "reason": decision.reason,
        "fallback_used": decision.fallback_used,
        "enforcement_enabled": opa_retrieval_acl_context_enforcement_enabled(),
    }


def _evaluate_chunk(
    *,
    chunk: InferenceChunk,
    subject_user_id: str | None,
    subject_tenant_id: str | None,
    subject_groups: list[str] | tuple[str, ...] | set[str] | None,
    correlation_id: str,
    opa_client: OPAClient | RetrievalACLEvaluator,
) -> OPADecision:
    opa_input = build_chunk_context_opa_input(
        chunk=chunk,
        subject_user_id=subject_user_id,
        subject_tenant_id=subject_tenant_id,
        subject_groups=subject_groups,
        correlation_id=correlation_id,
    )
    with security_span(
        "security.opa.retrieval_acl.decision",
        _opa_input_security_attributes(opa_input),
    ) as span:
        if isinstance(opa_client, OPAClient):
            decision = evaluate_retrieval_acl_with_fallback(opa_client, opa_input)
        else:
            decision = opa_client.evaluate_retrieval_acl(opa_input)
        set_security_span_attributes(span, _opa_decision_security_attributes(decision))
        return decision


def _section_with_allowed_chunks(
    section: InferenceSection,
    allowed_chunks: list[InferenceChunk],
) -> InferenceSection | None:
    if not allowed_chunks:
        return None

    center_chunk = (
        section.center_chunk
        if section.center_chunk in allowed_chunks
        else allowed_chunks[0]
    )
    return InferenceSection(
        center_chunk=center_chunk,
        chunks=allowed_chunks,
        combined_content="\n".join(chunk.content for chunk in allowed_chunks),
    )


def filter_sections_for_opa_retrieval_acl_context(
    *,
    sections: list[InferenceSection],
    subject_user_id: str | None,
    subject_tenant_id: str | None,
    subject_groups: list[str] | tuple[str, ...] | set[str] | None,
    correlation_id: str,
    opa_client: OPAClient | RetrievalACLEvaluator | None = None,
) -> RetrievalContextOPAFilterResult:
    """Deny chunks before they are serialized into final RAG tool context.

    This is intentionally scoped to the final `InferenceSection` serialization
    seam: every chunk that contributes text to `section.combined_content` is
    evaluated, denied chunks are removed, and empty sections are dropped.
    """

    resolved_client = opa_client or OPAClient()
    filtered_sections: list[InferenceSection] = []
    decisions: list[OPADecision] = []

    with security_span(
        "security.opa.retrieval_context_filter",
        {
            "correlation_id": correlation_id,
            "subject_user_id": subject_user_id,
            "subject_tenant_id": subject_tenant_id,
            "enforcement_enabled": opa_retrieval_acl_context_enforcement_enabled(),
        },
    ) as span:
        for section in sections:
            allowed_chunks: list[InferenceChunk] = []
            for chunk in section.chunks:
                decision = _evaluate_chunk(
                    chunk=chunk,
                    subject_user_id=subject_user_id,
                    subject_tenant_id=subject_tenant_id,
                    subject_groups=subject_groups,
                    correlation_id=f"{correlation_id}:{chunk.document_id}:{chunk.chunk_id}",
                    opa_client=resolved_client,
                )
                decisions.append(decision)
                if decision.decision == OPADecisionValue.ALLOW:
                    allowed_chunks.append(chunk)

            filtered_section = _section_with_allowed_chunks(section, allowed_chunks)
            if filtered_section is not None:
                filtered_sections.append(filtered_section)

        set_security_span_attributes(
            span,
            {
                "decision_count": len(decisions),
                "allowed_section_count": len(filtered_sections),
            },
        )

    return RetrievalContextOPAFilterResult(
        sections=filtered_sections,
        decisions=tuple(decisions),
    )
