from backend.security_layer.staging.checklist import build_coolify_staging_checklist
from backend.security_layer.staging.checklist import evaluate_coolify_staging_go_no_go
from backend.security_layer.staging.models import CoolifyStagingEvidenceBundle
from backend.security_layer.staging.models import CoolifyStagingStatus


def test_default_checklist_marks_live_execution_and_validation_pending() -> None:
    checklist = build_coolify_staging_checklist()
    status_by_id = {item.item_id: item.status for item in checklist}
    assert status_by_id["CS-001"] == CoolifyStagingStatus.PASSED
    assert status_by_id["CS-002"] == CoolifyStagingStatus.PASSED
    assert status_by_id["CS-003"] == CoolifyStagingStatus.PENDING
    assert status_by_id["CS-004"] == CoolifyStagingStatus.PENDING
    assert status_by_id["CS-005"] == CoolifyStagingStatus.PASSED


def test_default_go_no_go_blocks_until_live_staging_validation_exists() -> None:
    checklist = build_coolify_staging_checklist()
    decision = evaluate_coolify_staging_go_no_go(checklist)
    assert decision.status == CoolifyStagingStatus.BLOCKED
    assert decision.live_staging_validation_status == CoolifyStagingStatus.PENDING
    assert decision.blocking_item_ids == ("CS-003", "CS-004")
    assert decision.production_readiness_claimed is False


def test_runtime_boundary_violation_blocks_checklist() -> None:
    bundle = CoolifyStagingEvidenceBundle(enforce_mode_enabled=True)
    checklist = build_coolify_staging_checklist(bundle)
    boundary_item = next(item for item in checklist if item.item_id == "CS-005")
    assert boundary_item.status == CoolifyStagingStatus.BLOCKED
