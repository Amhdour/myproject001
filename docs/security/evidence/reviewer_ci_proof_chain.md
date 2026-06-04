# Reviewer CI Proof Chain

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T14:12:00Z |
| Branch name | `step-11-reviewer-evidence-proof-chain-v2` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `22d5a99102080fd67869065ff435819f898d3863` |

## Purpose

This file gives reviewers one concise proof chain for the recent CI-backed portfolio evidence steps.

It links the CI-backed recovery and execution evidence from Steps 07 through 10 without expanding the claim boundary.

## Claim boundary

This proof chain supports only portfolio-review claims.

It does not prove:

- production readiness;
- enterprise readiness;
- live enforcement;
- live blocking;
- live filtering;
- full Onyx staging;
- external validation;
- compliance certification;
- full backend test success;
- customer deployment readiness.

## Proof chain summary

| Step | Evidence | CI classification | Safe claim |
| --- | --- | --- | --- |
| Step 07 | Backend unit-test collection recovery after `SearchSettings` annotation fix | `TEST_COLLECTION_RECOVERED_BY_CI` | Backend unit-test collection passes in CI after the targeted import/annotation fix. |
| Step 08 | Isolated security-layer test execution with artifact upload | `SECURITY_LAYER_TEST_EXECUTION_PROVEN_BY_CI` | Isolated security-layer helper tests execute and pass in CI. |
| Step 09 | Narrow backend unit-test subset execution with artifact upload | `BACKEND_UNIT_SUBSET_TEST_EXECUTION_PROVEN_BY_CI` | Selected LLM secret-scrubbing backend unit tests execute and pass in CI. |
| Step 10 | Deterministic synthetic demo attack runner with artifact upload | `DEMO_ATTACK_RUNNER_PROVEN_BY_CI` | Synthetic demo attack runner executes and passes in CI. |

## Step 07 — backend collection recovery

### Evidence file

```text
docs/security/evidence/step_07_searchsettings_runtime_annotation_fix.md
```

### What was proven

The Python Backend Test Collection workflow recovered after the runtime annotation issue in `backend/onyx/context/search/models.py` was fixed with:

```python
from __future__ import annotations
```

### Safe classification

```text
TEST_COLLECTION_RECOVERED_BY_CI
```

### Boundary

This is collection proof only. It is not full backend test execution proof.

## Step 08 — isolated security-layer test execution

### Evidence file

```text
docs/security/evidence/step_08_security_layer_test_execution_gate.md
```

### Workflow

```text
.github/workflows/security-layer-tests.yml
```

### Artifact

```text
isolated-security-layer-test-evidence
```

### Safe classification

```text
SECURITY_LAYER_TEST_EXECUTION_PROVEN_BY_CI
```

### Boundary

This proves isolated helper behavior covered by `backend/security_layer/tests` only. It does not prove live production enforcement.

## Step 09 — backend unit subset execution

### Evidence file

```text
docs/security/evidence/step_09_backend_unit_subset_test_gate.md
```

### Workflow

```text
.github/workflows/backend-unit-subset-tests.yml
```

### Selected test subset

```text
backend/tests/unit/onyx/llm/test_llm_utils_scrub.py
```

### Artifact

```text
backend-unit-subset-test-evidence
```

### Safe classification

```text
BACKEND_UNIT_SUBSET_TEST_EXECUTION_PROVEN_BY_CI
```

### Boundary

This proves only the selected LLM credential/secret-scrubbing unit-test subset.

## Step 10 — demo attack runner execution

### Evidence file

```text
docs/security/evidence/step_10_demo_attack_execution_gate.md
```

### Workflow

```text
.github/workflows/demo-attack-runner.yml
```

### Runner

```text
demo_attacks/run_demo_attacks.py
```

### Artifact

```text
demo-attack-runner-evidence
```

### Safe classification

```text
DEMO_ATTACK_RUNNER_PROVEN_BY_CI
```

### Boundary

This proves deterministic synthetic demo attack execution only. It does not prove production protection, live blocking, live filtering, live enforcement, external validation, or compliance.

## Reviewer checklist

- [ ] Confirm Step 07 evidence states collection recovery only.
- [ ] Confirm Step 08 artifact exists for isolated security-layer tests.
- [ ] Confirm Step 09 artifact exists for the selected backend unit subset.
- [ ] Confirm Step 10 artifact exists for synthetic demo attacks.
- [ ] Confirm no file claims production readiness.
- [ ] Confirm no file claims enterprise readiness.
- [ ] Confirm no file claims compliance certification.
- [ ] Confirm no file claims full Onyx staging or live enforcement.

## Recommended reviewer-safe summary

```text
This repository now includes CI-backed evidence that backend unit-test collection recovers, isolated security-layer helper tests pass, a selected backend secret-scrubbing unit-test subset passes, and a deterministic synthetic demo attack runner executes. These are production-style portfolio proofs only and do not establish production readiness or enterprise readiness.
```

## Next step

Step 12 should add a public reviewer navigation update that points reviewers from the portfolio package to this CI proof chain, while preserving all NO-GO production and enterprise boundaries.
