from backend.security_layer.artifacts.metadata_contract import REQUIRED_ARTIFACT_METADATA_FIELDS
from backend.security_layer.artifacts.models import ArtifactDecisionStatus, ArtifactMetadata, ArtifactSafetyStage, ArtifactSecurityContext
from backend.security_layer.artifacts.validators import (
    build_artifact_decision,
    validate_artifact_content,
    validate_artifact_context_and_metadata,
    validate_artifact_type,
    validate_download_authorization,
    validate_retention_deletion_authorization,
)


def _context(**overrides: str | tuple[str, ...] | ArtifactMetadata | None) -> ArtifactSecurityContext:
    metadata = ArtifactMetadata(values={k: "x" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {"metadata_schema_version": "1.0", "release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    base = dict(request_id="r1", stage=ArtifactSafetyStage.UPLOAD_REQUESTED, tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", subject_id_hash_or_safe_id="s", storage_namespace="ns", authorized_storage_namespaces=("ns",), metadata=metadata)
    base.update(overrides)
    return ArtifactSecurityContext(**base)


def test_context_and_metadata_failure_modes() -> None:
    assert not validate_artifact_context_and_metadata(_context(tenant_id_hash_or_safe_id=None))
    assert not validate_artifact_context_and_metadata(_context(subject_id_hash_or_safe_id=None))
    assert not validate_artifact_context_and_metadata(_context(workspace_id_hash_or_safe_id=None))
    assert not validate_artifact_context_and_metadata(_context(metadata=None))


def test_unknown_artifact_and_authz_validations() -> None:
    assert not validate_artifact_type("unknown")
    assert validate_artifact_type("report")
    assert not validate_download_authorization(False)
    assert validate_download_authorization(True)
    assert not validate_retention_deletion_authorization(False)


def test_content_markers_and_non_leakage_decision() -> None:
    assert not validate_artifact_content("api_key=abc")[0]
    assert not validate_artifact_content("raw_document_text marker")[0]
    decision = build_artifact_decision(_context(), ArtifactDecisionStatus.DENY, "blocked")
    assert "raw_payload" not in str(decision)
    assert "policy_internal" not in str(decision)
