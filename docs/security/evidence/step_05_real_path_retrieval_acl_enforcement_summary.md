# Step 05 Real-Path Retrieval ACL Enforcement Summary

## Result

Step 05 wires the Retrieval ACL Enforcement v1 hook into the real Onyx `search_pipeline` return seam behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE`.

## What changed

- The hook now runs after `censored_chunks` are produced by post-query censoring and before `search_pipeline` returns.
- `off` mode returns chunks unchanged through the existing no-op seam hook.
- `shadow` mode returns chunks unchanged and keeps the existing reviewer-safe observation behavior.
- `enforce` mode calls the Step 04 enforcement helper.
- Missing required ACL metadata remains fail-closed.
- Decision records avoid document content and use redacted document references.

## Known limitation

Real Onyx `InferenceChunk` tenant metadata mapping is incomplete in this slice. The enforce-mode real-path tests use fake chunk objects with explicit metadata and do not prove full real Onyx enforcement.

## Safe claim boundary

This is a portfolio technical-proof slice only.

Do not claim production readiness.
Do not claim enterprise readiness.
Do not claim staging validation.
Do not claim full Onyx-wide authorization coverage.
