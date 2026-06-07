# Reproduction Commands

```bash
python scripts/security/evaluations/run_rag_security_eval.py
python -m pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_rag_security_evaluations.py
```

Optional dependency-backed checks:

```bash
# Run only if ragas is installed
python scripts/security/evaluations/run_rag_security_eval.py --run-ragas

# Run only if promptfoo CLI is installed
python scripts/security/evaluations/run_rag_security_eval.py --run-promptfoo-cli
```
