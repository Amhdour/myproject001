from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum


class RuntimeEnforcementMode(str, Enum):
    DISABLED = "disabled"
    MONITOR_ONLY = "monitor_only"
    ENFORCE = "enforce"


@dataclass(frozen=True)
class RuntimeEnforcementConfig:
    mode: RuntimeEnforcementMode = RuntimeEnforcementMode.DISABLED


def parse_runtime_enforcement_mode(raw_mode: str | None) -> RuntimeEnforcementMode:
    if raw_mode is None or raw_mode == "":
        return RuntimeEnforcementMode.DISABLED
    normalized = raw_mode.strip().lower()
    try:
        return RuntimeEnforcementMode(normalized)
    except ValueError as exc:
        valid_modes = ", ".join(mode.value for mode in RuntimeEnforcementMode)
        raise ValueError(f"Invalid Step 39X runtime enforcement mode: {normalized}. Expected one of: {valid_modes}") from exc


def get_runtime_enforcement_config() -> RuntimeEnforcementConfig:
    return RuntimeEnforcementConfig(
        mode=parse_runtime_enforcement_mode(os.getenv("STEP_39X_RUNTIME_ENFORCEMENT_MODE"))
    )
