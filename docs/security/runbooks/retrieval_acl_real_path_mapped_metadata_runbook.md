# Retrieval ACL Real-Path Mapped Metadata Runbook

## Purpose

Use this runbook to reproduce the Step 07 mapped-metadata real-path enforcement evidence for Retrieval ACL Enforcement v1.

This runbook does not claim production readiness, enterprise readiness, staging validation, compliance certification, or full Onyx-wide authorization coverage.

## Preconditions

- Work from the Step 07 branch: `step-07-real-path-enforce-with-mapped-metadata`.
- Use the repository root as the working directory.
- If Python dependencies are missing, activate the project virtual environment first:

```bash
source .venv/bin/activate
```

## Test command

Run the focused Step 07 proof:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
```

## Expected behavior

The focused test file should pass and demonstrate:

- matching tenant metadata is allowed in enforce mode;
- cross-tenant mapped metadata is blocked in enforce mode;
- missing chunk tenant metadata fails closed in enforce mode;
- missing caller tenant metadata fails closed in enforce mode;
- off mode returns chunks unchanged;
- shadow mode returns chunks unchanged while recording a denial decision;
- decision records do not contain chunk text.

## Environment gate

Enforce behavior is gated behind:

```bash
ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce
```

Do not treat off or shadow mode observations as enforce-mode blocking behavior. Off mode and shadow mode intentionally preserve returned chunks.

## Evidence files

- `backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py`
- `docs/security/evidence/step_07_real_path_enforce_mapped_metadata.md`
- `docs/security/evidence/step_07_real_path_enforce_mapped_metadata_summary.md`

## Known limitation

Real `InferenceChunk` tenant metadata remains incomplete as a guarantee. The evidence relies on mapped metadata when `metadata["tenant_id"]` or equivalent tenant metadata is present, and fails closed when chunk tenant metadata is missing. The test slice does not invent metadata that the retrieval model does not guarantee.

## Claim boundary

- Production readiness: `NO-GO`.
- Enterprise readiness: `NO-GO`.
- Staging validation: not claimed.
- Full Onyx-wide authorization: not claimed.
