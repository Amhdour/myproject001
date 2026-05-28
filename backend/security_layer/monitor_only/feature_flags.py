from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from os import getenv


class MonitorOnlyRuntimeMode(str, Enum):
    DISABLED = "disabled"
    MONITOR_ONLY = "monitor_only"


@dataclass(frozen=True)
class MonitorOnlyFeatureFlags:
    runtime_mode: MonitorOnlyRuntimeMode = MonitorOnlyRuntimeMode.DISABLED
    shared_sink_enabled: bool = False
    cache_adapter_enabled: bool = False


IMPLEMENTED_MONITOR_ONLY_FEATURE_FLAG_COUNT = 3


def default_monitor_only_feature_flags() -> MonitorOnlyFeatureFlags:
    return MonitorOnlyFeatureFlags()


def validate_monitor_only_feature_flags(flags: MonitorOnlyFeatureFlags) -> MonitorOnlyFeatureFlags:
    if not isinstance(flags.runtime_mode, MonitorOnlyRuntimeMode):
        raise ValueError("Invalid monitor-only runtime mode")
    if flags.runtime_mode is MonitorOnlyRuntimeMode.DISABLED and (flags.shared_sink_enabled or flags.cache_adapter_enabled):
        raise ValueError("Monitor-only helpers must remain disabled when runtime mode is disabled")
    return flags


def is_monitor_only_runtime_enabled(flags: MonitorOnlyFeatureFlags) -> bool:
    validate_monitor_only_feature_flags(flags)
    return flags.runtime_mode is MonitorOnlyRuntimeMode.MONITOR_ONLY


def is_shared_sink_enabled(flags: MonitorOnlyFeatureFlags) -> bool:
    validate_monitor_only_feature_flags(flags)
    return is_monitor_only_runtime_enabled(flags) and flags.shared_sink_enabled


def is_cache_adapter_enabled(flags: MonitorOnlyFeatureFlags) -> bool:
    validate_monitor_only_feature_flags(flags)
    return is_monitor_only_runtime_enabled(flags) and flags.cache_adapter_enabled


def _env_flag(name: str) -> bool:
    return getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def monitor_only_feature_flags_from_env() -> MonitorOnlyFeatureFlags:
    runtime_mode = (
        MonitorOnlyRuntimeMode.MONITOR_ONLY
        if _env_flag("SECURITY_LAYER_MONITOR_ONLY_ENABLED")
        else MonitorOnlyRuntimeMode.DISABLED
    )
    if runtime_mode is MonitorOnlyRuntimeMode.DISABLED:
        return MonitorOnlyFeatureFlags()
    return MonitorOnlyFeatureFlags(
        runtime_mode=runtime_mode,
        shared_sink_enabled=_env_flag("SECURITY_LAYER_MONITOR_ONLY_SHARED_SINK_ENABLED"),
        cache_adapter_enabled=_env_flag("SECURITY_LAYER_MONITOR_ONLY_CACHE_ADAPTER_ENABLED"),
    )
