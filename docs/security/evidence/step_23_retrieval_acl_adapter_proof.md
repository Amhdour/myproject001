# Step 23 Retrieval ACL Adapter Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T16:35:00Z |
| Branch name | `step-23-retrieval-acl-adapter-proof` |
| Base branch | `main` |
| Starting commit SHA | `0e711976992f247bef4962172876e09e99b7eff1` |

## Objective

Step 23 adds an isolated adapter proof that converts Onyx-like retrieved chunks plus ACL metadata into the Step 21 Retrieval ACL helper model.

This step does not wire into live Onyx retrieval paths. It proves only that an adapter shape can map retrieved chunk metadata into the isolated runtime ACL helper and preserve allowed original chunks after filtering.

## Files added

```text
backend/security_layer/retrieval_acl/adapter.py
backend/security_layer/tests/test_retrieval_acl_adapter.py
.github/workflows/retrieval-acl-adapter-tests.yml
docs/security/evidence/step_23_retrieval_acl_adapter_proof.md
```

## Adapter proof behavior

The adapter proof:

- defines a small `OnyxLikeRetrievalChunk` test double for retrieved chunk shape;
- maps chunk ID, document ID, tenant metadata, subject ACL metadata, and group ACL metadata into the Step 21 `RetrievalResultChunk` model;
- calls the existing Step 21 `enforce_retrieval_acl(...)` helper;
- maps allowed decisions back to original Onyx-like chunks;
- fails closed when required ACL metadata is missing or malformed;
- records audit events through the existing Step 21 audit sink when decisions deny or filter.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_adapter.py -q
```

## Focused tests

The Step 23 tests cover:

- adapter mapping from Onyx-like chunk to Step 21 helper chunk;
- allowed chunk returns the original retrieved object;
- mixed results are filtered and audited;
- missing ACL metadata fails closed;
- missing requester context fails closed;
- document ACL subject/group mismatch denies.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-adapter-tests.yml
```

Artifact name:

```text
retrieval-acl-adapter-test-evidence
```

Artifact contents:

```text
retrieval-acl-adapter-artifacts/environment_metadata.txt
retrieval-acl-adapter-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_ADAPTER_PROVEN_BY_CI
```

## What this proves

This proves an isolated adapter path from Onyx-like retrieved chunks to the Step 21 retrieval ACL helper model.

It proves that allowed original chunks can be preserved after ACL enforcement and denied chunks can be filtered before downstream use in the isolated test environment.

## What this does not prove

This does **not** prove:

- live Onyx retrieval enforcement;
- production retrieval security;
- enterprise readiness;
- full tenant isolation;
- complete RAG authorization;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Step 23 provides an isolated adapter proof for Onyx-like retrieval chunks.
- The adapter can map metadata into the Step 21 helper and preserve allowed original chunks.
- The adapter fails closed for missing ACL metadata and missing requester context.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim the adapter is wired into `search_pipeline`.
- Do not claim live Onyx retrieval enforcement.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live tenant isolation.
- Do not claim complete RAG authorization.

## Recommended Step 24

Step 24 should add a shadow-mode wrapper design for the post-`search_chunks` integration point discovered in Step 22. It should still avoid changing live behavior unless explicitly gated and proven by tests.
