from __future__ import annotations

from onyx.security_layer.gateway_governance.evidence import (
    build_gateway_governance_evidence,
)
from onyx.security_layer.gateway_governance.models import GatewayGovernanceConfig
from onyx.security_layer.gateway_governance.models import GatewayGovernanceDecision
from onyx.security_layer.gateway_governance.models import GatewayGovernanceEvidence
from onyx.security_layer.gateway_governance.models import GatewayGovernanceRequest
from onyx.security_layer.gateway_governance.models import GatewayGovernanceResult
from onyx.security_layer.gateway_governance.models import GatewayRouteTarget
from onyx.security_layer.gateway_governance.route_policy import config_from_env
from onyx.security_layer.gateway_governance.route_policy import (
    evaluate_gateway_route_policy,
)
from onyx.security_layer.tracing import security_span
from onyx.security_layer.tracing import set_security_span_attributes


def evaluate_gateway_governance(
    request: GatewayGovernanceRequest,
    *,
    config: GatewayGovernanceConfig | None = None,
) -> GatewayGovernanceResult:
    resolved_config = config or config_from_env()
    if not resolved_config.enabled:
        decision = GatewayGovernanceDecision.ALLOW
        route_target = (
            GatewayRouteTarget.EXTERNAL
            if request.external_provider
            else GatewayRouteTarget.PRIVATE
        )
        reason = "Gateway governance disabled; request routing preserved"
    else:
        decision, route_target, reason = evaluate_gateway_route_policy(
            request,
            config=resolved_config,
        )
    evidence = GatewayGovernanceEvidence(
        model_provider=request.model_provider,
        requested_model=request.requested_model,
        data_classification=request.data_classification,
        decision=decision,
        route_target=route_target,
        contains_pii=request.contains_pii,
        contains_secret=request.contains_secret,
        restricted_data=request.contains_restricted_tenant_data,
        correlation_id=request.correlation_id,
    )
    safe_evidence = build_gateway_governance_evidence(evidence)

    with security_span(
        "security.gateway_governance.decision",
        {
            "security.correlation_id": request.correlation_id,
            "security.model_provider": request.model_provider,
            "security.requested_model": request.requested_model,
            "security.data_classification": request.data_classification.value,
            "security.decision": decision.value,
            "security.route_target": route_target.value,
        },
    ) as span:
        set_security_span_attributes(
            span,
            {
                "security.contains_pii": request.contains_pii,
                "security.contains_secret": request.contains_secret,
                "security.restricted_data": request.contains_restricted_tenant_data,
                "security.reason": reason,
                "security.evidence_fields": ",".join(sorted(safe_evidence)),
            },
        )

    return GatewayGovernanceResult(
        request=request,
        decision=decision,
        route_target=route_target,
        reason=reason,
        evidence=evidence,
    )
