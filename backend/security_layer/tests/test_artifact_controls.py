from backend.security_layer.artifacts.controls import authorize_artifact_stage
from backend.security_layer.artifacts.metadata_contract import REQUIRED_ARTIFACT_METADATA_FIELDS
from backend.security_layer.artifacts.models import ArtifactDecisionStatus, ArtifactMetadata, ArtifactSafetyStage, ArtifactSecurityContext


def _context(stage: ArtifactSafetyStage, storage_namespace: str = "ns") -> ArtifactSecurityContext:
    metadata = ArtifactMetadata(values={k: "x" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {"metadata_schema_version": "1.0", "release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    return ArtifactSecurityContext(request_id="r1", stage=stage, tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", subject_id_hash_or_safe_id="s", storage_namespace=storage_namespace, authorized_storage_namespaces=("ns",), metadata=metadata)


def test_all_24_stages_have_isolated_control_path() -> None:
    for stage in ArtifactSafetyStage:
        assert authorize_artifact_stage(_context(stage)).status == ArtifactDecisionStatus.ALLOW


def test_denied_on_unauthorized_namespace() -> None:
    decision = authorize_artifact_stage(_context(ArtifactSafetyStage.UPLOAD_REQUESTED, storage_namespace="other"))
    assert decision.status == ArtifactDecisionStatus.DENY
