"""OPA integration helpers for Retrieval ACL policy decisions."""

from __future__ import annotations

from typing import Any

__all__ = [
    "OPAClient",
    "OPADecision",
    "OPADecisionValue",
    "OPAUnavailableError",
    "filter_sections_for_opa_retrieval_acl_context",
    "opa_retrieval_acl_context_enforcement_enabled",
    "build_retrieval_acl_input",
]


def __getattr__(name: str) -> Any:
    if name in {"OPADecision", "OPADecisionValue"}:
        from onyx.security_layer.opa import decision_mapper

        return getattr(decision_mapper, name)
    if name == "build_retrieval_acl_input":
        from onyx.security_layer.opa.input_builder import build_retrieval_acl_input

        return build_retrieval_acl_input
    if name in {"OPAClient", "OPAUnavailableError"}:
        from onyx.security_layer.opa import opa_client

        return getattr(opa_client, name)
    if name in {
        "filter_sections_for_opa_retrieval_acl_context",
        "opa_retrieval_acl_context_enforcement_enabled",
    }:
        from onyx.security_layer.opa import retrieval_context_filter

        return getattr(retrieval_context_filter, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
