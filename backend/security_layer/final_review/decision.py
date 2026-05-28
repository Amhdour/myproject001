"""Decision helpers for the final pilot partner go/no-go bundle.

The helpers only transform in-memory review metadata into checklist and outcome
records. They do not enable enforce mode, shadow-deny runtime mode, live
blocking, live filtering, or any live application path.
"""

from __future__ import annotations

from backend.security_layer.final_review.models import FinalReviewBundle
from backend.security_layer.final_review.models import FinalReviewChecklistItem
from backend.security_layer.final_review.models import FinalReviewDecision
from backend.security_layer.final_review.models import FinalReviewOutcome
from backend.security_layer.final_review.models import FinalReviewStatus


def build_final_review_checklist(
    bundle: FinalReviewBundle | None = None,
) -> tuple[FinalReviewChecklistItem, ...]:
    """Build the final review checklist from sanitized evidence metadata."""

    review_bundle = bundle or FinalReviewBundle()
    return (
        FinalReviewChecklistItem(
            item_id="FR-001",
            title="Partner-demo evidence package is indexed",
            status=FinalReviewStatus.CONFIRMED,
            evidence_reference="docs/security/final_evidence_package_index.md",
            blocks_production_claim=False,
            sanitized_notes="Final evidence index references sanitized partner-demo artifacts only.",
        ),
        FinalReviewChecklistItem(
            item_id="FR-002",
            title="Claim boundary keeps production claims out of scope",
            status=(
                FinalReviewStatus.CONFIRMED
                if not review_bundle.production_readiness_claimed
                and not review_bundle.enterprise_production_readiness_claimed
                else FinalReviewStatus.PENDING
            ),
            evidence_reference="docs/security/final_claim_boundary.md",
            blocks_production_claim=True,
            sanitized_notes="Production and enterprise production readiness are explicitly no-go.",
        ),
        FinalReviewChecklistItem(
            item_id="FR-003",
            title="Live staging validation remains pending unless real evidence exists",
            status=review_bundle.live_staging_validation_status,
            evidence_reference="docs/security/final_open_blockers.md",
            blocks_production_claim=True,
            sanitized_notes="No live staging validation is claimed by this final review bundle.",
        ),
        FinalReviewChecklistItem(
            item_id="FR-004",
            title="External validation and compliance certification are not claimed",
            status=(
                FinalReviewStatus.CONFIRMED
                if review_bundle.external_validation_status == FinalReviewStatus.PENDING
                and review_bundle.compliance_certification_status == FinalReviewStatus.NOT_CLAIMED
                else FinalReviewStatus.PENDING
            ),
            evidence_reference="docs/security/final_claim_boundary.md",
            blocks_production_claim=True,
            sanitized_notes="External validation is pending and compliance certification is not claimed.",
        ),
        FinalReviewChecklistItem(
            item_id="FR-005",
            title="Runtime safety boundary remains unchanged",
            status=(
                FinalReviewStatus.CONFIRMED
                if final_review_runtime_boundary_confirmed(review_bundle)
                else FinalReviewStatus.PENDING
            ),
            evidence_reference="docs/security/final_pilot_partner_go_no_go.md",
            blocks_production_claim=True,
            sanitized_notes="No enforce mode, shadow-deny runtime, live blocking, live filtering, or behavior change is enabled.",
        ),
    )


def evaluate_final_review(
    checklist: tuple[FinalReviewChecklistItem, ...],
    bundle: FinalReviewBundle | None = None,
) -> FinalReviewOutcome:
    """Evaluate final partner-demo go/no-go decisions."""

    review_bundle = bundle or FinalReviewBundle()
    blocking_item_ids = tuple(
        item.item_id
        for item in checklist
        if item.blocks_production_claim and item.status != FinalReviewStatus.CONFIRMED
    )
    runtime_boundary_confirmed = final_review_runtime_boundary_confirmed(review_bundle)
    return FinalReviewOutcome(
        partner_demo_evidence_review_decision=FinalReviewDecision.GO,
        production_readiness_decision=FinalReviewDecision.NO_GO,
        enterprise_production_readiness_decision=FinalReviewDecision.NO_GO,
        live_staging_validation_status=review_bundle.live_staging_validation_status,
        external_validation_status=review_bundle.external_validation_status,
        compliance_certification_status=review_bundle.compliance_certification_status,
        runtime_boundary_confirmed=runtime_boundary_confirmed,
        blocking_item_ids=blocking_item_ids,
        final_recommendation=(
            "Proceed with partner-demo evidence review only. Do not proceed with "
            "production-readiness, enterprise production-readiness, live-staging, "
            "external-validation, or compliance-certification claims until real "
            "evidence exists and is reviewed separately."
        ),
    )


def final_review_runtime_boundary_confirmed(bundle: FinalReviewBundle) -> bool:
    """Return whether the bundle preserves all no-live-change boundaries."""

    return not any(
        (
            bundle.enforce_mode_enabled,
            bundle.shadow_deny_runtime_enabled,
            bundle.live_blocking_enabled,
            bundle.live_filtering_enabled,
            bundle.application_behavior_changed,
            bundle.production_readiness_claimed,
            bundle.enterprise_production_readiness_claimed,
        )
    )
