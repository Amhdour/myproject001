"""Blast-radius validation for isolated enforce-mode simulations."""

from __future__ import annotations

from collections.abc import Iterable

from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceReadinessStage

MAX_TENANTS = 1
MAX_WORKSPACES = 1
MAX_SUBJECTS = 5
MAX_CONTROL_FAMILIES = 1
MAX_STAGES = 1
MAX_DENY_RATE = 0.01
MAX_FALSE_POSITIVE_RATE = 0.001
MAX_ERROR_RATE = 0.005
MAX_LATENCY_MS = 50.0


def _safe_count(values: Iterable[str]) -> int:
    return len(tuple(values))


def validate_tenant_allowlist(tenant_safe_ids: Iterable[str]) -> bool:
    count = _safe_count(tenant_safe_ids)
    return 0 <= count <= MAX_TENANTS


def validate_workspace_allowlist(workspace_safe_ids: Iterable[str]) -> bool:
    count = _safe_count(workspace_safe_ids)
    return 0 <= count <= MAX_WORKSPACES


def validate_subject_allowlist(subject_safe_ids: Iterable[str]) -> bool:
    count = _safe_count(subject_safe_ids)
    return 0 <= count <= MAX_SUBJECTS


def validate_control_family_allowlist(
    control_families: Iterable[EnforceControlFamily],
) -> bool:
    count = _safe_count(family.value for family in control_families)
    return 0 <= count <= MAX_CONTROL_FAMILIES


def validate_stage_allowlist(stages: Iterable[EnforceReadinessStage]) -> bool:
    count = _safe_count(stage.value for stage in stages)
    return 0 <= count <= MAX_STAGES


def validate_deny_rate_threshold(deny_rate: float) -> bool:
    return 0.0 <= deny_rate <= MAX_DENY_RATE


def validate_false_positive_threshold(false_positive_rate: float) -> bool:
    return 0.0 <= false_positive_rate <= MAX_FALSE_POSITIVE_RATE


def validate_error_rate_threshold(error_rate: float) -> bool:
    return 0.0 <= error_rate <= MAX_ERROR_RATE


def validate_latency_threshold(latency_added_ms: float) -> bool:
    return 0.0 <= latency_added_ms <= MAX_LATENCY_MS


def validate_blast_radius_scope(
    *,
    tenant_safe_ids: Iterable[str] = (),
    workspace_safe_ids: Iterable[str] = (),
    subject_safe_ids: Iterable[str] = (),
    control_families: Iterable[EnforceControlFamily] = (),
    stages: Iterable[EnforceReadinessStage] = (),
) -> EnforceBlastRadiusStatus:
    tenant_count = _safe_count(tenant_safe_ids)
    workspace_count = _safe_count(workspace_safe_ids)
    subject_count = _safe_count(subject_safe_ids)
    family_count = _safe_count(family.value for family in control_families)
    stage_count = _safe_count(stage.value for stage in stages)
    if (
        tenant_count
        == workspace_count
        == subject_count
        == family_count
        == stage_count
        == 0
    ):
        return EnforceBlastRadiusStatus.NONE_ALLOWED
    if (
        tenant_count <= MAX_TENANTS
        and workspace_count <= MAX_WORKSPACES
        and subject_count <= MAX_SUBJECTS
        and family_count <= MAX_CONTROL_FAMILIES
        and stage_count <= MAX_STAGES
    ):
        return EnforceBlastRadiusStatus.LIMITED
    return EnforceBlastRadiusStatus.TOO_BROAD


def evaluate_automatic_rollback_conditions(
    *,
    deny_rate: float,
    false_positive_rate: float,
    error_rate: float,
    latency_added_ms: float,
) -> bool:
    return not (
        validate_deny_rate_threshold(deny_rate)
        and validate_false_positive_threshold(false_positive_rate)
        and validate_error_rate_threshold(error_rate)
        and validate_latency_threshold(latency_added_ms)
    )


def sanitize_blast_radius_summary(status: EnforceBlastRadiusStatus) -> str:
    if status == EnforceBlastRadiusStatus.NONE_ALLOWED:
        return "no tenants, workspaces, subjects, stages, or control families allowed"
    if status == EnforceBlastRadiusStatus.LIMITED:
        return "limited placeholder-scope pilot only"
    if status == EnforceBlastRadiusStatus.THRESHOLD_BREACHED:
        return "threshold breached; simulated activation blocked"
    return "scope too broad; simulated activation blocked"
