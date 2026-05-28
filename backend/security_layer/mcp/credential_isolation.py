# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from __future__ import annotations
import re, time
from .models import MCPCredentialContext

def detect_raw_mcp_credential_exposure(value:str)->bool:
    return bool(re.search(r"(api[_-]?key|token|password|secret|-----BEGIN PRIVATE KEY-----)",value,re.I))

def sanitize_mcp_credential_metadata(metadata:dict[str,object])->dict[str,object]:
    return {k:("[redacted]" if isinstance(v,str) and detect_raw_mcp_credential_exposure(v) else v) for k,v in metadata.items() if "secret" not in k.lower()}

def validate_mcp_credential_context(context:MCPCredentialContext): return (context.placeholder_only and not (context.credential_id and detect_raw_mcp_credential_exposure(context.credential_id)),"ok" if context.placeholder_only else "non_placeholder")
def validate_mcp_credential_scope(context, registry_entry): return (not registry_entry.get("delegated_credential_required") or bool(context.delegated_scope),"missing_scope")
def validate_mcp_credential_lifetime(context):
    now=int(time.time())
    if context.expires_at is None or context.expires_at<now: return False,"expired_credential"
    return True,"ok"
def validate_mcp_credential_tenant_boundary(context): return (bool(context.tenant_id),"missing_tenant")
def validate_mcp_credential_user_boundary(context): return (bool(context.subject_id),"missing_subject")
def validate_mcp_service_credential_boundary(context): return (context.credential_type.value!="service" or context.subject_id is None,"service_boundary_violation" if context.credential_type.value=="service" and context.subject_id else "ok")
def validate_mcp_delegated_credential_boundary(context): return (context.credential_type.value!="delegated" or bool(context.delegated_scope),"delegated_scope_missing")
