from __future__ import annotations

from backend.security_layer.artifacts.content_scanners import scan_artifact_malware_markers, scan_artifact_policy_markers, scan_artifact_secret_markers
from backend.security_layer.artifacts.metadata_contract import sanitize_metadata_for_decision, validate_artifact_metadata
from backend.security_layer.artifacts.models import ArtifactDecisionStatus, ArtifactSecurityContext, ArtifactSecurityDecision
from backend.security_layer.artifacts.release_policy import validate_artifact_release_policy
from backend.security_layer.runtime.denials import DenialCategory

_ALLOWED_ARTIFACT_TYPES = {"report", "export", "summary", "analysis", "log"}


def validate_artifact_context(context: ArtifactSecurityContext) -> bool:
    return bool(context.tenant_id_hash_or_safe_id and context.workspace_id_hash_or_safe_id and context.subject_id_hash_or_safe_id and context.storage_namespace)


def validate_artifact_namespace_authorization(context: ArtifactSecurityContext) -> bool:
    return context.storage_namespace in context.authorized_storage_namespaces


def validate_artifact_content(content: str) -> tuple[bool, list[str]]:
    if not scan_artifact_malware_markers(content):
        return False, ["malware_marker_detected"]
    if not scan_artifact_secret_markers(content):
        return False, ["secret_marker_detected"]
    ok, flags = scan_artifact_policy_markers(content)
    return ok, flags


def validate_artifact_context_and_metadata(context: ArtifactSecurityContext) -> bool:
    if context.metadata is None:
        return False
    return validate_artifact_context(context) and validate_artifact_metadata(context.metadata.values) and validate_artifact_release_policy(context.metadata.values)


def validate_artifact_type(artifact_type: str) -> bool:
    return artifact_type in _ALLOWED_ARTIFACT_TYPES


def validate_download_authorization(is_authorized: bool) -> bool:
    return is_authorized


def validate_retention_deletion_authorization(can_delete: bool) -> bool:
    return can_delete


def build_artifact_decision(
    context: ArtifactSecurityContext,
    status: ArtifactDecisionStatus,
    reason: str,
    denial_category: DenialCategory | None = None,
    flags: list[str] | None = None,
) -> ArtifactSecurityDecision:
    safe_metadata = sanitize_metadata_for_decision(context.metadata.values) if context.metadata else {}
    return ArtifactSecurityDecision(
        stage=context.stage,
        status=status,
        reason=reason,
        denial_category=denial_category,
        flags=tuple(flags or []),
        metadata=safe_metadata,
    )
