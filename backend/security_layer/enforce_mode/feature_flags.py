"""Default-disabled enforce-mode feature flag helpers.

These helpers are isolated from runtime configuration and cannot enable live
blocking, live filtering, or shadow-deny runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping

from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState

SECURITY_ENFORCE_MODE_ENABLED = "SECURITY_ENFORCE_MODE_ENABLED"
RETRIEVAL_ENFORCE_ENABLED = "RETRIEVAL_ENFORCE_ENABLED"
VECTOR_ENFORCE_ENABLED = "VECTOR_ENFORCE_ENABLED"
CACHE_ENFORCE_ENABLED = "CACHE_ENFORCE_ENABLED"
TOOL_ENFORCE_ENABLED = "TOOL_ENFORCE_ENABLED"
MCP_ENFORCE_ENABLED = "MCP_ENFORCE_ENABLED"
ARTIFACT_ENFORCE_ENABLED = "ARTIFACT_ENFORCE_ENABLED"
INGESTION_ENFORCE_ENABLED = "INGESTION_ENFORCE_ENABLED"
ENFORCE_APPROVAL_GATE_ENABLED = "ENFORCE_APPROVAL_GATE_ENABLED"
ENFORCE_ROLLBACK_ENABLED = "ENFORCE_ROLLBACK_ENABLED"
ENFORCE_KILL_SWITCH_ENABLED = "ENFORCE_KILL_SWITCH_ENABLED"
ENFORCE_BLAST_RADIUS_LIMIT_ENABLED = "ENFORCE_BLAST_RADIUS_LIMIT_ENABLED"
ENFORCE_SAFE_DENIAL_REQUIRED = "ENFORCE_SAFE_DENIAL_REQUIRED"
ENFORCE_TELEMETRY_REQUIRED = "ENFORCE_TELEMETRY_REQUIRED"

ENFORCE_MODE_FLAGS: tuple[str, ...] = (
    SECURITY_ENFORCE_MODE_ENABLED,
    RETRIEVAL_ENFORCE_ENABLED,
    VECTOR_ENFORCE_ENABLED,
    CACHE_ENFORCE_ENABLED,
    TOOL_ENFORCE_ENABLED,
    MCP_ENFORCE_ENABLED,
    ARTIFACT_ENFORCE_ENABLED,
    INGESTION_ENFORCE_ENABLED,
    ENFORCE_APPROVAL_GATE_ENABLED,
    ENFORCE_ROLLBACK_ENABLED,
    ENFORCE_KILL_SWITCH_ENABLED,
    ENFORCE_BLAST_RADIUS_LIMIT_ENABLED,
    ENFORCE_SAFE_DENIAL_REQUIRED,
    ENFORCE_TELEMETRY_REQUIRED,
)

DEFAULT_ENFORCE_FLAG_STATE: dict[str, EnforceFeatureFlagState] = {
    flag: EnforceFeatureFlagState.DISABLED for flag in ENFORCE_MODE_FLAGS
}

_FAMILY_FLAG: dict[EnforceControlFamily, str] = {
    EnforceControlFamily.RETRIEVAL_ACL: RETRIEVAL_ENFORCE_ENABLED,
    EnforceControlFamily.VECTOR_DB_SECURITY: VECTOR_ENFORCE_ENABLED,
    EnforceControlFamily.CACHE_SECURITY: CACHE_ENFORCE_ENABLED,
    EnforceControlFamily.TOOL_AUTHORIZATION: TOOL_ENFORCE_ENABLED,
    EnforceControlFamily.MCP_HARDENING: MCP_ENFORCE_ENABLED,
    EnforceControlFamily.ARTIFACT_SAFETY: ARTIFACT_ENFORCE_ENABLED,
    EnforceControlFamily.SECURE_INGESTION: INGESTION_ENFORCE_ENABLED,
    EnforceControlFamily.SAFE_DENIAL: ENFORCE_SAFE_DENIAL_REQUIRED,
    EnforceControlFamily.AUDIT_FINDING_METRIC: ENFORCE_TELEMETRY_REQUIRED,
}


def _normalize_flag_state(
    value: EnforceFeatureFlagState | str,
) -> EnforceFeatureFlagState:
    if isinstance(value, EnforceFeatureFlagState):
        return value
    if value in {state.value for state in EnforceFeatureFlagState}:
        return EnforceFeatureFlagState(value)
    raise ValueError("invalid enforce-mode feature flag value")


def build_enforce_flag_state(
    overrides: Mapping[str, EnforceFeatureFlagState | str] | None = None,
) -> dict[str, EnforceFeatureFlagState]:
    flags = dict(DEFAULT_ENFORCE_FLAG_STATE)
    if overrides is None:
        return flags
    for flag, value in overrides.items():
        if flag not in ENFORCE_MODE_FLAGS:
            raise ValueError("unknown enforce-mode feature flag")
        flags[flag] = _normalize_flag_state(value)
    validate_enforce_flags(flags)
    return flags


def validate_enforce_flags(flags: Mapping[str, EnforceFeatureFlagState | str]) -> bool:
    for required_flag in ENFORCE_MODE_FLAGS:
        if required_flag not in flags:
            raise ValueError("missing enforce-mode feature flag")
    for flag, value in flags.items():
        if flag not in ENFORCE_MODE_FLAGS:
            raise ValueError("unknown enforce-mode feature flag")
        _normalize_flag_state(value)
    return True


def _enabled(flags: Mapping[str, EnforceFeatureFlagState | str], flag: str) -> bool:
    validate_enforce_flags(flags)
    return _normalize_flag_state(flags[flag]) == EnforceFeatureFlagState.ENABLED


def enforce_globally_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, SECURITY_ENFORCE_MODE_ENABLED)


def enforce_family_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
    control_family: EnforceControlFamily,
) -> bool:
    return enforce_globally_enabled(flags) and _enabled(
        flags, _FAMILY_FLAG[control_family]
    )


def enforce_approval_gate_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_APPROVAL_GATE_ENABLED)


def enforce_rollback_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_ROLLBACK_ENABLED)


def enforce_kill_switch_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_KILL_SWITCH_ENABLED)


def enforce_blast_radius_enabled(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_BLAST_RADIUS_LIMIT_ENABLED)


def enforce_safe_denial_required(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_SAFE_DENIAL_REQUIRED)


def enforce_telemetry_required(
    flags: Mapping[str, EnforceFeatureFlagState | str],
) -> bool:
    return _enabled(flags, ENFORCE_TELEMETRY_REQUIRED)
