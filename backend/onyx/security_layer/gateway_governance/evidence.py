from __future__ import annotations

from collections.abc import Mapping

from onyx.security_layer.gateway_governance.models import GatewayGovernanceEvidence
from onyx.security_layer.redaction import safe_metadata

_SAFE_GATEWAY_EVIDENCE_FIELDS = frozenset(
    {
        "model_provider",
        "requested_model",
        "data_classification",
        "decision",
        "route_target",
        "contains_pii",
        "contains_secret",
        "restricted_data",
        "correlation_id",
    }
)
_SAFE_SCALAR_TYPES = (str, bool, int, float)


def safe_gateway_governance_evidence_payload(
    metadata: Mapping[str, object | None],
) -> dict[str, str | bool | int | float]:
    payload: dict[str, str | bool | int | float] = {}
    for key in _SAFE_GATEWAY_EVIDENCE_FIELDS:
        value = metadata.get(key)
        if value is None:
            continue
        if isinstance(value, _SAFE_SCALAR_TYPES):
            payload[key] = value
    redacted = safe_metadata(payload)
    return {
        key: value
        for key, value in redacted.items()
        if isinstance(value, _SAFE_SCALAR_TYPES)
    }


def build_gateway_governance_evidence(
    evidence: GatewayGovernanceEvidence,
) -> dict[str, str | bool | int | float]:
    return safe_gateway_governance_evidence_payload(evidence.model_dump(mode="json"))
