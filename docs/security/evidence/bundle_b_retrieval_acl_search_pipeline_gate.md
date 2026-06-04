# Bundle B Retrieval ACL Search-Pipeline Gate Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T17:05:00Z |
| Branch name | `bundle-b-retrieval-acl-search-pipeline-gate` |
| Base branch | `main` |
| Starting commit SHA | `82a2f1e5b81a173b187497e804199773cad40952` |

## Objective

Bundle B adds an isolated feature-flagged search-pipeline gate proof around the post-`search_chunks` integration point discovered in Step 22.

This bundle proves gated behavior with Onyx-like retrieved chunks and mocked downstream surfaces. It does not modify live Onyx `search_pipeline` behavior.

## Accelerated scope

Bundle B combines:

- Step 27 — search-pipeline feature-flag integration design;
- Step 28 — mocked `search_chunks` integration tests;
- Step 29 — downstream leakage tests.

## Files added

```text
backend/security_layer/retrieval_acl/search_pipeline_gate.py
backend/security_layer/tests/test_retrieval_acl_search_pipeline_gate.py
.github/workflows/retrieval-acl-search-pipeline-gate-tests.yml
docs/security/evidence/bundle_b_retrieval_acl_search_pipeline_gate.md
```

## Gate behavior

The isolated gate supports three modes:

```text
off
shadow
enforce
```

### `off`

Returns retrieved chunks unchanged and records no ACL decision.

### `shadow`

Returns retrieved chunks unchanged, but records what ACL would allow, deny, or filter.

### `enforce`

Returns only ACL-allowed chunks in the isolated proof path, proving that unauthorized chunks can be removed before simulated downstream surfaces.

## Simulated downstream surfaces

The tests simulate document IDs visible to downstream surfaces after the gate. This represents a simplified proof target for later real integration work around:

- recombination;
- UI document emission;
- LLM section selection;
- LLM-facing context construction.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_search_pipeline_gate.py -q
```

## Focused tests

The Bundle B tests cover:

- gate `off` mode returns all chunks and records no ACL decision;
- gate `shadow` mode records would-filter evidence but preserves downstream chunks;
- gate `enforce` mode filters unauthorized chunks before simulated downstream surfaces;
- gate `enforce` mode denies all chunks when requester context is missing;
- invalid gate mode is rejected.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-search-pipeline-gate-tests.yml
```

Artifact name:

```text
retrieval-acl-search-pipeline-gate-test-evidence
```

Artifact contents:

```text
retrieval-acl-search-pipeline-gate-artifacts/environment_metadata.txt
retrieval-acl-search-pipeline-gate-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SEARCH_PIPELINE_GATED_PROOF_BY_CI
```

## What this proves

This proves an isolated, feature-flagged gate design for the post-`search_chunks` retrieval boundary.

It proves that unauthorized chunks can be filtered before simulated downstream document visibility when `mode="enforce"` is explicitly selected.

## What this does not prove

This does **not** prove:

- live Onyx `search_pipeline` integration;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- full tenant isolation;
- complete RAG authorization;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle B provides an isolated feature-flagged search-pipeline gate proof.
- `off`, `shadow`, and explicit isolated `enforce` modes are tested.
- Enforce mode filters unauthorized chunks before simulated downstream surfaces.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx `search_pipeline` integration.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim full tenant isolation.
- Do not claim complete RAG authorization.

## Recommended next bundle

Bundle C should add stronger runtime audit/telemetry proof for retrieval ACL decisions, including structured deny/filter telemetry and evidence artifacts that summarize decision counts and reasons.
