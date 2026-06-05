# Retrieval ACL Metadata Mapping Runbook

## Purpose

Describe how to verify the Step 06 metadata adapter boundary for Retrieval ACL Enforcement v1 without claiming full Onyx-wide authorization or staging validation.

## Configuration

- Off mode: `ONYX_SECURITY_RETRIEVAL_ACL_MODE=off`.
- Shadow mode: `ONYX_SECURITY_RETRIEVAL_ACL_MODE=shadow`.
- Enforce mode: `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.

Only enforce mode filters returned chunks. Off and shadow modes must preserve returned chunks.

## Verification Steps

1. Confirm adapter extraction uses real chunk-like fields:
   - `document_id` for a redacted document reference.
   - `tenant_id` only if present directly or in known metadata mappings.
   - `user_tenant_id` from the caller.
2. Confirm missing tenant metadata is recorded as `missing_chunk_tenant_id`.
3. Confirm enforce mode fails closed when required metadata is missing.
4. Confirm matching tenant metadata is allowed in enforce mode.
5. Confirm cross-tenant metadata is denied in enforce mode.
6. Confirm decision records do not include chunk text.
7. Confirm off and shadow modes preserve returned chunks.

## Required Commands

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py backend/onyx/context/search/pipeline.py
ruff check backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/retrieval_acl/metadata_adapter.py backend/security_layer/tests/test_retrieval_acl_enforce_hook.py
python scripts/portfolio/check_claim_boundary.py
```

## Failure Handling

- If tenant metadata is absent, do not derive or invent it from document IDs or request filters.
- Keep enforce mode behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
- Preserve off and shadow behavior while recording the metadata decision boundary.

## Readiness Boundary

- Production readiness: NO-GO.
- Enterprise readiness: NO-GO.
- Staging validation: not claimed.
