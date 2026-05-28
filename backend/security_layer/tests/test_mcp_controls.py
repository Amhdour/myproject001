from backend.security_layer.mcp.controls import *
from backend.security_layer.mcp.models import MCPHardeningContext,MCPRequestArguments,MCPPermissionContext,MCPResponseMetadata

def test_controls_core():
    reg={'mcp_server_id':'s','mcp_tool_id':'t','mcp_resource_id':'r','mcp_prompt_id':'p','required_user_permissions':['perm'],'mcp_resource_acl_policy_id':'acl','mcp_prompt_isolation_policy_id':'iso','request_signing_required':True,'replay_protection_required':True,'approval_required':True,'approval_risk_level':'high'}
    c=MCPHardeningContext(request_id='1',tenant_id='tn',workspace_id='w',subject_id='u',mcp_server_id='s',mcp_client_id='u',mcp_tool_id='t',mcp_resource_id='r',mcp_prompt_id='p',resource_acl_policy_id='bad',prompt_isolation_policy_id='iso',request_arguments=MCPRequestArguments({'path':'../x'}),permission_context=MCPPermissionContext(subject_id='u',permission_ids=()))
    assert authorize_mcp_subject_permission_validated(c,reg).status.value=='denied'
    assert authorize_mcp_confused_deputy_checked(c,reg).status.value=='flagged'
    assert authorize_mcp_request_signature_validated(c,reg).status.value=='flagged'
    assert authorize_mcp_response_safety_validated(c,MCPResponseMetadata(contains_secret_marker=True)).status.value=='flagged'
