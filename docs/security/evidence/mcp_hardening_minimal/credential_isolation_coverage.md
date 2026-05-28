# MCP Credential Isolation Coverage

`backend/security_layer/mcp/credential_isolation.py` includes concrete checks for:
- credential scope requirements
- credential lifetime/expiration
- tenant boundary
- user boundary
- service credential boundary
- delegated credential boundary

It also includes raw credential exposure detection and metadata sanitization helpers.
