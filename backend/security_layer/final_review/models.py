"""Models for the final pilot partner go/no-go review bundle.

These models are intentionally isolated data helpers. They do not enable
runtime enforcement, call external services, mutate feature flags, or change
application behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

SCHEMA_VERSION = "final-pilot-partner-go-no-go.v1"


class FinalReviewDecision(StrEnum):
    """Allowed final review decision values."""

    GO = "GO"
    NO_GO = "NO-GO"


class FinalReviewStatus(StrEnum):
    """Allowed validation and claim status values."""

    PENDING = "PENDING"
    NOT_CLAIMED = "NOT CLAIMED"
    CONFIRMED = "CONFIRMED"


class FinalReviewMode(StrEnum):
    """Boundary modes for the final review bundle."""

    DOCUMENTATION_ONLY = "documentation_only"
    ISOLATED_HELPER_ONLY = "isolated_helper_only"


@dataclass(frozen=True)
class FinalReviewBundle:
    """Static final pilot partner go/no-go evidence metadata."""

    bundle_id: str = "final_pilot_partner_go_no_go_bundle"
    branch_name: str = "final-pilot-partner-go-no-go-bundle"
    mode: FinalReviewMode = FinalReviewMode.ISOLATED_HELPER_ONLY
    partner_demo_evidence_review_decision: FinalReviewDecision = FinalReviewDecision.GO
    production_readiness_decision: FinalReviewDecision = FinalReviewDecision.NO_GO
    enterprise_production_readiness_decision: FinalReviewDecision = FinalReviewDecision.NO_GO
    live_staging_validation_status: FinalReviewStatus = FinalReviewStatus.PENDING
    external_validation_status: FinalReviewStatus = FinalReviewStatus.PENDING
    compliance_certification_status: FinalReviewStatus = FinalReviewStatus.NOT_CLAIMED
    enforce_mode_enabled: bool = False
    shadow_deny_runtime_enabled: bool = False
    live_blocking_enabled: bool = False
    live_filtering_enabled: bool = False
    application_behavior_changed: bool = False
    production_readiness_claimed: bool = False
    enterprise_production_readiness_claimed: bool = False
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class FinalReviewChecklistItem:
    """Single checklist item for final partner-demo review."""

    item_id: str
    title: str
    status: FinalReviewStatus
    evidence_reference: str
    blocks_production_claim: bool
    sanitized_notes: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class FinalReviewOutcome:
    """Evaluated final review outcome and safety confirmations."""

    partner_demo_evidence_review_decision: FinalReviewDecision
    production_readiness_decision: FinalReviewDecision
    enterprise_production_readiness_decision: FinalReviewDecision
    live_staging_validation_status: FinalReviewStatus
    external_validation_status: FinalReviewStatus
    compliance_certification_status: FinalReviewStatus
    runtime_boundary_confirmed: bool
    blocking_item_ids: tuple[str, ...]
    final_recommendation: str
    schema_version: str = SCHEMA_VERSION
