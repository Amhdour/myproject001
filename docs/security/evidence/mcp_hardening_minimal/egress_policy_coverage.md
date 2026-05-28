# MCP Egress Policy Coverage

`backend/security_layer/mcp/egress_policy.py` includes concrete checks for:
- internal network target blocking
- metadata service target blocking (`169.254.169.254`)
- disallowed domain handling
- credential exfiltration target patterns (`token=`, `api_key=`, `password=`)

It also evaluates allowed/denied domains and computes allow/flag/deny decisions.
