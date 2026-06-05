# Bundle H Retrieval ACL Live-Adjacent Seam Instrumentation Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-h-live-adjacent-seam-instrumentation` |
| Base branch | `main` |
| Bundle G dependency | `RETRIEVAL_ACL_ENFORCE_HARNESS_ROLLBACK_PROVEN_BY_CI` |

## Objective

Bundle H adds default-off live-adjacent retrieval seam observation proof.

It proves a seam-observation helper can record retrieval ACL observations while preserving behavior in `off` and `shadow` modes.

It does not modify live Onyx `search_pipeline` behavior.

## Scope

Bundle H includes:

- default-off live-adjacent seam observation helper;
- focused seam-observation tests;
- focused CI workflow;
- evidence documentation.

## Files added

```text
backend/security_layer/retrieval_acl/live_adjacent_seam.py
backend/security_layer/tests/test_retrieval_acl_live_adjacent_seam.py
.github/workflows/retrieval-acl-live-adjacent-seam-tests.yml
docs/security/evidence/bundle_h_retrieval_acl_live_adjacent_seam_proof.md
```

## Feature flag contract

```text
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce
```

Default behavior:

```text
off
```

Unsupported, empty, or missing values resolve to:

```text
off
```

## Seam observation behavior

The live-adjacent seam observation helper:

- accepts a named seam such as `post_search_chunks_pre_llm_context`;
- observes input chunk count and document IDs;
- records returned chunk count and returned document IDs;
- records whether behavior changed;
- proves `off` mode preserves chunks;
- proves `shadow` mode preserves chunks while recording would-filter evidence;
- proves explicit `enforce` behavior remains isolated and does not claim live enforcement;
- preserves `NO-GO` production and enterprise readiness boundaries.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_live_adjacent_seam.py -q
```

## Focused tests

The Bundle H tests cover:

- default-off seam observation preserves chunks;
- shadow seam observation records would-filter evidence without behavior change;
- explicit enforce remains isolated and records behavior change;
- invalid env values fail safe to off.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-live-adjacent-seam-tests.yml
```

Artifact name:

```text
retrieval-acl-live-adjacent-seam-test-evidence
```

Artifact contents:

```text
retrieval-acl-live-adjacent-seam-artifacts/environment_metadata.txt
retrieval-acl-live-adjacent-seam-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_LIVE_ADJACENT_SEAM_OBSERVATION_PROVEN_BY_CI
```

## What this proves

This proves default-off live-adjacent seam observation behavior for an isolated retrieval ACL helper.

## What this does not prove

This does **not** prove:

- live Onyx `search_pipeline` integration;
- live Onyx retrieval enforcement;
- live Onyx runtime instrumentation;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle H provides default-off live-adjacent retrieval seam observation proof.
- Bundle H proves `off` and `shadow` modes preserve chunk behavior in the isolated helper path.
- Bundle H proves explicit enforce behavior remains isolated and claim-bounded.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx `search_pipeline` integration.
- Do not claim live Onyx retrieval enforcement.
- Do not claim live Onyx runtime instrumentation.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.

## Recommended next bundle

Bundle I should identify the real Onyx retrieval seam file/function and add documentation plus tests that prove the seam location is stable before any live patch is attempted.
