from __future__ import annotations

import os

from onyx.security_layer.gateway_governance.models import GatewayDataClassification
from onyx.security_layer.gateway_governance.models import GatewayGovernanceConfig
from onyx.security_layer.gateway_governance.models import GatewayGovernanceDecision
from onyx.security_layer.gateway_governance.models import GatewayGovernanceRequest
from onyx.security_layer.gateway_governance.models import GatewayPolicyMode
from onyx.security_layer.gateway_governance.models import GatewayRouteTarget

GATEWAY_GOVERNANCE_ENABLED_ENV = "SECURITY_GATEWAY_GOVERNANCE_ENABLED"
GATEWAY_RESTRICTED_EXTERNAL_MODE_ENV = "SECURITY_GATEWAY_RESTRICTED_EXTERNAL_MODE"
GATEWAY_PII_EXTERNAL_MODE_ENV = "SECURITY_GATEWAY_PII_EXTERNAL_MODE"
GATEWAY_HIGH_RISK_MODE_ENV = "SECURITY_GATEWAY_HIGH_RISK_MODE"


def _enabled_from_env() -> bool:
    return os.getenv(GATEWAY_GOVERNANCE_ENABLED_ENV, "false").lower() == "true"


def _mode_from_env(env_name: str, default: GatewayPolicyMode) -> GatewayPolicyMode:
    value = os.getenv(env_name, default.value).lower()
    try:
        return GatewayPolicyMode(value)
    except ValueError:
        return default


def _high_risk_mode_from_env() -> GatewayGovernanceDecision:
    value = os.getenv(
        GATEWAY_HIGH_RISK_MODE_ENV,
        GatewayGovernanceDecision.APPROVAL_REQUIRED.value,
    ).lower()
    if value == GatewayGovernanceDecision.MONITOR.value:
        return GatewayGovernanceDecision.MONITOR
    return GatewayGovernanceDecision.APPROVAL_REQUIRED


def config_from_env() -> GatewayGovernanceConfig:
    return GatewayGovernanceConfig(
        enabled=_enabled_from_env(),
        restricted_external_mode=_mode_from_env(
            GATEWAY_RESTRICTED_EXTERNAL_MODE_ENV,
            GatewayPolicyMode.DENY,
        ),
        pii_external_mode=_mode_from_env(
            GATEWAY_PII_EXTERNAL_MODE_ENV,
            GatewayPolicyMode.MASK,
        ),
        high_risk_mode=_high_risk_mode_from_env(),
    )


def is_high_risk_gateway_request(request: GatewayGovernanceRequest) -> bool:
    return request.data_classification in {
        GatewayDataClassification.HIGH,
        GatewayDataClassification.RESTRICTED,
    }


def map_restricted_external_mode(
    mode: GatewayPolicyMode,
) -> tuple[GatewayGovernanceDecision, GatewayRouteTarget, str]:
    if mode == GatewayPolicyMode.ROUTE_PRIVATE:
        return (
            GatewayGovernanceDecision.ROUTE_PRIVATE,
            GatewayRouteTarget.PRIVATE,
            "Restricted tenant data routed to private model provider",
        )
    if mode == GatewayPolicyMode.MONITOR:
        return (
            GatewayGovernanceDecision.MONITOR,
            GatewayRouteTarget.MONITOR,
            "Restricted tenant data external route monitored by configuration",
        )
    return (
        GatewayGovernanceDecision.DENY,
        GatewayRouteTarget.BLOCKED,
        "Restricted tenant data external route denied",
    )


def map_pii_external_mode(
    mode: GatewayPolicyMode,
) -> tuple[GatewayGovernanceDecision, GatewayRouteTarget, str]:
    if mode == GatewayPolicyMode.DENY:
        return (
            GatewayGovernanceDecision.DENY,
            GatewayRouteTarget.BLOCKED,
            "PII external route denied",
        )
    if mode == GatewayPolicyMode.MONITOR:
        return (
            GatewayGovernanceDecision.MONITOR,
            GatewayRouteTarget.MONITOR,
            "PII external route monitored by configuration",
        )
    return (
        GatewayGovernanceDecision.MASK,
        GatewayRouteTarget.EXTERNAL,
        "PII external route requires masking before external provider call",
    )


def evaluate_gateway_route_policy(
    request: GatewayGovernanceRequest,
    *,
    config: GatewayGovernanceConfig,
) -> tuple[GatewayGovernanceDecision, GatewayRouteTarget, str]:
    if request.contains_secret:
        return (
            GatewayGovernanceDecision.DENY,
            GatewayRouteTarget.BLOCKED,
            "Secret-bearing request denied before model routing",
        )

    if request.external_provider and request.contains_restricted_tenant_data:
        return map_restricted_external_mode(config.restricted_external_mode)

    if request.external_provider and request.contains_pii:
        return map_pii_external_mode(config.pii_external_mode)

    if is_high_risk_gateway_request(request):
        if config.high_risk_mode == GatewayGovernanceDecision.MONITOR:
            return (
                GatewayGovernanceDecision.MONITOR,
                GatewayRouteTarget.MONITOR,
                "High-risk model request monitored by configuration",
            )
        return (
            GatewayGovernanceDecision.APPROVAL_REQUIRED,
            GatewayRouteTarget.PENDING_APPROVAL,
            "High-risk model request requires approval",
        )

    if request.external_provider:
        return (
            GatewayGovernanceDecision.ROUTE_EXTERNAL,
            GatewayRouteTarget.EXTERNAL,
            "Low-risk clean request allowed for external route",
        )

    return (
        GatewayGovernanceDecision.ALLOW,
        GatewayRouteTarget.PRIVATE,
        "Request allowed for private route",
    )
