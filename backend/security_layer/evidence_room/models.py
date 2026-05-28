"""Models for the partner evidence room bundle.

The evidence room schema is deliberately documentation-only. It stores safe
manifest metadata, review statuses, and claim boundaries. It does not enable
runtime enforcement, shadow-deny runtime mode, live blocking, live filtering, or
any application-path behavior changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

SCHEMA_VERSION = "partner-evidence-room.v1"
BRANCH_NAME = "partner-evidence-room-bundle"


class PartnerEvidenceStatus(StrEnum):
    """Allowed statuses for partner evidence room records."""

    PASSED = "passed"
    PENDING = "pending"
    GO = "go"
    NO_GO = "no_go"
    NOT_CLAIMED = "not_claimed"


class PartnerEvidenceCategory(StrEnum):
    """Document categories represented in the partner evidence room."""

    EVIDENCE_ROOM = "evidence_room"
    SAFE_CLAIMS = "safe_claims"
    DEMO_WALKTHROUGH = "demo_walkthrough"
    CONTROL_COVERAGE = "control_coverage"
    TEST_EVIDENCE = "test_evidence"
    DEMO_ATTACKS = "demo_attacks"
    LIMITATIONS = "limitations"
    INDEX = "index"
    GO_NO_GO = "go_no_go"


@dataclass(frozen=True)
class PartnerEvidenceDocument:
    """Single document entry exposed through the evidence-room index."""

    document_id: str
    title: str
    path: str
    category: PartnerEvidenceCategory
    status: PartnerEvidenceStatus
    sanitized_summary: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class PartnerEvidenceFile:
    """Single evidence artifact entry for partner-review evidence."""

    evidence_id: str
    path: str
    status: PartnerEvidenceStatus
    sanitized_summary: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class PartnerEvidenceRoomBundle:
    """Top-level partner evidence room boundary and status metadata."""

    bundle_id: str = "partner_evidence_room_bundle"
    branch_name: str = BRANCH_NAME
    partner_evidence_review_decision: PartnerEvidenceStatus = PartnerEvidenceStatus.GO
    production_readiness_decision: PartnerEvidenceStatus = PartnerEvidenceStatus.NO_GO
    live_staging_validation_status: PartnerEvidenceStatus = PartnerEvidenceStatus.PENDING
    external_validation_status: PartnerEvidenceStatus = PartnerEvidenceStatus.PENDING
    compliance_certification_status: PartnerEvidenceStatus = PartnerEvidenceStatus.NOT_CLAIMED
    enforce_mode_enabled: bool = False
    shadow_deny_runtime_enabled: bool = False
    live_blocking_enabled: bool = False
    live_filtering_enabled: bool = False
    application_behavior_changed: bool = False
    production_readiness_claimed: bool = False
    external_validation_claimed: bool = False
    compliance_certification_claimed: bool = False
    schema_version: str = SCHEMA_VERSION
