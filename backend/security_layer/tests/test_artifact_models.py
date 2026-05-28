from backend.security_layer.artifacts.models import ArtifactSafetyStage


def test_artifact_safety_stage_count_is_24() -> None:
    assert len(ArtifactSafetyStage) == 24
