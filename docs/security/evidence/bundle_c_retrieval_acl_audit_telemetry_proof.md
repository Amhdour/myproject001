# Bundle C Retrieval ACL Audit / Telemetry Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T17:18:00Z |
| Branch name | `bundle-c-retrieval-acl-audit-telemetry-proof` |
| Base branch | `main` |
| Starting commit SHA | `5a160e27473264d226c528795df11191ce976af7` |

## Objective

Bundle C adds structured retrieval ACL audit and telemetry proof for deny/filter decisions.

This bundle remains isolated. It does not wire telemetry into live Onyx runtime, production logging infrastructure, SIEM, observability stack, or external monitoring.

## Accelerated scope

Bundle C combines:

- Step 30 — Runtime ACL audit-log schema/proof;
- Step 31 — deny/filter telemetry proof;
- Step 32 — evidence artifact for retrieval decisions.

## Files added

```text
backend/security_layer/retrieval_acl/telemetry.py
backend/security_layer/tests/test_retrieval_acl_telemetry.py
scripts/portfolio/generate_retrieval_acl_telemetry_evidence.py
.github/workflows/retrieval-acl-telemetry-tests.yml
docs/security/evidence/bundle_c_retrieval_acl_audit_telemetry_proof.md
```

## Telemetry behavior

The telemetry proof:

- converts individual ACL decisions into structured decision telemetry records;
- summarizes in-memory audit events into deterministic counts;
- counts deny and filter decisions;
- counts denied chunks;
- aggregates denied document IDs;
- aggregates denial reasons;
- records request IDs;
- renders deterministic text evidence for CI artifacts;
- preserves `production_readiness=NO-GO`, `enterprise_readiness=NO-GO`, and `live_enforcement_claimed=false`.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_telemetry.py -q
```

## Evidence generation command

```bash
PYTHONPATH=. python scripts/portfolio/generate_retrieval_acl_telemetry_evidence.py
```

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-telemetry-tests.yml
```

Artifact name:

```text
retrieval-acl-telemetry-test-evidence
```

Artifact contents:

```text
retrieval-acl-telemetry-artifacts/environment_metadata.txt
retrieval-acl-telemetry-artifacts/test.log
retrieval-acl-telemetry-artifacts/telemetry_summary.txt
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_AUDIT_TELEMETRY_PROVEN_BY_CI
```

## What this proves

This proves that isolated retrieval ACL deny/filter decisions can produce structured, deterministic telemetry summaries and CI evidence artifacts.

## What this does not prove

This does **not** prove:

- live Onyx telemetry integration;
- production logging;
- SIEM integration;
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

- Bundle C provides isolated retrieval ACL audit/telemetry proof.
- Deny/filter decisions can be summarized into structured evidence.
- CI artifact evidence captures test output, environment metadata, and deterministic telemetry summary.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx telemetry integration.
- Do not claim production logging or SIEM integration.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim full tenant isolation.
- Do not claim complete RAG authorization.

## Recommended next bundle

Bundle D should add a tool authorization runtime helper, denial tests, and focused CI evidence gate for agent/tool calls.
