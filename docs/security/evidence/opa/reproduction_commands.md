# OPA Retrieval ACL Reproduction Commands

Run from the repository root.

```bash
opa fmt --check backend/onyx/security_layer/policy/opa/
opa check backend/onyx/security_layer/policy/opa/
opa test backend/onyx/security_layer/policy/opa/
pytest backend/onyx/security_layer -q
python scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py
```

If Python dependencies are missing, retry Python commands with the project virtual environment activated:

```bash
source .venv/bin/activate
pytest backend/onyx/security_layer -q
```
