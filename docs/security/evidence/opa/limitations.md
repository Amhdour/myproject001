# OPA Retrieval ACL Limitations

- This is a small Retrieval ACL policy-as-code layer only. It is not integrated across every tool or runtime surface.
- This change does not claim production readiness.
- The live RAG patch point added here is intentionally narrow: internal-search `InferenceSection` objects are filtered immediately before `convert_inference_sections_to_llm_string` serializes retrieved chunk text into the LLM-facing tool response.
- OPA Retrieval ACL context enforcement is controlled by `SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT=true`. Without that flag, existing context serialization behavior is preserved.
- OPA availability is not guaranteed by this repository change. If context enforcement is enabled and OPA is unavailable, high-risk retrieval context-inclusion decisions are denied and decision evidence marks `fallback_used = true`.
- Runtime OPA enforcement currently uses metadata already present on retrieved chunks, especially `onyx_acl` metadata. This does not replace DB-backed permission checks or prove every connector emits complete ACL metadata.
- The demo attack script uses a deterministic in-process simulation of the Rego decision so evidence can be generated without requiring a running OPA server.
- The Rego validation commands require the `opa` CLI to be installed in the execution environment; CI installs the pinned OPA CLI version before running `opa fmt --check`, `opa check`, and `opa test`.
- Local validation on 2026-06-07 found that `opa` was not installed: `/bin/bash: line 1: opa: command not found`.
- Local validation on 2026-06-07 could not install OPA from the public release download URLs because the local agent environment returned `curl: (56) CONNECT tunnel failed, response 403`; this is an environment/network limitation, not evidence that the policy passes or fails.
- Local validation on 2026-06-07 found that the project Python environment was missing dependencies required by existing security-layer imports; without the virtual environment, `sqlalchemy` was missing, and with `source .venv/bin/activate`, `pydantic` was missing.
- `pytest backend/onyx/security_layer -q` returned exit code 5 because no tests were collected from the source directory path.
- `pytest backend/tests/security_layer/test_opa_retrieval_acl.py -q` could not load the repository test `conftest.py` because `fastapi_users` is missing. The same blocker occurred after `source .venv/bin/activate`.
- OpenTelemetry trace linkage is documented separately under `docs/security/evidence/opentelemetry/`; trace export depends on deployment tracer-provider/exporter configuration and does not prove production readiness.
- CI OPA validation does not prove live RAG runtime enforcement.
- CI OPA validation does not prove production readiness.
- The previously referenced GitHub Actions OPA validation run failed at the formatting step; it is not evidence that `opa check` or `opa test` completed successfully.
