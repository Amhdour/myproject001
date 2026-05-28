from backend.security_layer.shadow_deny.models import ShadowDenyControlFamily
from backend.security_layer.shadow_deny.simulator import apply_shadow_deny_rollback_if_enabled, simulate_shadow_deny_decision


def _simulate(context, family, monitor_only_decision=None):
    context.control_family = family
    decision = simulate_shadow_deny_decision(context, monitor_only_decision=monitor_only_decision)
    return apply_shadow_deny_rollback_if_enabled(context, decision)


def simulate_retrieval_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.RETRIEVAL, monitor_only_decision)

def simulate_vector_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.VECTOR, monitor_only_decision)

def simulate_cache_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.CACHE, monitor_only_decision)

def simulate_tool_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.TOOL, monitor_only_decision)

def simulate_mcp_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.MCP, monitor_only_decision)

def simulate_artifact_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.ARTIFACT, monitor_only_decision)

def simulate_ingestion_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.INGESTION, monitor_only_decision)

def simulate_safe_denial_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.SAFE_DENIAL, monitor_only_decision)

def simulate_audit_metric_shadow_deny(context, monitor_only_decision=None):
    return _simulate(context, ShadowDenyControlFamily.AUDIT_METRIC, monitor_only_decision)
