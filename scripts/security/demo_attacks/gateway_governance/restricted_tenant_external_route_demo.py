#!/usr/bin/env python
# ruff: noqa: E402
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend"))

from onyx.security_layer.gateway_governance import (
    evaluate_gateway_governance,  # noqa: E402
)
from onyx.security_layer.gateway_governance import GatewayGovernanceConfig  # noqa: E402
from onyx.security_layer.gateway_governance import (
    GatewayGovernanceRequest,  # noqa: E402
)
from onyx.security_layer.gateway_governance import GatewayPolicyMode  # noqa: E402
from onyx.security_layer.gateway_governance.evidence import (  # noqa: E402
    build_gateway_governance_evidence,
)


def main() -> int:
    request = GatewayGovernanceRequest(
        user_id="demo-user",
        tenant_id="tenant-a",
        model_provider="external-provider",
        requested_model="external-model",
        data_classification="restricted",
        contains_restricted_tenant_data=True,
        external_provider=True,
        correlation_id="demo-gateway-restricted-external-route",
        raw_context="restricted tenant document content omitted from evidence",
    )
    result = evaluate_gateway_governance(
        request,
        config=GatewayGovernanceConfig(
            enabled=True,
            restricted_external_mode=GatewayPolicyMode.ROUTE_PRIVATE,
        ),
    )
    evidence = build_gateway_governance_evidence(result.evidence)
    print(json.dumps({"decision": result.decision.value, "route_target": result.route_target.value, "evidence": evidence}, indent=2, sort_keys=True))
    return 0 if result.decision.value == "route_private" else 1


if __name__ == "__main__":
    raise SystemExit(main())
