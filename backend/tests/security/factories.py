from __future__ import annotations

from copy import deepcopy

BASE_CONTEXT: dict[str, object] = {
    "user_id": "user-alpha",
    "tenant_id": "tenant-alpha",
    "resource_type": "retrieval_chunk",
    "resource_id": "doc-alpha:1",
    "action": "retrieval.read",
    "source": "pytest",
    "risk_level": "medium",
    "correlation_id": "corr-security-test",
    "resource_tenant_id": "tenant-alpha",
}


def valid_same_tenant_context() -> dict[str, object]:
    return deepcopy(BASE_CONTEXT)


def missing_user_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context["user_id"] = None
    return context


def missing_tenant_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context["tenant_id"] = None
    return context


def cross_tenant_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context["resource_tenant_id"] = "tenant-bravo"
    return context


def unknown_action_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context["action"] = "unknown.action"
    return context


def high_risk_tool_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context.update(
        {
            "resource_type": "tool",
            "resource_id": "shell-tool",
            "action": "tool.execute",
            "risk_level": "high",
        }
    )
    return context


def monitor_only_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context["monitor_only"] = True
    return context


def approval_required_context() -> dict[str, object]:
    return high_risk_tool_context()


def unsafe_sandbox_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context.update(
        {
            "resource_type": "sandbox",
            "resource_id": "command:rm-rf",
            "action": "sandbox.execute",
            "risk_level": "critical",
        }
    )
    return context


def artifact_access_context() -> dict[str, object]:
    context = valid_same_tenant_context()
    context.update(
        {
            "resource_type": "artifact",
            "resource_id": "artifact-safe-demo",
            "action": "artifact.download",
            "risk_level": "low",
        }
    )
    return context
