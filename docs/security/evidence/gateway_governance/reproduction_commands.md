# Gateway Governance Reproduction Commands

Run from the repository root after activating the Python virtual environment if needed.

```bash
git diff --check
python -m py_compile backend/onyx/security_layer/gateway_governance/__init__.py backend/onyx/security_layer/gateway_governance/models.py backend/onyx/security_layer/gateway_governance/route_policy.py backend/onyx/security_layer/gateway_governance/decision_mapper.py backend/onyx/security_layer/gateway_governance/evidence.py backend/tests/security_layer/test_gateway_governance.py scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py
python -m ruff check backend/onyx/security_layer/gateway_governance/__init__.py backend/onyx/security_layer/gateway_governance/models.py backend/onyx/security_layer/gateway_governance/route_policy.py backend/onyx/security_layer/gateway_governance/decision_mapper.py backend/onyx/security_layer/gateway_governance/evidence.py backend/tests/security_layer/test_gateway_governance.py scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py
pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_gateway_governance.py
python scripts/security/demo_attacks/gateway_governance/external_secret_route_block_demo.py
python scripts/security/demo_attacks/gateway_governance/restricted_tenant_external_route_demo.py
```
