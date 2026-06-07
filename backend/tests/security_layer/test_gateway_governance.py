from __future__ import annotations

import onyx.security_layer.gateway_governance.decision_mapper as decision_mapper
from onyx.security_layer.gateway_governance import evaluate_gateway_governance
from onyx.security_layer.gateway_governance import GatewayDataClassification
from onyx.security_layer.gateway_governance import GatewayGovernanceConfig
from onyx.security_layer.gateway_governance import GatewayGovernanceDecision
from onyx.security_layer.gateway_governance import GatewayGovernanceRequest
from onyx.security_layer.gateway_governance import GatewayPolicyMode
from onyx.security_layer.gateway_governance import GatewayRouteTarget
from onyx.security_layer.gateway_governance.evidence import (
    safe_gateway_governance_evidence_payload,
)


class RecordingSpan:
    def __init__(self) -> None:
        self.attributes: dict[str, str | bool | int | float] = {}

    def set_attribute(self, key: str, value: str | bool | int | float) -> None:
        self.attributes[key] = value


class RecordingSecuritySpan:
    def __init__(self) -> None:
        self.name: str | None = None
        self.attributes: dict[str, object | None] = {}
        self.span = RecordingSpan()

    def __call__(self, name: str, attributes: dict[str, object | None]):
        self.name = name
        self.attributes = attributes
        return self

    def __enter__(self) -> RecordingSpan:
        return self.span

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None


def _config(**overrides: object) -> GatewayGovernanceConfig:
    payload = {"enabled": True}
    payload.update(overrides)
    return GatewayGovernanceConfig(**payload)


def _request(**overrides: object) -> GatewayGovernanceRequest:
    payload = {
        "user_id": "user-1",
        "tenant_id": "tenant-a",
        "model_provider": "openai",
        "requested_model": "gpt-example",
        "data_classification": GatewayDataClassification.LOW,
        "contains_pii": False,
        "contains_secret": False,
        "contains_restricted_tenant_data": False,
        "external_provider": True,
        "correlation_id": "corr-gateway-test",
    }
    payload.update(overrides)
    return GatewayGovernanceRequest(**payload)


def test_clean_low_risk_external_request_allowed(monkeypatch) -> None:
    recording_security_span = RecordingSecuritySpan()
    monkeypatch.setattr(decision_mapper, "security_span", recording_security_span)

    result = evaluate_gateway_governance(_request(), config=_config())

    assert result.decision == GatewayGovernanceDecision.ROUTE_EXTERNAL
    assert result.route_target == GatewayRouteTarget.EXTERNAL
    assert recording_security_span.name == "security.gateway_governance.decision"
    assert recording_security_span.attributes["security.decision"] == "route_external"


def test_pii_external_request_masked_or_denied_by_config() -> None:
    masked = evaluate_gateway_governance(
        _request(contains_pii=True),
        config=_config(pii_external_mode=GatewayPolicyMode.MASK),
    )
    denied = evaluate_gateway_governance(
        _request(contains_pii=True),
        config=_config(pii_external_mode=GatewayPolicyMode.DENY),
    )

    assert masked.decision == GatewayGovernanceDecision.MASK
    assert masked.route_target == GatewayRouteTarget.EXTERNAL
    assert denied.decision == GatewayGovernanceDecision.DENY
    assert denied.route_target == GatewayRouteTarget.BLOCKED


def test_secret_external_request_denied() -> None:
    result = evaluate_gateway_governance(
        _request(contains_secret=True),
        config=_config(),
    )

    assert result.decision == GatewayGovernanceDecision.DENY
    assert result.route_target == GatewayRouteTarget.BLOCKED


def test_restricted_tenant_data_external_request_route_private_or_denied() -> None:
    private = evaluate_gateway_governance(
        _request(contains_restricted_tenant_data=True),
        config=_config(restricted_external_mode=GatewayPolicyMode.ROUTE_PRIVATE),
    )
    denied = evaluate_gateway_governance(
        _request(contains_restricted_tenant_data=True),
        config=_config(restricted_external_mode=GatewayPolicyMode.DENY),
    )

    assert private.decision == GatewayGovernanceDecision.ROUTE_PRIVATE
    assert private.route_target == GatewayRouteTarget.PRIVATE
    assert denied.decision == GatewayGovernanceDecision.DENY
    assert denied.route_target == GatewayRouteTarget.BLOCKED


def test_high_risk_request_requires_approval_or_monitor_by_config() -> None:
    approval = evaluate_gateway_governance(
        _request(data_classification=GatewayDataClassification.HIGH),
        config=_config(high_risk_mode=GatewayGovernanceDecision.APPROVAL_REQUIRED),
    )
    monitor = evaluate_gateway_governance(
        _request(data_classification=GatewayDataClassification.HIGH),
        config=_config(high_risk_mode=GatewayGovernanceDecision.MONITOR),
    )

    assert approval.decision == GatewayGovernanceDecision.APPROVAL_REQUIRED
    assert monitor.decision == GatewayGovernanceDecision.MONITOR


def test_gateway_evidence_excludes_raw_prompt_and_context() -> None:
    result = evaluate_gateway_governance(
        _request(
            contains_pii=True,
            raw_prompt="Prompt contains alice@example.com and api_key=secret",
            raw_context="Retrieved private context",
            raw_payload={"token": "secret-token"},
        ),
        config=_config(),
    )
    payload = safe_gateway_governance_evidence_payload(
        {
            **result.evidence.model_dump(mode="json"),
            "raw_prompt": "Prompt contains alice@example.com and api_key=secret",
            "raw_context": "Retrieved private context",
            "token": "secret-token",
        }
    )
    serialized = str(payload)

    assert "raw_prompt" not in payload
    assert "raw_context" not in payload
    assert "token" not in payload
    assert "alice@example.com" not in serialized
    assert "secret-token" not in serialized
    assert "Retrieved private context" not in serialized
