from backend.security_layer.staging.models import CoolifyStagingEvidenceBundle
from backend.security_layer.staging.models import CoolifyStagingMode
from backend.security_layer.staging.models import CoolifyStagingStatus


def test_staging_bundle_defaults_to_pending_live_validation() -> None:
    bundle = CoolifyStagingEvidenceBundle()
    assert bundle.branch_name == "coolify-staging-evidence-bundle"
    assert bundle.mode == CoolifyStagingMode.ISOLATED_HELPER_ONLY
    assert bundle.live_deployment_status == CoolifyStagingStatus.PENDING
    assert bundle.live_validation_status == CoolifyStagingStatus.PENDING


def test_staging_bundle_preserves_runtime_boundary_defaults() -> None:
    bundle = CoolifyStagingEvidenceBundle()
    assert bundle.enforce_mode_enabled is False
    assert bundle.shadow_deny_runtime_enabled is False
    assert bundle.live_blocking_enabled is False
    assert bundle.live_filtering_enabled is False
    assert bundle.application_behavior_changed is False
    assert bundle.production_readiness_claimed is False


def test_staging_model_fields_do_not_store_real_endpoint_or_secret_values() -> None:
    field_names = set(CoolifyStagingEvidenceBundle.__dataclass_fields__)
    forbidden = {
        "domain",
        "ip_address",
        "credential",
        "credentials",
        "token",
        "private_key",
        "secret",
        "password",
        "api_key",
    }
    assert field_names.isdisjoint(forbidden)
