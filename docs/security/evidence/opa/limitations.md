# OPA Retrieval ACL Limitations

- This is a small Retrieval ACL policy-as-code layer only. It is not integrated across every tool or runtime surface.
- This change does not claim production readiness.
- OPA availability is not guaranteed by this repository change. If OPA is unavailable, high-risk retrieval context-inclusion decisions are denied and decision evidence records `fallback_used = true`.
- The demo attack script uses a deterministic in-process simulation of the Rego decision so evidence can be generated without requiring a running OPA server.
- The Rego validation commands require the `opa` CLI to be installed in the execution environment; CI installs the pinned OPA CLI version before running `opa fmt --check`, `opa check`, and `opa test`.
- Local validation on 2026-06-07 found that `opa` was not installed: `/bin/bash: line 1: opa: command not found`.
- Local validation on 2026-06-07 could not install OPA from the public release download URLs because the local agent environment returned `curl: (56) CONNECT tunnel failed, response 403`; this is an environment/network limitation, not evidence that the policy passes or fails.
- Local validation on 2026-06-07 found that the project Python environment was missing dependencies required by existing security-layer imports; without the virtual environment, `sqlalchemy` was missing, and with `source .venv/bin/activate`, `pydantic` was missing.
- `pytest backend/onyx/security_layer -q` returned exit code 5 because no tests were collected from the source directory path.
- `pytest backend/tests/security_layer/test_opa_retrieval_acl.py -q` could not load the repository test `conftest.py` because `fastapi_users` is missing. The same blocker occurred after `source .venv/bin/activate`.
