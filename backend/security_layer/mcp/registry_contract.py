# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from __future__ import annotations
import re

MCP_REGISTRY_SCHEMA_VERSION = "1.0"
REQUIRED_MCP_REGISTRY_FIELDS = (
"mcp_server_id","mcp_server_name","mcp_server_version","mcp_server_owner","mcp_server_status","mcp_server_trust_tier","mcp_server_allowed_tenant_scope","mcp_server_allowed_workspace_scope","mcp_tool_id","mcp_tool_name","mcp_tool_version","mcp_tool_risk_tier","mcp_tool_status","mcp_resource_id","mcp_resource_type","mcp_resource_acl_policy_id","mcp_prompt_id","mcp_prompt_isolation_policy_id","required_user_permissions","required_group_permissions","required_role_permissions","service_account_allowed","delegated_credential_required","delegated_credential_scope","approval_required","approval_risk_level","egress_policy_id","request_signing_required","replay_protection_required","response_safety_policy_id","audit_required","finding_required_on_violation","metric_required","default_effect","metadata_schema_version")
OPTIONAL_MCP_REGISTRY_FIELDS=("description",)
FORBIDDEN_MCP_REGISTRY_FIELDS=("api_key","token","password","private_key","secret")
_PAT=re.compile(r"(api[_-]?key|token|password|private[_-]?key|secret|AKIA[0-9A-Z]{16}|-----BEGIN PRIVATE KEY-----|@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",re.I)

def sanitize_mcp_registry_entry(entry:dict[str,object])->dict[str,object]:
    out={}
    for k,v in entry.items():
        if any(x in k.lower() for x in FORBIDDEN_MCP_REGISTRY_FIELDS): continue
        if isinstance(v,str) and _PAT.search(v): out[k]="[redacted]"
        else: out[k]=v
    return out

def validate_mcp_registry_schema_version(entry:dict[str,object])->tuple[bool,str]:
    return (entry.get("metadata_schema_version")==MCP_REGISTRY_SCHEMA_VERSION,"invalid_schema_version")

def validate_no_forbidden_mcp_registry_content(entry:dict[str,object])->tuple[bool,str]:
    for k,v in entry.items():
        if any(x in k.lower() for x in FORBIDDEN_MCP_REGISTRY_FIELDS): return False,"forbidden_field"
        if isinstance(v,str) and _PAT.search(v): return False,"forbidden_content"
    return True,"ok"

def validate_mcp_registry_entry(entry:dict[str,object])->tuple[bool,list[str]]:
    errors=[f"missing:{f}" for f in REQUIRED_MCP_REGISTRY_FIELDS if f not in entry]
    if any(k not in REQUIRED_MCP_REGISTRY_FIELDS+OPTIONAL_MCP_REGISTRY_FIELDS for k in entry):
        errors.append("unexpected_field")
    okv,msg=validate_mcp_registry_schema_version(entry)
    if not okv: errors.append(msg)
    okc,msg=validate_no_forbidden_mcp_registry_content(entry)
    if not okc: errors.append(msg)
    return (not errors,errors)

def build_safe_mcp_registry_entry(**kwargs:object)->dict[str,object]:
    e={f:kwargs.get(f) for f in REQUIRED_MCP_REGISTRY_FIELDS}
    for f in OPTIONAL_MCP_REGISTRY_FIELDS:
        if f in kwargs: e[f]=kwargs[f]
    return sanitize_mcp_registry_entry(e)
