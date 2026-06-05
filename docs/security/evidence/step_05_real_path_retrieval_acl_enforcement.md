# Step 05 Real-Path Retrieval ACL Enforcement Evidence

## Objective

Wire the Step 04 Retrieval ACL Enforcement v1 hook into the real Onyx search pipeline behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE` as a portfolio technical-proof slice.

This step proves a real search-pipeline return seam can call the hook safely while preserving `off` and `shadow` behavior. It does not claim production readiness, enterprise readiness, staging validation, or full Onyx-wide authorization coverage.

## Files changed

- `backend/onyx/context/search/pipeline.py`
- `backend/security_layer/retrieval_acl/enforce_hook.py`
- `backend/security_layer/tests/test_retrieval_acl_enforce_hook.py`
- `backend/security_layer/tests/test_retrieval_acl_search_pipeline_seam.py`
- `backend/security_layer/tests/test_retrieval_acl_real_seam_identification.py`
- `backend/security_layer/tests/test_retrieval_acl_real_search_pipeline_noop_hook.py`
- `docs/security/evidence/step_05_real_path_retrieval_acl_enforcement.md`
- `docs/security/evidence/step_05_real_path_retrieval_acl_enforcement_summary.md`
- `docs/security/runbooks/retrieval_acl_real_path_enforcement_runbook.md`

## Exact hook location

The real-path hook is located in `backend/onyx/context/search/pipeline.py` after post-query censoring produces `censored_chunks` and before `search_pipeline` returns chunks.

Code path:

1. `search_pipeline(...)`
2. `retrieved_chunks = search_chunks(...)`
3. post-query censoring via `fetch_ee_implementation_or_noop(...)(chunks=retrieved_chunks, user=user)`
4. `return apply_retrieval_acl_real_path_enforcement_hook(chunks=censored_chunks, user_tenant_id=get_current_tenant_id() if MULTI_TENANT else None)`

## Mode behavior

- `off`: delegates to the existing no-op seam hook and returns the same chunk list unchanged.
- `shadow`: delegates to the existing no-op seam hook, returns the same chunk list unchanged, and preserves the current reviewer-safe shadow observation behavior.
- `enforce`: calls Retrieval ACL Enforcement v1 and returns only allowed chunks.

## Required metadata and fail-closed behavior

The enforcement helper requires:

- caller tenant ID;
- chunk tenant ID;
- chunk document ID.

If any required metadata is missing, the helper fails closed with `missing_acl_metadata` and returns no chunk for that decision.

## Real InferenceChunk tenant metadata limitation

The real pipeline now has a call path to the enforcement hook, but real Onyx `InferenceChunk` tenant metadata mapping is incomplete in this slice. The tests use fake chunk objects with explicit `tenant_id` and `document_id` fields to prove the hook behavior when metadata is available.

Because real `InferenceChunk` tenant metadata is not fully mapped here, this evidence does not claim full real Onyx enforcement.

## Content leakage boundary

Decision records do not include chunk content. Document identifiers are represented through a redacted document reference only.

## Exact test commands and results

- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q`
  - Result: PASS, `10 passed`.
  - Note: pytest emitted local warnings about a `cryptography` warning filter import in this Python environment.
- `PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q`
  - Result: PASS, `5 passed`.
  - Note: pytest emitted local warnings about a `cryptography` warning filter import in this Python environment.
- `PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/enforce_hook.py backend/onyx/context/search/pipeline.py`
  - Result: PASS.
- `ruff check backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/tests/test_retrieval_acl_enforce_hook.py`
  - Result: PASS.
- `python scripts/portfolio/check_claim_boundary.py`
  - Result: PASS, claim-boundary check found no unsafe positive readiness claims across 949 reviewer-facing files.

## Safe claims

- This is a portfolio technical-proof slice.
- The real search pipeline now calls a safe wrapper after post-query censoring and before returning chunks.
- `off` mode preserves existing chunk-return behavior.
- `shadow` mode preserves existing chunk-return behavior and current shadow observation behavior.
- `enforce` mode has a real call path and fail-closed helper behavior when required metadata is missing.
- The current tests prove the enforcement hook with fake chunks carrying explicit metadata.

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- compliance certification;
- staging validation;
- full Onyx-wide authorization coverage;
- full real Onyx enforcement;
- full tenant metadata mapping for real `InferenceChunk` objects.

## Next step

Map real `InferenceChunk` tenant metadata from trusted Onyx retrieval/index metadata, then add an integration-level test that exercises real search results without leaking document content into decision records.

## Readiness update

- Production-style portfolio coverage: remains about `99%` as a reviewer artifact only.
- Production readiness: `NO-GO`.
- Enterprise production-candidate readiness: `NO-GO / 7–9%`.
- External validation: pending.
- Staging validation for this step: not claimed.
