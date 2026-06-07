# Live Hook Gap Report

## Date

2026-06-07

## Scope

This report documents what was inspected for the real query → retrieval → context-construction path and what is, and is not, proven for the retrieved-content prompt-injection hook.

## Inspected files

- `backend/onyx/context/search/retrieval/search_runner.py`
- `backend/onyx/context/search/pipeline.py`
- `backend/security_layer/retrieval/prompt_injection/hook.py`
- `backend/security_layer/tests/test_retrieved_content_prompt_injection.py`
- `demo_attacks/run_demo_attacks.py`
- `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/`

## Likely patch points

- Retrieval-result boundary: `search_chunks()` in `backend/onyx/context/search/retrieval/search_runner.py`.
- Context-construction boundary: downstream `search_pipeline()` and `merge_individual_chunks()` in `backend/onyx/context/search/pipeline.py`.

## Confirmed hook status

- The hook is wired into `search_chunks()` after Step 39X runtime retrieval enforcement and before chunks are returned downstream.
- Focused tests execute `apply_retrieved_content_prompt_injection_hook()` directly and verify monitor, shadow-deny, enforce/quarantine, negative, redacted audit, telemetry, and source-level search-runner wiring behavior.
- Evidence is stored under `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/`.

## Missing proof

- No live deployed Onyx request was executed for this hook.
- No full dependency-sync backend suite was run in this workspace because the current CPython 3.14 environment conflicts with the locked `onnxruntime==1.20.1` wheel.
- No staging redeploy, GitHub Actions pass, external review, customer deployment, production audit persistence, or production telemetry integration is claimed.

## Next implementation step

Run the focused workflow in GitHub Actions on Python 3.11, then execute a staging-safe retrieval request with a seeded malicious retrieved chunk and capture sanitized request-path logs, audit event, telemetry counter, and returned-context evidence. Until that evidence exists, live enforcement/blocking/filtering remains NOT CLAIMED.
