"""Partner evidence room index helpers.

These helpers only build in-memory manifests and summary decisions for the
partner evidence room. They do not read secrets, call services, alter feature
flags, wire request paths, or change application behavior.
"""

from __future__ import annotations

from backend.security_layer.evidence_room.models import PartnerEvidenceCategory
from backend.security_layer.evidence_room.models import PartnerEvidenceDocument
from backend.security_layer.evidence_room.models import PartnerEvidenceFile
from backend.security_layer.evidence_room.models import PartnerEvidenceRoomBundle
from backend.security_layer.evidence_room.models import PartnerEvidenceStatus

REQUIRED_PARTNER_DOCUMENT_PATHS: tuple[str, ...] = (
    "docs/security/partner_evidence_room.md",
    "docs/security/partner_safe_claims.md",
    "docs/security/partner_demo_walkthrough.md",
    "docs/security/partner_control_coverage_summary.md",
    "docs/security/partner_test_evidence_index.md",
    "docs/security/partner_demo_attack_summary.md",
    "docs/security/partner_limitations_and_next_steps.md",
    "docs/security/partner_evidence_index.md",
    "docs/security/partner_go_no_go.md",
)

REQUIRED_PARTNER_EVIDENCE_PATHS: tuple[str, ...] = (
    "docs/security/evidence/partner_evidence_room_bundle/prerequisite_check.txt",
    "docs/security/evidence/partner_evidence_room_bundle/evidence_room_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/safe_claims_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/demo_walkthrough_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/control_coverage_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/test_evidence_index_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/demo_attack_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/limitations_next_steps_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/go_no_go_summary.md",
    "docs/security/evidence/partner_evidence_room_bundle/evidence_room_helper_coverage.md",
    "docs/security/evidence/partner_evidence_room_bundle/test_output.txt",
    "docs/security/evidence/partner_evidence_room_bundle/test_exitcode.txt",
    "docs/security/evidence/partner_evidence_room_bundle/remote_sync_limitation.txt",
)


def build_partner_evidence_documents() -> tuple[PartnerEvidenceDocument, ...]:
    """Return the required Step 30X partner-facing document manifest."""

    return (
        PartnerEvidenceDocument(
            document_id="PER-DOC-001",
            title="Partner evidence room overview",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[0],
            category=PartnerEvidenceCategory.EVIDENCE_ROOM,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Navigation hub for sanitized partner evidence and non-claims.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-002",
            title="Partner safe claims",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[1],
            category=PartnerEvidenceCategory.SAFE_CLAIMS,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Approved wording boundaries that avoid production, certification, and external-validation claims.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-003",
            title="Partner demo walkthrough",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[2],
            category=PartnerEvidenceCategory.DEMO_WALKTHROUGH,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Demo script for documentation-only review without live blocking or filtering.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-004",
            title="Partner control coverage summary",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[3],
            category=PartnerEvidenceCategory.CONTROL_COVERAGE,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Summary of control-family evidence with limitations called out.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-005",
            title="Partner test evidence index",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[4],
            category=PartnerEvidenceCategory.TEST_EVIDENCE,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Index of focused and full security-layer test commands and outputs.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-006",
            title="Partner demo attack summary",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[5],
            category=PartnerEvidenceCategory.DEMO_ATTACKS,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="High-level demo attack coverage without claiming live attack validation.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-007",
            title="Partner limitations and next steps",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[6],
            category=PartnerEvidenceCategory.LIMITATIONS,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Open limitations including pending live staging and external validation.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-008",
            title="Partner evidence index",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[7],
            category=PartnerEvidenceCategory.INDEX,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Cross-reference index for all partner bundle documents and evidence files.",
        ),
        PartnerEvidenceDocument(
            document_id="PER-DOC-009",
            title="Partner go/no-go",
            path=REQUIRED_PARTNER_DOCUMENT_PATHS[8],
            category=PartnerEvidenceCategory.GO_NO_GO,
            status=PartnerEvidenceStatus.GO,
            sanitized_summary="GO for partner evidence review; NO-GO for production readiness.",
        ),
    )


def build_partner_evidence_files() -> tuple[PartnerEvidenceFile, ...]:
    """Return the required Step 30X evidence artifact manifest."""

    return tuple(
        PartnerEvidenceFile(
            evidence_id=f"PER-EV-{index:03d}",
            path=path,
            status=PartnerEvidenceStatus.PASSED,
            sanitized_summary="Sanitized Step 30X evidence-room artifact.",
        )
        for index, path in enumerate(REQUIRED_PARTNER_EVIDENCE_PATHS, start=1)
    )


def evaluate_partner_evidence_room_bundle(
    bundle: PartnerEvidenceRoomBundle | None = None,
) -> PartnerEvidenceRoomBundle:
    """Return the partner evidence-room decision with safe defaults."""

    evidence_bundle = bundle or PartnerEvidenceRoomBundle()
    if _bundle_preserves_runtime_boundary(evidence_bundle):
        return evidence_bundle
    return PartnerEvidenceRoomBundle(
        partner_evidence_review_decision=PartnerEvidenceStatus.NO_GO,
        production_readiness_decision=PartnerEvidenceStatus.NO_GO,
        live_staging_validation_status=evidence_bundle.live_staging_validation_status,
        external_validation_status=evidence_bundle.external_validation_status,
        compliance_certification_status=evidence_bundle.compliance_certification_status,
        enforce_mode_enabled=evidence_bundle.enforce_mode_enabled,
        shadow_deny_runtime_enabled=evidence_bundle.shadow_deny_runtime_enabled,
        live_blocking_enabled=evidence_bundle.live_blocking_enabled,
        live_filtering_enabled=evidence_bundle.live_filtering_enabled,
        application_behavior_changed=evidence_bundle.application_behavior_changed,
        production_readiness_claimed=evidence_bundle.production_readiness_claimed,
        external_validation_claimed=evidence_bundle.external_validation_claimed,
        compliance_certification_claimed=evidence_bundle.compliance_certification_claimed,
    )


def _bundle_preserves_runtime_boundary(bundle: PartnerEvidenceRoomBundle) -> bool:
    return not any(
        (
            bundle.enforce_mode_enabled,
            bundle.shadow_deny_runtime_enabled,
            bundle.live_blocking_enabled,
            bundle.live_filtering_enabled,
            bundle.application_behavior_changed,
            bundle.production_readiness_claimed,
            bundle.external_validation_claimed,
            bundle.compliance_certification_claimed,
        )
    )
