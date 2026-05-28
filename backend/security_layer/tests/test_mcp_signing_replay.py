from backend.security_layer.mcp.signing_replay import *
from backend.security_layer.mcp.models import MCPHardeningContext

def test_signature_replay_missing():
    c=MCPHardeningContext(request_id='r')
    assert not validate_mcp_signature_present(c)[0]
    assert not validate_mcp_replay_nonce_present(c)[0]
