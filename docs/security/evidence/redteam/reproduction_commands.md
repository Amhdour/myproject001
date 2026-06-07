# Reproduction Commands

Run from the repository root:

```bash
python scripts/security/redteam/run_external_redteam_summary.py
python -m pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_redteam_evidence.py
```

Optional dependency-backed red-team tools are not invoked by default. True PyRIT or garak execution is not proven unless those dependencies are installed and explicit dependency-backed runs occur outside the fixture parser.
