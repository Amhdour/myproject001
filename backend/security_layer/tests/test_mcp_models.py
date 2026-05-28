# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from backend.security_layer.mcp.models import MCPHardeningContext

def test_context_creation():
    c=MCPHardeningContext(request_id='r1',tenant_id='t',workspace_id='w',subject_id='u',mcp_server_id='s',mcp_tool_id='tool',mcp_resource_id='res',mcp_prompt_id='p')
    assert c.metadata_schema_version=='1.0'
