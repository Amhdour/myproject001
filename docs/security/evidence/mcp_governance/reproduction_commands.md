# MCP Governance Reproduction Commands

Run from the repository root after activating the Python virtual environment if needed.

```bash
git diff --check
python -m py_compile backend/onyx/security_layer/mcp_governance/__init__.py backend/onyx/security_layer/mcp_governance/models.py backend/onyx/security_layer/mcp_governance/registry.py backend/onyx/security_layer/mcp_governance/decision_mapper.py backend/onyx/security_layer/mcp_governance/receipts.py backend/onyx/security_layer/mcp_governance/enforcement.py backend/onyx/mcp_server/tools/search.py backend/tests/security_layer/test_mcp_governance.py backend/tests/security_layer/test_mcp_governance_enforcement.py scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py
python -m ruff check backend/onyx/security_layer/mcp_governance/__init__.py backend/onyx/security_layer/mcp_governance/models.py backend/onyx/security_layer/mcp_governance/registry.py backend/onyx/security_layer/mcp_governance/decision_mapper.py backend/onyx/security_layer/mcp_governance/receipts.py backend/onyx/security_layer/mcp_governance/enforcement.py backend/onyx/mcp_server/tools/search.py backend/tests/security_layer/test_mcp_governance.py backend/tests/security_layer/test_mcp_governance_enforcement.py scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py
pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_mcp_governance.py backend/tests/security_layer/test_mcp_governance_enforcement.py
python scripts/security/demo_attacks/mcp_governance/mcp_scope_bypass_demo.py
```
