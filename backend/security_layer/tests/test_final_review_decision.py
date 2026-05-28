from backend.security_layer.final_review.decision import build_final_review_checklist
from backend.security_layer.final_review.decision import evaluate_final_review
from backend.security_layer.final_review.decision import final_review_runtime_boundary_confirmed
from backend.security_layer.final_review.models import FinalReviewBundle
from backend.security_layer.final_review.models import FinalReviewDecision
from backend.security_layer.final_review.models import FinalReviewStatus


def test_default_final_review_checklist_keeps_pending_live_validation_blocker() -> None:
    checklist = build_final_review_checklist()
    status_by_id = {item.item_id: item.status for item in checklist}
    assert status_by_id["FR-001"] == FinalReviewStatus.CONFIRMED
    assert status_by_id["FR-002"] == FinalReviewStatus.CONFIRMED
    assert status_by_id["FR-003"] == FinalReviewStatus.PENDING
    assert status_by_id["FR-004"] == FinalReviewStatus.CONFIRMED
    assert status_by_id["FR-005"] == FinalReviewStatus.CONFIRMED


def test_default_final_review_outcome_allows_partner_demo_only() -> None:
    checklist = build_final_review_checklist()
    outcome = evaluate_final_review(checklist)
    assert outcome.partner_demo_evidence_review_decision == FinalReviewDecision.GO
    assert outcome.production_readiness_decision == FinalReviewDecision.NO_GO
    assert outcome.enterprise_production_readiness_decision == FinalReviewDecision.NO_GO
    assert outcome.live_staging_validation_status == FinalReviewStatus.PENDING
    assert outcome.external_validation_status == FinalReviewStatus.PENDING
    assert outcome.compliance_certification_status == FinalReviewStatus.NOT_CLAIMED
    assert outcome.runtime_boundary_confirmed is True
    assert outcome.blocking_item_ids == ("FR-003",)
    assert "partner-demo evidence review only" in outcome.final_recommendation


def test_runtime_boundary_violation_is_detected() -> None:
    bundle = FinalReviewBundle(enforce_mode_enabled=True)
    assert final_review_runtime_boundary_confirmed(bundle) is False
    checklist = build_final_review_checklist(bundle)
    boundary_item = next(item for item in checklist if item.item_id == "FR-005")
    assert boundary_item.status == FinalReviewStatus.PENDING
