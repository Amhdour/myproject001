from backend.security_layer.final_review.models import FinalReviewBundle
from backend.security_layer.final_review.models import FinalReviewDecision
from backend.security_layer.final_review.models import FinalReviewMode
from backend.security_layer.final_review.models import FinalReviewStatus


def test_final_review_bundle_defaults_to_required_decisions() -> None:
    bundle = FinalReviewBundle()
    assert bundle.branch_name == "final-pilot-partner-go-no-go-bundle"
    assert bundle.mode == FinalReviewMode.ISOLATED_HELPER_ONLY
    assert bundle.partner_demo_evidence_review_decision == FinalReviewDecision.GO
    assert bundle.production_readiness_decision == FinalReviewDecision.NO_GO
    assert bundle.enterprise_production_readiness_decision == FinalReviewDecision.NO_GO
    assert bundle.live_staging_validation_status == FinalReviewStatus.PENDING
    assert bundle.external_validation_status == FinalReviewStatus.PENDING
    assert bundle.compliance_certification_status == FinalReviewStatus.NOT_CLAIMED


def test_final_review_bundle_preserves_runtime_boundary_defaults() -> None:
    bundle = FinalReviewBundle()
    assert bundle.enforce_mode_enabled is False
    assert bundle.shadow_deny_runtime_enabled is False
    assert bundle.live_blocking_enabled is False
    assert bundle.live_filtering_enabled is False
    assert bundle.application_behavior_changed is False
    assert bundle.production_readiness_claimed is False
    assert bundle.enterprise_production_readiness_claimed is False


def test_final_review_model_fields_do_not_store_secret_material() -> None:
    field_names = set(FinalReviewBundle.__dataclass_fields__)
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
