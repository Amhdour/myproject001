from backend.security_layer.staging.execution import RealCoolifyExecutionDecision
from backend.security_layer.staging.execution import RealCoolifyExecutionMode
from backend.security_layer.staging.execution import RealCoolifyExecutionStatus
from backend.security_layer.staging.execution import RealCoolifyStagingExecutionBundle
from backend.security_layer.staging.execution import build_real_coolify_execution_checklist
from backend.security_layer.staging.execution import evaluate_real_coolify_execution
from backend.security_layer.staging.execution import real_coolify_execution_runtime_boundary_confirmed


def test_execution_bundle_defaults_to_no_real_deployment_and_pending_validation() -> None:
    bundle = RealCoolifyStagingExecutionBundle()
    assert bundle.branch_name == "real-coolify-staging-execution-bundle"
    assert bundle.mode == RealCoolifyExecutionMode.ISOLATED_HELPER_ONLY
    assert bundle.real_coolify_deployment_executed is False
    assert bundle.live_staging_validation_status == RealCoolifyExecutionStatus.PENDING
    assert bundle.partner_demo_evidence_review_decision == RealCoolifyExecutionDecision.GO
    assert bundle.production_readiness_decision == RealCoolifyExecutionDecision.NO_GO
    assert bundle.enterprise_production_readiness_decision == RealCoolifyExecutionDecision.NO_GO
    assert bundle.external_validation_status == RealCoolifyExecutionStatus.PENDING
    assert bundle.compliance_certification_status == RealCoolifyExecutionStatus.NOT_CLAIMED


def test_execution_bundle_preserves_runtime_boundary_defaults() -> None:
    bundle = RealCoolifyStagingExecutionBundle()
    assert real_coolify_execution_runtime_boundary_confirmed(bundle) is True
    assert bundle.enforce_mode_enabled is False
    assert bundle.shadow_deny_runtime_enabled is False
    assert bundle.live_blocking_enabled is False
    assert bundle.live_filtering_enabled is False
    assert bundle.application_behavior_changed is False
    assert bundle.production_readiness_claimed is False
    assert bundle.enterprise_production_readiness_claimed is False
    assert bundle.external_validation_claimed is False
    assert bundle.compliance_certification_claimed is False


def test_default_execution_checklist_keeps_live_execution_pending() -> None:
    checklist = build_real_coolify_execution_checklist()
    status_by_id = {item.item_id: item.status for item in checklist}
    assert status_by_id["RCSE-001"] == RealCoolifyExecutionStatus.CONFIRMED
    assert status_by_id["RCSE-002"] == RealCoolifyExecutionStatus.CONFIRMED
    assert status_by_id["RCSE-003"] == RealCoolifyExecutionStatus.PENDING
    assert status_by_id["RCSE-004"] == RealCoolifyExecutionStatus.PENDING
    assert status_by_id["RCSE-005"] == RealCoolifyExecutionStatus.CONFIRMED


def test_default_execution_outcome_allows_partner_demo_only() -> None:
    checklist = build_real_coolify_execution_checklist()
    outcome = evaluate_real_coolify_execution(checklist)
    assert outcome.partner_demo_evidence_review_decision == RealCoolifyExecutionDecision.GO
    assert outcome.production_readiness_decision == RealCoolifyExecutionDecision.NO_GO
    assert outcome.enterprise_production_readiness_decision == RealCoolifyExecutionDecision.NO_GO
    assert outcome.real_coolify_deployment_executed is False
    assert outcome.live_staging_validation_status == RealCoolifyExecutionStatus.PENDING
    assert outcome.external_validation_status == RealCoolifyExecutionStatus.PENDING
    assert outcome.compliance_certification_status == RealCoolifyExecutionStatus.NOT_CLAIMED
    assert outcome.runtime_boundary_confirmed is True
    assert outcome.blocking_item_ids == ("RCSE-003", "RCSE-004")
    assert "partner-demo evidence review only" in outcome.final_recommendation


def test_runtime_boundary_violation_is_detected() -> None:
    bundle = RealCoolifyStagingExecutionBundle(shadow_deny_runtime_enabled=True)
    assert real_coolify_execution_runtime_boundary_confirmed(bundle) is False
    checklist = build_real_coolify_execution_checklist(bundle)
    boundary_item = next(item for item in checklist if item.item_id == "RCSE-005")
    assert boundary_item.status == RealCoolifyExecutionStatus.PENDING


def test_execution_model_fields_do_not_store_secret_material() -> None:
    field_names = set(RealCoolifyStagingExecutionBundle.__dataclass_fields__)
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
