from __future__ import annotations
import time
from .models import MCPDecisionStatus, MCPHardeningDecision, MCPHardeningStage

def validate_mcp_request_signature_context(context): return (True,"ok")
def validate_mcp_signature_required(context, registry_entry): return (not registry_entry.get("request_signing_required") or bool(context.signature_context.signature_id),"signature_required")
def validate_mcp_signature_present(context): return (bool(context.signature_context.signature_id),"missing_signature")
def validate_mcp_signature_freshness(context):
    if context.signature_context.signed_at is None: return False,"missing_signed_at"
    return (int(time.time())-context.signature_context.signed_at<=context.signature_context.max_signature_age_seconds,"stale_signature")
def validate_mcp_replay_context(context): return (True,"ok")
def validate_mcp_replay_protection_required(context, registry_entry): return (not registry_entry.get("replay_protection_required") or bool(context.replay_context.nonce),"replay_required")
def validate_mcp_replay_nonce_present(context): return (bool(context.replay_context.nonce),"missing_nonce")
def validate_mcp_replay_nonce_freshness(context):
    if context.replay_context.nonce_issued_at is None: return False,"missing_nonce_time"
    return (int(time.time())-context.replay_context.nonce_issued_at<=context.replay_context.max_nonce_age_seconds,"stale_nonce")
def build_mcp_replay_decision(stage, reason): return MCPHardeningDecision(stage=stage,status=MCPDecisionStatus.FLAGGED,reason_code=reason)
