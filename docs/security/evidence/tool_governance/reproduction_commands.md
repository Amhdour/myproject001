# Reproduction Commands

Run from the repository root.

```bash
git diff --check
```

```bash
source .venv/bin/activate && python -m py_compile \
  backend/onyx/security_layer/audit/__init__.py \
  backend/onyx/security_layer/tool_governance/__init__.py \
  backend/onyx/security_layer/tool_governance/models.py \
  backend/onyx/security_layer/tool_governance/risk_registry.py \
  backend/onyx/security_layer/tool_governance/decision_mapper.py \
  backend/onyx/security_layer/tool_governance/approval.py \
  backend/onyx/security_layer/tool_governance/receipts.py \
  backend/onyx/security_layer/tool_governance/enforcement.py \
  backend/onyx/security_layer/langfuse_evidence.py \
  backend/onyx/tools/tool_runner.py \
  backend/tests/security_layer/test_tool_governance.py \
  scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py
```

```bash
python -m ruff check \
  backend/onyx/security_layer/audit/__init__.py \
  backend/onyx/security_layer/tool_governance/__init__.py \
  backend/onyx/security_layer/tool_governance/models.py \
  backend/onyx/security_layer/tool_governance/risk_registry.py \
  backend/onyx/security_layer/tool_governance/decision_mapper.py \
  backend/onyx/security_layer/tool_governance/approval.py \
  backend/onyx/security_layer/tool_governance/receipts.py \
  backend/onyx/security_layer/tool_governance/enforcement.py \
  backend/onyx/security_layer/langfuse_evidence.py \
  backend/onyx/tools/tool_runner.py \
  backend/tests/security_layer/test_tool_governance.py \
  scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py
```

```bash
source .venv/bin/activate && PYTHONPATH=backend pytest -q backend/tests/security_layer/test_tool_governance.py --confcutdir=backend/tests/security_layer
```

```bash
PYTHONPATH=backend python scripts/security/demo_attacks/tool_governance/high_risk_tool_requires_approval_demo.py
```
