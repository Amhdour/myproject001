# Bundle A Retrieval ACL Shadow-Mode Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T16:55:00Z |
| Branch name | `bundle-a-retrieval-acl-shadow-mode-proof` |
| Base branch | `main` |
| Starting commit SHA | `b1402c179e012693da04844198422eab7f11a6c2` |

## Objective

Bundle A combines the accelerated Phase 2 retrieval ACL shadow-mode proof work:

- Step 24 — Retrieval ACL shadow-mode wrapper proof;
- Step 25 — Shadow-mode CI artifact gate;
- Step 26 — Runtime decision/audit evidence.

This bundle remains isolated and does not wire into live Onyx retrieval paths.

## Files added

```text
backend/security_layer/retrieval_acl/shadow_mode.py
backend/security_layer/tests/test_retrieval_acl_shadow_mode.py
.github/workflows/retrieval-acl-shadow-mode-tests.yml
docs/security/evidence/bundle_a_retrieval_acl_shadow_mode_proof.md
```

## Shadow-mode behavior

The shadow-mode wrapper:

- accepts Onyx-like retrieved chunks and requester ACL context;
- calls the Step 23 adapter and Step 21 retrieval ACL helper;
- records what the ACL decision would allow, deny, or filter;
- returns original chunks unchanged when `mode="shadow"`;
- filters returned chunks only when `mode="enforce"` is explicitly selected in the isolated helper;
- creates reviewer-safe decision evidence with denied document IDs, denied reasons, observed count, would-return count, and returned count;
- preserves `production_readiness=NO-GO`, `enterprise_readiness=NO-GO`, and `live_enforcement_claimed=false` in evidence.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_shadow_mode.py -q
```

## Focused tests

The Bundle A tests cover:

- shadow mode preserves original chunks while recording filter decisions;
- shadow mode allows all chunks when ACL decision allows;
- shadow mode records deny decisions without changing returned chunks;
- explicit isolated enforce mode filters returned chunks;
- missing ACL context fails closed while preserving shadow-mode return behavior;
- invalid mode is rejected.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-shadow-mode-tests.yml
```

Artifact name:

```text
retrieval-acl-shadow-mode-test-evidence
```

Artifact contents:

```text
retrieval-acl-shadow-mode-artifacts/environment_metadata.txt
retrieval-acl-shadow-mode-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SHADOW_MODE_PROVEN_BY_CI
```

## What this proves

This proves an isolated shadow-mode wrapper can observe retrieval ACL decisions, record deny/filter evidence, preserve original returned chunks in shadow mode, and explicitly filter only in isolated enforce mode.

## What this does not prove

This does **not** prove:

- live Onyx retrieval enforcement;
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

- Bundle A provides an isolated Retrieval ACL shadow-mode proof.
- Shadow mode records what would be denied or filtered without changing returned chunks.
- Explicit isolated enforce mode can filter returned chunks in tests.
- CI artifact evidence captures test output and environment metadata.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx retrieval enforcement.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim full tenant isolation.
- Do not claim complete RAG authorization.

## Recommended next bundle

Bundle B should add a gated search-pipeline integration proof with mocked `search_chunks`, proving unauthorized chunks cannot reach downstream recombination/UI/LLM-context surfaces when a feature flag is explicitly enabled.
