"""Checklist helpers for Coolify staging evidence.

The helpers return in-memory checklist records only. They do not call Coolify,
open network connections, mutate environment variables, enable feature flags,
or change application behavior.
"""

from __future__ import annotations

from backend.security_layer.staging.models import CoolifyStagingChecklistItem
from backend.security_layer.staging.models import CoolifyStagingEvidenceBundle
from backend.security_layer.staging.models import CoolifyStagingGoNoGoDecision
from backend.security_layer.staging.models import CoolifyStagingStatus


def build_coolify_staging_checklist(
    bundle: CoolifyStagingEvidenceBundle | None = None,
) -> tuple[CoolifyStagingChecklistItem, ...]:
    """Build the default Step 29X staging checklist from sanitized evidence."""

    evidence_bundle = bundle or CoolifyStagingEvidenceBundle()
    return (
        CoolifyStagingChecklistItem(
            item_id="CS-001",
            title="Prerequisite documentation is present",
            status=CoolifyStagingStatus.PASSED,
            evidence_reference="docs/security/evidence/coolify_staging_evidence_bundle/prerequisite_check.txt",
            blocks_go_live=True,
            sanitized_notes="Required Step 29X document and helper paths are enumerated without secrets.",
        ),
        CoolifyStagingChecklistItem(
            item_id="CS-002",
            title="Environment template uses placeholders only",
            status=CoolifyStagingStatus.PASSED,
            evidence_reference="docs/security/coolify_staging_env_template.md",
            blocks_go_live=True,
            sanitized_notes="No real domains, IP addresses, credentials, tokens, private keys, or secrets are stored.",
        ),
        CoolifyStagingChecklistItem(
            item_id="CS-003",
            title="Live Coolify deployment execution",
            status=evidence_bundle.live_deployment_status,
            evidence_reference="docs/security/evidence/coolify_staging_evidence_bundle/live_staging_execution_pending.txt",
            blocks_go_live=True,
            sanitized_notes="Live deployment is pending unless separately executed and evidenced.",
        ),
        CoolifyStagingChecklistItem(
            item_id="CS-004",
            title="Live staging smoke validation",
            status=evidence_bundle.live_validation_status,
            evidence_reference="docs/security/coolify_staging_smoke_test_plan.md",
            blocks_go_live=True,
            sanitized_notes="Smoke validation remains pending until a real staging deployment is available.",
        ),
        CoolifyStagingChecklistItem(
            item_id="CS-005",
            title="Runtime mode safety boundary",
            status=(
                CoolifyStagingStatus.PASSED
                if _bundle_preserves_runtime_boundary(evidence_bundle)
                else CoolifyStagingStatus.BLOCKED
            ),
            evidence_reference="docs/security/coolify_staging_go_no_go.md",
            blocks_go_live=True,
            sanitized_notes="No enforce mode, shadow-deny runtime mode, live blocking, live filtering, or behavior changes are enabled.",
        ),
    )


def evaluate_coolify_staging_go_no_go(
    checklist: tuple[CoolifyStagingChecklistItem, ...],
    bundle: CoolifyStagingEvidenceBundle | None = None,
) -> CoolifyStagingGoNoGoDecision:
    """Evaluate a staging-only go/no-go recommendation."""

    evidence_bundle = bundle or CoolifyStagingEvidenceBundle()
    blocking_item_ids = tuple(
        item.item_id
        for item in checklist
        if item.blocks_go_live and item.status != CoolifyStagingStatus.PASSED
    )
    if blocking_item_ids:
        return CoolifyStagingGoNoGoDecision(
            status=CoolifyStagingStatus.BLOCKED,
            recommendation=(
                "No-go for any live or production claim; complete pending real "
                "Coolify staging deployment and smoke validation first."
            ),
            blocking_item_ids=blocking_item_ids,
            live_staging_validation_status=evidence_bundle.live_validation_status,
        )
    return CoolifyStagingGoNoGoDecision(
        status=CoolifyStagingStatus.PASSED,
        recommendation=(
            "Staging evidence checklist is complete for the supplied evidence; "
            "this is not a production-readiness approval."
        ),
        blocking_item_ids=(),
        live_staging_validation_status=evidence_bundle.live_validation_status,
    )


def _bundle_preserves_runtime_boundary(bundle: CoolifyStagingEvidenceBundle) -> bool:
    return not any(
        (
            bundle.enforce_mode_enabled,
            bundle.shadow_deny_runtime_enabled,
            bundle.live_blocking_enabled,
            bundle.live_filtering_enabled,
            bundle.application_behavior_changed,
            bundle.production_readiness_claimed,
        )
    )
