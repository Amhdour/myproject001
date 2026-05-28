from backend.security_layer.artifacts.controls import authorize_artifact_stage
from backend.security_layer.artifacts.metadata_contract import REQUIRED_ARTIFACT_METADATA_FIELDS
from backend.security_layer.artifacts.models import ArtifactDecisionStatus, ArtifactMetadata, ArtifactSafetyStage, ArtifactSecurityContext


def test_authorize_artifact_stage_allow() -> None:
    metadata = ArtifactMetadata(values={k: "x" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {"metadata_schema_version": "1.0"} | {"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    decision = authorize_artifact_stage(
        ArtifactSecurityContext(
            request_id="r1",
            stage=ArtifactSafetyStage.CONTENT_MALWARE_SCANNED,
            tenant_id_hash_or_safe_id="t",
            workspace_id_hash_or_safe_id="w",
            subject_id_hash_or_safe_id="s",
            storage_namespace="ns",
            authorized_storage_namespaces=("ns",),
            metadata=metadata,
        )
    )
    assert decision.status == ArtifactDecisionStatus.ALLOW
