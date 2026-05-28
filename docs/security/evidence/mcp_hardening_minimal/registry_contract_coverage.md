# MCP Registry Contract Coverage

`backend/security_layer/mcp/registry_contract.py` includes required contract validation with **35** required fields via `REQUIRED_MCP_REGISTRY_FIELDS` and enforcement in `validate_mcp_registry_entry`.

It also includes:
- metadata schema version check
- forbidden content checks
- unknown-field rejection
- sample entry builder from required+optional field sets
