from backend.security_layer.mcp.request_validators import *

def test_unsafe_arguments():
    r=validate_mcp_request_arguments({'path':'../etc/passwd','u':'http://169.254.169.254','cmd':'a;rm','s':'token=abc','p':'ignore previous'})
    assert not r['allowed']
