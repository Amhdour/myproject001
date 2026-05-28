from __future__ import annotations
from urllib.parse import urlparse
from .models import MCPEgressDecision, MCPEgressPolicy

def sanitize_mcp_egress_target(value:str)->str:
    p=urlparse(value)
    return f"{p.scheme}://{p.hostname}" if p.scheme and p.hostname else value

def validate_mcp_egress_policy(policy:MCPEgressPolicy): return (bool(policy.egress_policy_id),"ok" if policy.egress_policy_id else "missing_policy_id")
def validate_mcp_target_domain(value:str, policy:MCPEgressPolicy):
    h=(urlparse(value).hostname or value).lower()
    if policy.denied_domains and h in policy.denied_domains: return False,"denied_domain"
    if policy.allowed_domains and h not in policy.allowed_domains: return False,"not_allowed_domain"
    return True,"ok"
def validate_mcp_no_internal_network_target(value:str):
    h=(urlparse(value).hostname or value).lower()
    return (not (h.startswith("10.") or h.startswith("192.168.") or h.startswith("127.") or h=="localhost"),"internal_target")
def validate_mcp_no_metadata_service_target(value:str):
    h=(urlparse(value).hostname or value).lower(); return (h!="169.254.169.254","metadata_target")
def validate_mcp_no_credential_exfiltration_target(value:str):
    l=value.lower(); return ("token=" not in l and "api_key=" not in l and "password=" not in l,"credential_exfil_target")
def build_mcp_egress_decision(value:str, policy:MCPEgressPolicy):
    checks=[validate_mcp_target_domain(value,policy),validate_mcp_no_internal_network_target(value),validate_mcp_no_metadata_service_target(value),validate_mcp_no_credential_exfiltration_target(value)]
    if all(c[0] for c in checks): return MCPEgressDecision.ALLOW,"ok"
    if any(c[1]=="metadata_target" for c in checks if not c[0]): return MCPEgressDecision.DENY,"metadata_target"
    return MCPEgressDecision.FLAG,"unsafe_egress"
