# RAG Prompt-Injection Scanner Reproduction Commands

Run from the repository root.

## Static diff check

```bash
git diff --check
```

## Python compile smoke

```bash
python -m py_compile backend/onyx/security_layer/scanners/__init__.py backend/onyx/security_layer/scanners/models.py backend/onyx/security_layer/scanners/decision_mapper.py backend/onyx/security_layer/scanners/rag_injection_scanner.py backend/onyx/security_layer/langfuse_evidence.py backend/onyx/tools/tool_implementations/utils.py backend/tests/security_layer/test_rag_injection_scanner.py scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

If local dependencies are missing, retry with:

```bash
source .venv/bin/activate
python -m py_compile backend/onyx/security_layer/scanners/__init__.py backend/onyx/security_layer/scanners/models.py backend/onyx/security_layer/scanners/decision_mapper.py backend/onyx/security_layer/scanners/rag_injection_scanner.py backend/onyx/security_layer/langfuse_evidence.py backend/onyx/tools/tool_implementations/utils.py backend/tests/security_layer/test_rag_injection_scanner.py scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

## Targeted pytest

```bash
PYTHONPATH=backend pytest --confcutdir=backend/tests backend/tests/security_layer/test_rag_injection_scanner.py -q
```

## Demo attack

```bash
python scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

Expected high-level result:

- With the scanner disabled, the authorized attack chunk remains in context.
- With `SECURITY_RAG_INJECTION_SCANNER_MODE=deny`, the attack chunk is excluded.
- With `SECURITY_RAG_INJECTION_SCANNER_MODE=sanitize`, detected instruction text is replaced with a placeholder.
- Evidence metadata does not contain raw retrieved chunk text.
