from backend.security_layer.evidence_room.models import PartnerEvidenceRoomBundle
from backend.security_layer.evidence_room.models import PartnerEvidenceStatus


def test_partner_evidence_room_bundle_defaults_are_safe() -> None:
    bundle = PartnerEvidenceRoomBundle()
    assert bundle.branch_name == "partner-evidence-room-bundle"
    assert bundle.partner_evidence_review_decision == PartnerEvidenceStatus.GO
    assert bundle.production_readiness_decision == PartnerEvidenceStatus.NO_GO
    assert bundle.live_staging_validation_status == PartnerEvidenceStatus.PENDING
    assert bundle.external_validation_status == PartnerEvidenceStatus.PENDING
    assert bundle.compliance_certification_status == PartnerEvidenceStatus.NOT_CLAIMED


def test_partner_evidence_room_bundle_does_not_enable_runtime_modes() -> None:
    bundle = PartnerEvidenceRoomBundle()
    assert bundle.enforce_mode_enabled is False
    assert bundle.shadow_deny_runtime_enabled is False
    assert bundle.live_blocking_enabled is False
    assert bundle.live_filtering_enabled is False
    assert bundle.application_behavior_changed is False


def test_partner_evidence_room_bundle_does_not_claim_readiness_or_validation() -> None:
    bundle = PartnerEvidenceRoomBundle()
    assert bundle.production_readiness_claimed is False
    assert bundle.external_validation_claimed is False
    assert bundle.compliance_certification_claimed is False
