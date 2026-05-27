from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RetrievalIntegrationMode(str, Enum):
    DISABLED = "disabled"
    MONITOR_ONLY = "monitor_only"
    SHADOW_DENY = "shadow_deny"
    ENFORCE = "enforce"


@dataclass(frozen=True)
class RetrievalIntegrationConfig:
    mode: RetrievalIntegrationMode = RetrievalIntegrationMode.DISABLED


def default_retrieval_integration_config() -> RetrievalIntegrationConfig:
    return RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.DISABLED)


def validate_retrieval_integration_config(config: RetrievalIntegrationConfig) -> RetrievalIntegrationConfig:
    if not isinstance(config.mode, RetrievalIntegrationMode):
        raise ValueError("Invalid retrieval integration mode")
    return config


def is_retrieval_acl_enabled(config: RetrievalIntegrationConfig) -> bool:
    validate_retrieval_integration_config(config)
    return config.mode != RetrievalIntegrationMode.DISABLED


def is_monitor_only(config: RetrievalIntegrationConfig) -> bool:
    validate_retrieval_integration_config(config)
    return config.mode == RetrievalIntegrationMode.MONITOR_ONLY


def is_shadow_deny(config: RetrievalIntegrationConfig) -> bool:
    validate_retrieval_integration_config(config)
    return config.mode == RetrievalIntegrationMode.SHADOW_DENY


def is_enforce_mode(config: RetrievalIntegrationConfig) -> bool:
    validate_retrieval_integration_config(config)
    return config.mode == RetrievalIntegrationMode.ENFORCE
