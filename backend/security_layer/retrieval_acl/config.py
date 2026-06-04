from __future__ import annotations

import os
from typing import Literal


RetrievalACLIntegrationMode = Literal["off", "shadow", "enforce"]

RETRIEVAL_ACL_MODE_ENV_VAR = "ONYX_SECURITY_RETRIEVAL_ACL_MODE"
DEFAULT_RETRIEVAL_ACL_MODE: RetrievalACLIntegrationMode = "off"
_VALID_RETRIEVAL_ACL_MODES: frozenset[str] = frozenset({"off", "shadow", "enforce"})


def parse_retrieval_acl_mode(raw_value: str | None) -> RetrievalACLIntegrationMode:
    """Parse retrieval ACL integration mode safely.

    Missing, empty, or malformed values default to `off` so Phase 3 cannot
    accidentally claim or activate live enforcement from invalid configuration.
    """

    if raw_value is None:
        return DEFAULT_RETRIEVAL_ACL_MODE

    normalized = raw_value.strip().lower()
    if normalized in _VALID_RETRIEVAL_ACL_MODES:
        return normalized  # type: ignore[return-value]
    return DEFAULT_RETRIEVAL_ACL_MODE


def get_retrieval_acl_mode_from_env() -> RetrievalACLIntegrationMode:
    return parse_retrieval_acl_mode(os.getenv(RETRIEVAL_ACL_MODE_ENV_VAR))
