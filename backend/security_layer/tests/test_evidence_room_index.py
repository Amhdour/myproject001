from backend.security_layer.evidence_room.index import REQUIRED_PARTNER_DOCUMENT_PATHS
from backend.security_layer.evidence_room.index import REQUIRED_PARTNER_EVIDENCE_PATHS
from backend.security_layer.evidence_room.index import build_partner_evidence_documents
from backend.security_layer.evidence_room.index import build_partner_evidence_files
from backend.security_layer.evidence_room.index import evaluate_partner_evidence_room_bundle
from backend.security_layer.evidence_room.models import PartnerEvidenceRoomBundle
from backend.security_layer.evidence_room.models import PartnerEvidenceStatus


def test_partner_document_manifest_contains_required_nine_docs() -> None:
    documents = build_partner_evidence_documents()
    assert len(documents) == 9
    assert tuple(document.path for document in documents) == REQUIRED_PARTNER_DOCUMENT_PATHS
    assert documents[-1].status == PartnerEvidenceStatus.GO


def test_partner_evidence_manifest_contains_required_artifacts() -> None:
    evidence_files = build_partner_evidence_files()
    assert len(evidence_files) == len(REQUIRED_PARTNER_EVIDENCE_PATHS)
    assert tuple(evidence.path for evidence in evidence_files) == REQUIRED_PARTNER_EVIDENCE_PATHS
    assert all(evidence.status == PartnerEvidenceStatus.PASSED for evidence in evidence_files)


def test_partner_evidence_room_default_decision_is_go_for_review_only() -> None:
    decision = evaluate_partner_evidence_room_bundle()
    assert decision.partner_evidence_review_decision == PartnerEvidenceStatus.GO
    assert decision.production_readiness_decision == PartnerEvidenceStatus.NO_GO
    assert decision.live_staging_validation_status == PartnerEvidenceStatus.PENDING
    assert decision.external_validation_status == PartnerEvidenceStatus.PENDING
    assert decision.compliance_certification_status == PartnerEvidenceStatus.NOT_CLAIMED


def test_partner_evidence_room_runtime_boundary_violation_blocks_review_go() -> None:
    unsafe_bundle = PartnerEvidenceRoomBundle(live_blocking_enabled=True)
    decision = evaluate_partner_evidence_room_bundle(unsafe_bundle)
    assert decision.partner_evidence_review_decision == PartnerEvidenceStatus.NO_GO
    assert decision.production_readiness_decision == PartnerEvidenceStatus.NO_GO
    assert decision.live_blocking_enabled is True
