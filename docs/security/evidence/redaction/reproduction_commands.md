# Redaction Evidence Reproduction Commands

Run commands from the repository root.

## Static diff check

```bash
git diff --check
```

## Python compile smoke

```bash
python -m py_compile backend/onyx/security_layer/redaction.py backend/onyx/security_layer/langfuse_evidence.py backend/tests/security_layer/test_redaction.py backend/tests/security_layer/test_langfuse_evidence.py
```

If local Python dependencies are missing, retry with the project virtual environment activated:

```bash
source .venv/bin/activate
python -m py_compile backend/onyx/security_layer/redaction.py backend/onyx/security_layer/langfuse_evidence.py backend/tests/security_layer/test_redaction.py backend/tests/security_layer/test_langfuse_evidence.py
```

## Direct import and fallback smoke

```bash
PYTHONPATH=backend python - <<'PY'
from onyx.security_layer.redaction import redact_mapping
from onyx.security_layer.redaction import redact_text
from onyx.security_layer.redaction import safe_metadata

assert redact_text("admin@example.com") == "[REDACTED]"
assert redact_text("Authorization: Bearer abc.def.ghi") == "Authorization: [REDACTED]"

source = {
    "correlation_id": "corr-admin@example.com",
    "reviewer": "reviewer@example.com",
    "headers": {"Authorization": "Bearer abc.def.ghi"},
}
redacted = redact_mapping(source)
metadata = safe_metadata(source)

assert source["reviewer"] == "reviewer@example.com"
assert redacted["reviewer"] == "[REDACTED]"
assert redacted["headers"] == {"Authorization": "[REDACTED]"}
assert metadata["correlation_id"] == "corr-admin@example.com"
print(redacted)
print(metadata)
PY
```

## Pytest

```bash
pytest backend/tests/security_layer/test_redaction.py backend/tests/security_layer/test_langfuse_evidence.py -q
```

If repository test dependencies are unavailable in a local environment, record the missing dependency as an environment limitation rather than treating that as live production validation.
