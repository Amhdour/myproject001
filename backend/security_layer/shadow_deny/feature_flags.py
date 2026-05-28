from backend.security_layer.shadow_deny.models import ShadowDenyControlFamily

SHADOW_DENY_FLAGS = (
    "SECURITY_SHADOW_DENY_ENABLED",
    "RETRIEVAL_SHADOW_DENY_ENABLED",
    "VECTOR_SHADOW_DENY_ENABLED",
    "CACHE_SHADOW_DENY_ENABLED",
    "TOOL_SHADOW_DENY_ENABLED",
    "MCP_SHADOW_DENY_ENABLED",
    "ARTIFACT_SHADOW_DENY_ENABLED",
    "INGESTION_SHADOW_DENY_ENABLED",
    "SHADOW_DENY_DECISION_RECORDING_ENABLED",
    "SHADOW_DENY_COMPARE_MONITOR_ONLY_ENABLED",
    "SHADOW_DENY_FAIL_OPEN_ENABLED",
    "SHADOW_DENY_ROLLBACK_ENABLED",
)
DEFAULT_SHADOW_DENY_FLAG_STATE = {k: False for k in SHADOW_DENY_FLAGS}


FAMILY_FLAG = {
    ShadowDenyControlFamily.RETRIEVAL: "RETRIEVAL_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.VECTOR: "VECTOR_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.CACHE: "CACHE_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.TOOL: "TOOL_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.MCP: "MCP_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.ARTIFACT: "ARTIFACT_SHADOW_DENY_ENABLED",
    ShadowDenyControlFamily.INGESTION: "INGESTION_SHADOW_DENY_ENABLED",
}


def validate_shadow_deny_flags(flags: dict[str, bool]) -> dict[str, bool]:
    out = DEFAULT_SHADOW_DENY_FLAG_STATE.copy()
    for k, v in flags.items():
        if k not in SHADOW_DENY_FLAGS or not isinstance(v, bool):
            raise ValueError(f"Invalid shadow deny flag: {k}")
        out[k] = v
    return out


def build_shadow_deny_flag_state(flags: dict[str, bool] | None = None) -> dict[str, bool]:
    built = validate_shadow_deny_flags(flags or {})
    if built["SHADOW_DENY_ROLLBACK_ENABLED"]:
        built["SHADOW_DENY_DECISION_RECORDING_ENABLED"] = False
    return built


def shadow_deny_globally_enabled(flags: dict[str, bool]) -> bool:
    return bool(flags.get("SECURITY_SHADOW_DENY_ENABLED", False))


def shadow_deny_family_enabled(flags: dict[str, bool], control_family: ShadowDenyControlFamily) -> bool:
    return shadow_deny_globally_enabled(flags) and bool(flags.get(FAMILY_FLAG.get(control_family, ""), False))


def shadow_deny_decision_recording_enabled(flags: dict[str, bool]) -> bool:
    return bool(flags.get("SHADOW_DENY_DECISION_RECORDING_ENABLED", False)) and not shadow_deny_rollback_enabled(flags)


def shadow_deny_compare_monitor_only_enabled(flags: dict[str, bool]) -> bool:
    return bool(flags.get("SHADOW_DENY_COMPARE_MONITOR_ONLY_ENABLED", False))


def shadow_deny_fail_open_enabled(flags: dict[str, bool]) -> bool:
    return bool(flags.get("SHADOW_DENY_FAIL_OPEN_ENABLED", False))


def shadow_deny_rollback_enabled(flags: dict[str, bool]) -> bool:
    return bool(flags.get("SHADOW_DENY_ROLLBACK_ENABLED", False))
