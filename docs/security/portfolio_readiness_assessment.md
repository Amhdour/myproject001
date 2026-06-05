# Portfolio Readiness Assessment — Security Readiness MVP

## Confirmed repository state before implementation

Repository-visible inspection confirmed an Onyx-based backend with FastAPI/server modules under `backend/onyx/server`, RAG/search retrieval code under `backend/onyx/context/search`, existing security-layer packages under both `backend/onyx/security_layer` and `backend/security_layer`, security tests under `backend/tests/security_layer`, and many existing GitHub Actions workflows under `.github/workflows`.

The requested security documentation files already existed before this MVP update: `docs/security/README.md`, `security_requirements.md`, `control_traceability_matrix.md`, `evidence_report.md`, `known_limitations.md`, `execution_tracker.md`, `test_data_factories.md`, and `docs/security/evidence/`.

## What was proven before this implementation

- The repository already contained planning/security documentation and several security-layer modules.
- Existing retrieval code called retrieval guard and runtime-enforcement hooks from `backend/onyx/context/search/retrieval/search_runner.py`.
- Existing CI workflow files were present.

## What was not proven before this implementation

- A small, easy-to-review policy-as-code MVP with required context fields and four requested decision values was not isolated in the requested portfolio format.
- Runtime enforcement evidence for the exact MVP policy requirements was not tied to fresh negative tests, demo attacks, audit samples, telemetry samples, and an evidence validation script.
- CI for this exact MVP evidence bundle was not present.

## Blockers and constraints

- Full backend test execution in this container is blocked by missing project dependencies in `.venv` and by `uv` attempting to resolve CPython/onnxruntime platform constraints.
- The MVP therefore uses deterministic security tests with `--confcutdir=backend/tests/security` and minimal dependencies (`pytest`, `pydantic`) for local/CI reproducibility.
- Live deployed route testing and staging validation were not performed.

## Readiness before implementation

Estimated readiness before this implementation: **35%**. This reflects documentation-heavy readiness with existing security-layer material, but without this MVP's self-contained policy/enforcement/tests/demo/evidence/CI proof bundle.

## Evidence missing before implementation

- Fresh local validation results for the MVP controls.
- MVP audit JSONL sample with allow, deny, approval-required, and monitor-only decisions.
- MVP telemetry JSON sample.
- Executable MVP demo attack tests and JSON/Markdown results.
- Evidence validation script and CI gate for the MVP evidence files.

## Final readiness calculation after implementation

| Category | Weight | Awarded | Evidence |
|---|---:|---:|---|
| Repository architecture understood | 10% | 10% | This assessment and repository inspection notes. |
| Security patch points identified | 10% | 8% | Retrieval path identified and patched; other paths documented as partially unwired. |
| Policy-as-code implemented | 10% | 10% | `backend/security/policy/*`. |
| Runtime enforcement implemented | 15% | 13% | `backend/security/enforcement/security_enforcer.py`; retrieval hook patch added. |
| Audit logging implemented | 10% | 10% | `backend/security/audit/security_audit_logger.py` and audit sample. |
| Telemetry implemented | 10% | 10% | `backend/security/telemetry/security_metrics.py` and telemetry sample. |
| Unit/negative tests passing | 15% | 15% | 25 MVP tests passed locally with minimal dependency command. |
| Demo attacks executable and blocked | 10% | 8% | 5 demo tests passed; prompt-injection scanning is limitation, not blocked. |
| CI gate present and passing or pending clearly | 5% | 4% | Workflow added; local CI-equivalent passed; GitHub Actions not run here. |
| Evidence report and walkthrough complete | 5% | 5% | Evidence report, matrix, limitations, walkthrough updated. |

Final portfolio readiness after this MVP: **85%**. The score is capped at 85% because GitHub Actions was configured but not actually run in this environment. This is portfolio-demonstrable, not production-ready.
