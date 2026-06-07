# RAG Prompt-Injection Scanner Reproduction Commands

Run from the repository root.

## Static diff check

```bash
git diff --check
```

## Python compile smoke

```bash
python -m py_compile backend/onyx/security_layer/scanners/__init__.py backend/onyx/security_layer/scanners/models.py backend/onyx/security_layer/scanners/decision_mapper.py backend/onyx/security_layer/scanners/llamafirewall_adapter.py backend/onyx/security_layer/scanners/rag_injection_scanner.py backend/onyx/security_layer/langfuse_evidence.py backend/onyx/tools/tool_implementations/utils.py backend/tests/security_layer/test_rag_injection_scanner.py scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

If local dependencies are missing, retry with:

```bash
source .venv/bin/activate
python -m py_compile backend/onyx/security_layer/scanners/__init__.py backend/onyx/security_layer/scanners/models.py backend/onyx/security_layer/scanners/decision_mapper.py backend/onyx/security_layer/scanners/llamafirewall_adapter.py backend/onyx/security_layer/scanners/rag_injection_scanner.py backend/onyx/security_layer/langfuse_evidence.py backend/onyx/tools/tool_implementations/utils.py backend/tests/security_layer/test_rag_injection_scanner.py scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

## Targeted pytest

```bash
PYTHONPATH=backend pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_rag_injection_scanner.py -q
```

## Demo attack

```bash
python scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

Expected high-level result:

- With the scanner disabled, the authorized attack chunk remains in context.
- With `SECURITY_RAG_INJECTION_SCANNER_MODE=deny`, the attack chunk is excluded.
- With `SECURITY_RAG_INJECTION_SCANNER_MODE=sanitize`, detected instruction text is replaced with a placeholder.
- Provider selection defaults to the proven local heuristic scanner.
- If `SECURITY_RAG_SCANNER_PROVIDER=llamafirewall` is configured without a compatible backend dependency, the scanner path does not crash.
- `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=heuristic|monitor|deny` controls the unavailable-backend fallback behavior.
- Evidence metadata does not contain raw retrieved chunk text.
- Real LlamaFirewall backend behavior is not proven unless the dependency is installed and these tests/demos are rerun in that environment.
