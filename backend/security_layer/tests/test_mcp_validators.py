from backend.security_layer.mcp.validators import *
from backend.security_layer.mcp.models import MCPHardeningContext,MCPResponseMetadata,MCPPermissionContext

def test_validator_denies_and_flags():
    c=MCPHardeningContext(request_id='r')
    assert validate_mcp_hardening_context(c).status.value=='denied'
    c2=MCPHardeningContext(request_id='r',tenant_id='t',workspace_id='w',subject_id='u',permission_context=MCPPermissionContext(subject_id='u',permission_ids=('a',)))
    assert validate_mcp_response_safety(c2,MCPResponseMetadata(contains_secret_marker=True)).status.value=='flagged'
