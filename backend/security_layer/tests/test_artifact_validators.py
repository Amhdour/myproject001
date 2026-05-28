from backend.security_layer.artifacts.metadata_contract import REQUIRED_ARTIFACT_METADATA_FIELDS
from backend.security_layer.artifacts.models import ArtifactMetadata, ArtifactSafetyStage, ArtifactSecurityContext
from backend.security_layer.artifacts.validators import validate_artifact_context_and_metadata


def test_validate_artifact_context_and_metadata() -> None:
    metadata = ArtifactMetadata(values={k: "x" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {"metadata_schema_version": "1.0"} | {"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    context = ArtifactSecurityContext(
        request_id="r1",
        stage=ArtifactSafetyStage.UPLOAD_REQUESTED,
        tenant_id_hash_or_safe_id="t",
        workspace_id_hash_or_safe_id="w",
        subject_id_hash_or_safe_id="s",
        storage_namespace="ns",
        authorized_storage_namespaces=("ns",),
        metadata=metadata,
    )
    assert validate_artifact_context_and_metadata(context)
