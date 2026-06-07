# OpenTelemetry Retrieval ACL Reproduction Commands

Run commands from the repository root.

## Import and compile checks

These checks prove the OpenTelemetry helper and instrumented OPA Retrieval ACL modules import or compile without requiring a running OpenTelemetry collector.

```bash
python -m py_compile backend/onyx/security_layer/tracing.py backend/onyx/security_layer/opa/retrieval_context_filter.py backend/onyx/security_layer/opa/decision_mapper.py backend/onyx/security_layer/opa/fallback.py
```

```bash
pytest backend/tests/security_layer/test_security_tracing.py backend/tests/security_layer/test_opa_retrieval_acl.py backend/tests/security_layer/test_opa_retrieval_context_filter.py -q
```

If Python dependencies are missing, retry with the project virtual environment activated:

```bash
source .venv/bin/activate
pytest backend/tests/security_layer/test_security_tracing.py backend/tests/security_layer/test_opa_retrieval_acl.py backend/tests/security_layer/test_opa_retrieval_context_filter.py -q
```

## Optional runtime trace export check

To observe exported spans, configure an OpenTelemetry tracer provider/exporter through the normal application runtime environment, enable OPA Retrieval ACL context enforcement, and exercise an internal-search RAG path that serializes `InferenceSection` results.

```bash
SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT=true pytest backend/tests/security_layer/test_opa_retrieval_context_filter.py -q
```

The test suite uses a local fake span recorder for schema verification; it does not require an OpenTelemetry collector and does not prove production readiness.
