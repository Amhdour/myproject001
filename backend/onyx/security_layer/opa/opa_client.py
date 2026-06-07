from __future__ import annotations

from typing import Any

import httpx

from onyx.security_layer.opa.decision_mapper import OPADecision
from onyx.security_layer.opa.decision_mapper import map_opa_result
from onyx.security_layer.opa.fallback import deny_high_risk_retrieval_fallback

DEFAULT_OPA_RETRIEVAL_ACL_URL = "http://localhost:8181/v1/data/onyx/security/retrieval_acl/decision"


class OPAUnavailableError(RuntimeError):
    pass


class OPAClient:
    def __init__(self, *, url: str = DEFAULT_OPA_RETRIEVAL_ACL_URL, timeout_seconds: float = 1.0) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds

    def evaluate_retrieval_acl(self, opa_input: dict[str, Any]) -> OPADecision:
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(self.url, json={"input": opa_input})
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise OPAUnavailableError(str(exc)) from exc

        result = payload.get("result")
        if not isinstance(result, dict):
            raise OPAUnavailableError("OPA response missing object result")
        return map_opa_result(result, opa_input)


def evaluate_retrieval_acl_with_fallback(client: OPAClient, opa_input: dict[str, Any]) -> OPADecision:
    try:
        return client.evaluate_retrieval_acl(opa_input)
    except OPAUnavailableError as exc:
        return deny_high_risk_retrieval_fallback(opa_input, str(exc))
