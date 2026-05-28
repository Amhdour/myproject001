# MCP Request Validator Coverage

`backend/security_layer/mcp/request_validators.py` includes concrete checks for:
- path traversal detection
- SSRF URL detection
- command injection detection
- secret-bearing argument value detection
- prompt injection marker detection

It also includes argument type/length/name checks and composite request argument validation.
