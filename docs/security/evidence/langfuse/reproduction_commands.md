# Langfuse Evidence Reproduction Commands

Run from the repository root.

## Static checks

```bash
git diff --check
```

## Python compile smoke

```bash
source .venv/bin/activate
python -m py_compile backend/onyx/security_layer/langfuse_evidence.py backend/onyx/security_layer/opa/retrieval_context_filter.py backend/tests/security_layer/test_langfuse_evidence.py
```

## Direct import and no-config smoke

```bash
PYTHONPATH=backend/onyx/security_layer python - <<'PY'
from langfuse_evidence import emit_opa_retrieval_acl_langfuse_evidence
from langfuse_evidence import safe_opa_retrieval_acl_langfuse_payload

metadata = {
    "correlation_id": "corr-1",
    "subject_user_id": "user-1",
    "subject_tenant_id": "tenant-a",
    "resource_document_id": "doc-1",
    "resource_chunk_id": "chunk-1",
    "resource_tenant_id": "tenant-a",
    "policy_package": "onyx.security.retrieval_acl",
    "decision": "allow",
    "reason": "same tenant allowed user",
    "fallback_used": False,
    "enforcement_enabled": True,
    "chunk_text": "must not export",
}

payload = safe_opa_retrieval_acl_langfuse_payload(metadata)
assert "chunk_text" not in payload
assert emit_opa_retrieval_acl_langfuse_evidence(metadata) is False
print(payload)
PY
```

## Pytest

```bash
source .venv/bin/activate
pytest backend/tests/security_layer/test_langfuse_evidence.py -q
```

If local Python dependencies are unavailable, record the missing dependency rather than treating that as live Langfuse validation.
