from backend.security_layer.artifacts.metadata_contract import REQUIRED_ARTIFACT_METADATA_FIELDS, validate_artifact_metadata


def _valid_metadata() -> dict[str, str | bool]:
    return {k: "x" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {"metadata_schema_version": "1.0"}


def test_required_metadata_field_count_is_33() -> None:
    assert len(REQUIRED_ARTIFACT_METADATA_FIELDS) == 33


def test_validate_artifact_metadata_accepts_complete_payload() -> None:
    assert validate_artifact_metadata(_valid_metadata())
