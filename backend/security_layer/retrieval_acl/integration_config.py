from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal


RetrievalACLIntegrationMode = Literal["off", "shadow", "enforce"]

INTEGRATION_MODE_ENV_VAR = "ONYX_SECURITY_RETRIEVAL_ACL_MODE"
SUPPORTED_INTEGRATION_MODES: frozenset[str] = frozenset({"off", "shadow", "enforce"})


@dataclass(frozen=True)
class RetrievalACLIntegrationConfig:
    """Off-by-default integration config for Phase 3 retrieval ACL proof."""

    mode: RetrievalACLIntegrationMode
    env_var_name: str = INTEGRATION_MODE_ENV_VAR
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False

    @property
    def is_off(self) -> bool:
        return self.mode == "off"

    @property
    def is_shadow(self) -> bool:
        return self.mode == "shadow"

    @property
    def is_enforce(self) -> bool:
        return self.mode == "enforce"


def parse_retrieval_acl_integration_mode(raw_value: str | None) -> RetrievalACLIntegrationMode:
    """Parse the retrieval ACL integration mode with safe default-off behavior."""

    if raw_value is None:
        return "off"

    normalized = raw_value.strip().lower()
    if normalized in SUPPORTED_INTEGRATION_MODES:
        return normalized  # type: ignore[return-value]

    return "off"


def get_retrieval_acl_integration_config(
    env: dict[str, str] | None = None,
) -> RetrievalACLIntegrationConfig:
    """Read the off-by-default retrieval ACL integration config.

    This helper is intentionally small and testable. It does not wire live Onyx
    retrieval behavior by itself.
    """

    source = os.environ if env is None else env
    return RetrievalACLIntegrationConfig(
        mode=parse_retrieval_acl_integration_mode(source.get(INTEGRATION_MODE_ENV_VAR))
    )
