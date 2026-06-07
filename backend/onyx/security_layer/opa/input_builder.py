from __future__ import annotations

from typing import Any

RETRIEVAL_ACL_ACTION = "rag.context.include"


def _normalize_string_list(values: list[str] | tuple[str, ...] | set[str] | None) -> list[str]:
    if values is None:
        return []
    return sorted({str(value) for value in values if str(value)})


def build_retrieval_acl_input(
    *,
    subject_user_id: str | None,
    subject_tenant_id: str | None,
    subject_groups: list[str] | tuple[str, ...] | set[str] | None,
    resource_document_id: str | None,
    resource_chunk_id: str | int | None,
    resource_tenant_id: str | None,
    resource_allowed_users: list[str] | tuple[str, ...] | set[str] | None,
    resource_allowed_groups: list[str] | tuple[str, ...] | set[str] | None,
    resource_connector_id: str | None,
    resource_deleted: bool,
    resource_permission_version: str | int | None,
    correlation_id: str,
) -> dict[str, Any]:
    """Build the normalized OPA input for a Retrieval ACL context-inclusion decision."""

    return {
        "subject": {
            "user_id": str(subject_user_id) if subject_user_id is not None else None,
            "tenant_id": str(subject_tenant_id) if subject_tenant_id is not None else None,
            "groups": _normalize_string_list(subject_groups),
        },
        "resource": {
            "document_id": str(resource_document_id) if resource_document_id is not None else None,
            "chunk_id": str(resource_chunk_id) if resource_chunk_id is not None else None,
            "tenant_id": str(resource_tenant_id) if resource_tenant_id is not None else None,
            "allowed_users": _normalize_string_list(resource_allowed_users),
            "allowed_groups": _normalize_string_list(resource_allowed_groups),
            "connector_id": str(resource_connector_id) if resource_connector_id is not None else None,
            "deleted": resource_deleted,
            "permission_version": str(resource_permission_version) if resource_permission_version is not None else None,
        },
        "action": RETRIEVAL_ACL_ACTION,
        "correlation_id": correlation_id,
    }
