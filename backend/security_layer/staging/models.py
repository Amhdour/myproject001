"""Models for isolated Coolify staging evidence.

The schema intentionally uses safe placeholders and sanitized summaries only. It
must not contain real domains, IP addresses, credentials, tokens, private keys,
or secret values.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

SCHEMA_VERSION = "coolify-staging-evidence.v1"


class CoolifyStagingStatus(StrEnum):
    """Allowed statuses for staging evidence and checklist records."""

    NOT_STARTED = "not_started"
    PENDING = "pending"
    PASSED = "passed"
    BLOCKED = "blocked"


class CoolifyStagingMode(StrEnum):
    """Runtime mode boundary for the staging evidence bundle."""

    DOCUMENTATION_ONLY = "documentation_only"
    ISOLATED_HELPER_ONLY = "isolated_helper_only"


@dataclass(frozen=True)
class CoolifyStagingEvidenceBundle:
    """Sanitized evidence metadata for a Coolify staging validation bundle."""

    bundle_id: str = "coolify_staging_evidence_bundle"
    branch_name: str = "coolify-staging-evidence-bundle"
    mode: CoolifyStagingMode = CoolifyStagingMode.ISOLATED_HELPER_ONLY
    live_deployment_status: CoolifyStagingStatus = CoolifyStagingStatus.PENDING
    live_validation_status: CoolifyStagingStatus = CoolifyStagingStatus.PENDING
    enforce_mode_enabled: bool = False
    shadow_deny_runtime_enabled: bool = False
    live_blocking_enabled: bool = False
    live_filtering_enabled: bool = False
    application_behavior_changed: bool = False
    production_readiness_claimed: bool = False
    sanitized_summary: str = (
        "Coolify staging evidence bundle prepared with placeholders only; live "
        "deployment and validation remain pending until separately executed."
    )
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class CoolifyStagingChecklistItem:
    """Single sanitized checklist item for staging review."""

    item_id: str
    title: str
    status: CoolifyStagingStatus
    evidence_reference: str
    blocks_go_live: bool
    sanitized_notes: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class CoolifyStagingGoNoGoDecision:
    """Go/no-go output for staging-only review.

    This decision is for staging evidence review only and is not a production
    launch approval.
    """

    status: CoolifyStagingStatus
    recommendation: str
    blocking_item_ids: tuple[str, ...]
    live_staging_validation_status: CoolifyStagingStatus
    production_readiness_claimed: bool = False
    schema_version: str = SCHEMA_VERSION
