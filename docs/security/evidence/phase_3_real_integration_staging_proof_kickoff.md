# Phase 3 Real Integration & Staging Proof Kickoff

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T18:15:00Z |
| Branch name | `phase-3-real-integration-staging-proof-kickoff` |
| Base branch | `main` |
| Starting commit SHA | `10610a67f86055f478073e349ba8742e49bedd08` |
| Phase 2 completion | `PHASE_2_RUNTIME_SECURITY_PROOF_CHECKPOINT_COMPLETE` |

## Objective

Phase 3 moves from isolated/gated runtime-security proof toward real integration and staging proof.

This phase must remain evidence-first and safety-first. It should not claim production readiness or enterprise readiness unless future real implementation, tests, staging evidence, rollback evidence, and external validation prove those claims.

## Phase 3 mission

Build evidence that selected Phase 2 controls can be safely connected closer to real Onyx runtime paths using:

- feature flags;
- shadow mode first;
- explicit off-by-default behavior;
- focused integration tests;
- rollback/runbook documentation;
- staging evidence where available;
- no production/enterprise overclaiming.

## Phase 3 ordered plan

| Step | Name | Goal |
| --- | --- | --- |
| Step 40 | Integration safety gate | Define preconditions, flags, rollback, test targets, and forbidden claims before modifying live-adjacent code. |
| Step 41 | Real search-pipeline seam test | Add tests around the discovered post-`search_chunks` seam using mocks/stubs only. |
| Step 42 | Retrieval ACL feature flag config | Add off-by-default feature-flag plumbing for retrieval ACL integration. |
| Step 43 | Shadow-mode search-pipeline integration | Wire retrieval ACL shadow evaluation near the real search-pipeline seam without changing returned chunks. |
| Step 44 | Shadow-mode integration tests | Prove real-seam shadow mode records would-deny/filter evidence and preserves returned chunks. |
| Step 45 | Explicit enforce-mode test harness | Add test-only or gated enforce-mode harness proving unauthorized chunks are filtered only when explicitly enabled. |
| Step 46 | Rollback and runbook evidence | Document how to disable, roll back, and troubleshoot the integration. |
| Step 47 | Staging readiness checklist | Define environment, secrets, dependencies, commands, and evidence requirements for staging. |
| Step 48 | Minimal staging smoke proof | Run minimal staging/smoke proof if a real environment exists; otherwise document blocker honestly. |
| Step 49 | Phase 3 checkpoint | Summarize CI/integration/staging evidence and remaining NO-GO boundaries. |

## Step 40 scope

Step 40 should be the first Phase 3 implementation step. It should add an integration safety gate document and, if useful, a small config/design stub. It should not wire runtime behavior yet.

Step 40 must answer:

- which real seam is targeted first;
- what feature flag name is used;
- default mode;
- fallback behavior;
- rollback command/process;
- required tests before any merge;
- safe claims;
- forbidden claims.

## First target seam

Based on Phase 2 discovery, the first integration target remains:

```text
backend/onyx/context/search/pipeline.py::search_pipeline
after search_chunks(...)
before post-query censoring / return to callers
```

This remains a target only until a later step adds and proves real integration.

## Required safety rules

- Default behavior must remain off.
- Shadow mode must preserve returned chunks.
- Enforce mode must be explicitly gated.
- Any live-adjacent behavior change must be covered by tests.
- Any deny/filter action must produce evidence.
- Any failure mode must fail safe or preserve existing behavior depending on mode and documented expectations.
- Rollback must be documented before live-adjacent wiring.

## Safe Phase 3 claims

- Phase 3 is beginning real integration and staging proof work.
- Phase 3 is not production readiness.
- Phase 3 is not enterprise readiness.
- Phase 2 isolated runtime-security helpers are CI-backed.
- Future Phase 3 claims must depend on actual integration and staging evidence.

## Forbidden Phase 3 claims

Do not claim:

- production readiness;
- enterprise readiness;
- live retrieval enforcement;
- live agent/tool enforcement;
- live blocking/filtering;
- full Onyx staging;
- external validation;
- compliance certification;
- customer deployment readiness.

## Current readiness at Phase 3 start

| Area | Status |
| --- | --- |
| Production-style portfolio readiness | `99%` |
| Employable portfolio readiness | `99%` |
| Phase 2 runtime-security proof readiness | `90% portfolio-level` |
| Real integration readiness | `10-15%` |
| Staging proof readiness | `0-10%` |
| Production readiness | `0% / NO-GO` |
| Enterprise production-candidate | `0-7% / NO-GO` |

## Recommended next step

Start Step 40:

```text
Step 40 — Integration safety gate
```

Only after Step 40 should the repo move toward real seam tests, feature flags, and shadow-mode integration.
