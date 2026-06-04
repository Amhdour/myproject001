# Step 40 Integration Safety Gate

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T18:25:00Z |
| Branch name | `step-40-integration-safety-gate` |
| Base branch | `main` |
| Starting commit SHA | `15061679480225d24c7d26375e5adbc7f0b98bca` |
| Phase 3 kickoff | `PHASE_3_REAL_INTEGRATION_STAGING_PROOF_KICKOFF_COMPLETE` |

## Objective

Step 40 defines the integration safety gate that must be satisfied before any Phase 3 live-adjacent runtime modification.

This step is documentation/evidence only. It does not modify runtime behavior, wire live enforcement, add staging proof, or claim production readiness.

## First target seam

The first live-adjacent integration target remains the retrieval pipeline seam discovered in Step 22:

```text
backend/onyx/context/search/pipeline.py::search_pipeline
after search_chunks(...)
before post-query censoring / return to callers
```

This seam is selected because retrieved chunks exist after `search_chunks(...)` and before downstream return/selection paths.

## Integration mode policy

Any future integration must support these modes:

| Mode | Default | Behavior |
| --- | --- | --- |
| `off` | Yes | Existing behavior preserved. No runtime filtering. No production claim. |
| `shadow` | Optional explicit enable | Record would-deny/would-filter evidence while preserving returned chunks. |
| `enforce` | Never default | Filter only when explicitly enabled by test/config gate and covered by integration tests. |

## Required feature flag

Future integration should use one explicit flag family:

```text
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce
```

Default must be:

```text
off
```

If the variable is missing, empty, malformed, or unsupported, the integration must preserve existing behavior or fail closed according to the documented mode contract. No malformed configuration may silently claim enforcement.

## Preconditions before touching live-adjacent code

Before modifying `backend/onyx/context/search/pipeline.py` or any real retrieval path, the repo must have:

1. Step 21 Retrieval ACL helper proven by CI.
2. Step 23 adapter proven by CI.
3. Bundle A shadow-mode wrapper proven by CI.
4. Bundle B isolated search-pipeline gate proven by CI.
5. Bundle C audit/telemetry proof proven by CI.
6. A targeted seam test plan.
7. Rollback instructions.
8. Claim-boundary checks passing.
9. No production/enterprise readiness claim.

## Required tests before any future integration merge

Future live-adjacent integration PRs must prove:

- default `off` mode preserves existing returned chunks;
- `shadow` mode preserves returned chunks but records would-deny/filter evidence;
- explicit `enforce` mode filters unauthorized chunks only when explicitly enabled;
- missing/malformed feature flag does not create accidental enforcement claims;
- cross-tenant unauthorized chunks cannot reach simulated downstream surfaces in enforce mode;
- audit/telemetry evidence is produced for deny/filter outcomes;
- existing focused security-layer tests remain green;
- claim-boundary and evidence checks remain green.

## Required rollback process

Any future integration must be reversible by:

1. setting `ONYX_SECURITY_RETRIEVAL_ACL_MODE=off`;
2. redeploying/restarting the affected runtime if necessary;
3. confirming returned-chunk behavior matches pre-integration baseline in `off` mode;
4. preserving logs/evidence showing rollback mode and command used;
5. reverting the integration PR if feature-flag rollback does not restore expected behavior.

## Required runbook content before staging proof

Before claiming staging proof, a future PR must document:

- environment name;
- commit SHA;
- feature flag value;
- test command or smoke command;
- expected returned-chunk behavior;
- evidence artifact path;
- rollback command;
- observed result;
- blocker status if staging cannot run.

## Failure handling policy

| Condition | Required behavior |
| --- | --- |
| Mode `off` | Preserve existing behavior. |
| Mode `shadow` | Preserve returned chunks; record evidence if possible. |
| Mode `enforce` | Filter only by proven helper path; if required ACL context is missing, deny/filter according to explicit tests. |
| Unknown mode | Treat as `off` or fail closed according to explicit future implementation docs; never claim enforcement. |
| Missing ACL metadata | Must be tested; no silent allow in enforce-mode proof. |
| Telemetry failure | Must not create production claim; behavior must be documented by mode. |

## Allowed Phase 3 implementation sequence

Future work should follow this order:

1. Step 41 — real search-pipeline seam tests with mocks/stubs only.
2. Step 42 — off-by-default feature flag config proof.
3. Step 43 — shadow-mode search-pipeline integration.
4. Step 44 — shadow-mode integration tests.
5. Step 45 — explicit enforce-mode test harness.
6. Step 46 — rollback and runbook evidence.
7. Step 47 — staging readiness checklist.
8. Step 48 — minimal staging smoke proof if real environment exists.
9. Step 49 — Phase 3 checkpoint.

## Step 40 safe claims

- Step 40 defines the Phase 3 integration safety gate.
- Step 40 identifies the first target seam and required feature-flag contract.
- Step 40 defines rollback, test, and runbook requirements before live-adjacent integration.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Step 40 forbidden claims

Do not claim:

- runtime code changed;
- live Onyx retrieval enforcement;
- live blocking/filtering;
- staging proof;
- production readiness;
- enterprise readiness;
- full backend test success;
- external validation;
- compliance certification.

## Acceptance criteria

- This file exists.
- It identifies the target seam.
- It defines the feature flag and default mode.
- It defines preconditions, required tests, rollback, and runbook requirements.
- It preserves NO-GO / PENDING / NOT CLAIMED boundaries.
- Claim-boundary checks pass.

## Completion classification after CI passes

```text
STEP_40_INTEGRATION_SAFETY_GATE_COMPLETE
```

## Recommended next step

Step 41 should add real search-pipeline seam tests using mocks/stubs only, without changing production runtime behavior.
