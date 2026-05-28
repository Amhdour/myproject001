import time
from backend.security_layer.mcp.credential_isolation import *
from backend.security_layer.mcp.models import MCPCredentialContext

def test_credential_denies():
    c=MCPCredentialContext(placeholder_only=True,tenant_id='t',subject_id='u',expires_at=int(time.time())-10)
    assert validate_mcp_credential_lifetime(c)[0] is False
    assert detect_raw_mcp_credential_exposure('password=1')
