# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from backend.security_layer.mcp.egress_policy import *
from backend.security_layer.mcp.models import MCPEgressPolicy,MCPEgressDecision

def test_egress_flags():
    p=MCPEgressPolicy('p1',allowed_domains=('example.com',),denied_domains=('bad.com',))
    assert build_mcp_egress_decision('http://169.254.169.254',p)[0] in {MCPEgressDecision.DENY,MCPEgressDecision.FLAG}
