"""Isolated helpers for Step 32X real Coolify staging execution evidence.

The helpers produce sanitized in-memory execution metadata only. They do not
call Coolify, open network connections, read or write secrets, mutate feature
flags, enable runtime enforcement, block/filter traffic, or change application
behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

SCHEMA_VERSION = "real-coolify-staging-execution.v1"


class RealCoolifyExecutionDecision(StrEnum):
    """Allowed Step 32X decision values."""

    GO = "GO"
    NO_GO = "NO-GO"


class RealCoolifyExecutionStatus(StrEnum):
    """Allowed Step 32X execution and validation statuses."""

    PENDING = "PENDING"
    PASSED = "PASSED"
    NOT_CLAIMED = "NOT CLAIMED"
    CONFIRMED = "CONFIRMED"


class RealCoolifyExecutionMode(StrEnum):
    """Boundary modes for the Step 32X helper bundle."""

    DOCUMENTATION_ONLY = "documentation_only"
    ISOLATED_HELPER_ONLY = "isolated_helper_only"


@dataclass(frozen=True)
class RealCoolifyStagingExecutionBundle:
    """Sanitized Step 32X execution metadata.

    Defaults intentionally represent the current repository-only state: no real
    Coolify deployment has been performed and live validation remains pending.
    """

    bundle_id: str = "real_coolify_staging_execution_bundle"
    branch_name: str = "real-coolify-staging-execution-bundle"
    mode: RealCoolifyExecutionMode = RealCoolifyExecutionMode.ISOLATED_HELPER_ONLY
    real_coolify_deployment_executed: bool = False
    live_staging_validation_status: RealCoolifyExecutionStatus = (
        RealCoolifyExecutionStatus.PENDING
    )
    partner_demo_evidence_review_decision: RealCoolifyExecutionDecision = (
        RealCoolifyExecutionDecision.GO
    )
    production_readiness_decision: RealCoolifyExecutionDecision = (
        RealCoolifyExecutionDecision.NO_GO
    )
    enterprise_production_readiness_decision: RealCoolifyExecutionDecision = (
        RealCoolifyExecutionDecision.NO_GO
    )
    external_validation_status: RealCoolifyExecutionStatus = (
        RealCoolifyExecutionStatus.PENDING
    )
    compliance_certification_status: RealCoolifyExecutionStatus = (
        RealCoolifyExecutionStatus.NOT_CLAIMED
    )
    enforce_mode_enabled: bool = False
    shadow_deny_runtime_enabled: bool = False
    live_blocking_enabled: bool = False
    live_filtering_enabled: bool = False
    application_behavior_changed: bool = False
    production_readiness_claimed: bool = False
    enterprise_production_readiness_claimed: bool = False
    external_validation_claimed: bool = False
    compliance_certification_claimed: bool = False
    sanitized_summary: str = (
        "Step 32X execution bundle prepared with sanitized placeholders only; "
        "real Coolify deployment and live staging validation remain pending."
    )
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class RealCoolifyExecutionChecklistItem:
    """Single sanitized Step 32X execution checklist item."""

    item_id: str
    title: str
    status: RealCoolifyExecutionStatus
    evidence_reference: str
    blocks_production_claim: bool
    sanitized_notes: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class RealCoolifyExecutionOutcome:
    """Evaluated Step 32X outcome and safety confirmations."""

    partner_demo_evidence_review_decision: RealCoolifyExecutionDecision
    production_readiness_decision: RealCoolifyExecutionDecision
    enterprise_production_readiness_decision: RealCoolifyExecutionDecision
    real_coolify_deployment_executed: bool
    live_staging_validation_status: RealCoolifyExecutionStatus
    external_validation_status: RealCoolifyExecutionStatus
    compliance_certification_status: RealCoolifyExecutionStatus
    runtime_boundary_confirmed: bool
    blocking_item_ids: tuple[str, ...]
    final_recommendation: str
    schema_version: str = SCHEMA_VERSION


def build_real_coolify_execution_checklist(
    bundle: RealCoolifyStagingExecutionBundle | None = None,
) -> tuple[RealCoolifyExecutionChecklistItem, ...]:
    """Build the Step 32X checklist from sanitized execution metadata."""

    execution_bundle = bundle or RealCoolifyStagingExecutionBundle()
    return (
        RealCoolifyExecutionChecklistItem(
            item_id="RCSE-001",
            title="Prerequisite Step 32X documentation and evidence paths exist",
            status=RealCoolifyExecutionStatus.CONFIRMED,
            evidence_reference="docs/security/evidence/real_coolify_staging_execution_bundle/prerequisite_check.txt",
            blocks_production_claim=False,
            sanitized_notes="Repository prerequisites are verified without storing secrets or real endpoints.",
        ),
        RealCoolifyExecutionChecklistItem(
            item_id="RCSE-002",
            title="Operator runbook and evidence capture template are prepared",
            status=RealCoolifyExecutionStatus.CONFIRMED,
            evidence_reference="docs/security/evidence/real_coolify_staging_execution_bundle/operator_runbook_summary.md",
            blocks_production_claim=False,
            sanitized_notes="Operator instructions require out-of-band secrets and sanitized evidence only.",
        ),
        RealCoolifyExecutionChecklistItem(
            item_id="RCSE-003",
            title="Real Coolify deployment execution is evidenced",
            status=(
                RealCoolifyExecutionStatus.CONFIRMED
                if execution_bundle.real_coolify_deployment_executed
                else RealCoolifyExecutionStatus.PENDING
            ),
            evidence_reference="docs/security/evidence/real_coolify_staging_execution_bundle/live_execution_status.txt",
            blocks_production_claim=True,
            sanitized_notes="No deployment is claimed unless sanitized operator evidence confirms execution.",
        ),
        RealCoolifyExecutionChecklistItem(
            item_id="RCSE-004",
            title="Live staging smoke validation is evidenced",
            status=execution_bundle.live_staging_validation_status,
            evidence_reference="docs/security/evidence/real_coolify_staging_execution_bundle/smoke_validation_summary.md",
            blocks_production_claim=True,
            sanitized_notes="Live staging validation remains pending until sanitized smoke evidence is captured.",
        ),
        RealCoolifyExecutionChecklistItem(
            item_id="RCSE-005",
            title="Runtime and claim boundaries remain safe",
            status=(
                RealCoolifyExecutionStatus.CONFIRMED
                if real_coolify_execution_runtime_boundary_confirmed(execution_bundle)
                else RealCoolifyExecutionStatus.PENDING
            ),
            evidence_reference="docs/security/evidence/real_coolify_staging_execution_bundle/go_no_go_summary.md",
            blocks_production_claim=True,
            sanitized_notes="No enforce mode, shadow-deny runtime mode, live blocking/filtering, behavior change, production-readiness claim, external validation claim, or certification claim is enabled.",
        ),
    )


def evaluate_real_coolify_execution(
    checklist: tuple[RealCoolifyExecutionChecklistItem, ...],
    bundle: RealCoolifyStagingExecutionBundle | None = None,
) -> RealCoolifyExecutionOutcome:
    """Evaluate Step 32X decisions while preserving no-production boundaries."""

    execution_bundle = bundle or RealCoolifyStagingExecutionBundle()
    blocking_item_ids = tuple(
        item.item_id
        for item in checklist
        if item.blocks_production_claim
        and item.status != RealCoolifyExecutionStatus.CONFIRMED
        and item.status != RealCoolifyExecutionStatus.PASSED
    )
    runtime_boundary_confirmed = real_coolify_execution_runtime_boundary_confirmed(
        execution_bundle
    )
    return RealCoolifyExecutionOutcome(
        partner_demo_evidence_review_decision=RealCoolifyExecutionDecision.GO,
        production_readiness_decision=RealCoolifyExecutionDecision.NO_GO,
        enterprise_production_readiness_decision=RealCoolifyExecutionDecision.NO_GO,
        real_coolify_deployment_executed=execution_bundle.real_coolify_deployment_executed,
        live_staging_validation_status=execution_bundle.live_staging_validation_status,
        external_validation_status=execution_bundle.external_validation_status,
        compliance_certification_status=execution_bundle.compliance_certification_status,
        runtime_boundary_confirmed=runtime_boundary_confirmed,
        blocking_item_ids=blocking_item_ids,
        final_recommendation=(
            "Proceed with partner-demo evidence review only. Keep production and "
            "enterprise production readiness at NO-GO until real staging, "
            "external validation, compliance, and residual-risk evidence are "
            "completed and separately approved."
        ),
    )


def real_coolify_execution_runtime_boundary_confirmed(
    bundle: RealCoolifyStagingExecutionBundle,
) -> bool:
    """Return whether the Step 32X bundle preserves no-live-change boundaries."""

    return not any(
        (
            bundle.enforce_mode_enabled,
            bundle.shadow_deny_runtime_enabled,
            bundle.live_blocking_enabled,
            bundle.live_filtering_enabled,
            bundle.application_behavior_changed,
            bundle.production_readiness_claimed,
            bundle.enterprise_production_readiness_claimed,
            bundle.external_validation_claimed,
            bundle.compliance_certification_claimed,
        )
    )
