# Control Summary

## Control name

Step 63X bounded runtime retrieval ACL proof

## Threat addressed

Cross-tenant retrieval leakage where a retrieved chunk from one tenant reaches another tenant's answer context.

## Runtime location

The live retrieval path already calls the runtime enforcement adapter from `backend/onyx/context/search/retrieval/search_runner.py` after retrieval candidates are produced and after the existing retrieval guard result handling.

## Security invariant

A retrieved chunk should not remain eligible for answer context when its `tenant_id` does not match the acting request tenant.

## Modes

- `disabled`: preserve existing retrieval behavior and emit no Step 63X telemetry.
- `monitor_only`: record deny decision evidence but do not block returned chunks.
- `enforce`: remove unauthorized chunks from the returned chunk set.

## Step 63X change

Step 63X adds a dedicated telemetry helper for runtime retrieval ACL decisions and a focused proof package around the existing runtime retrieval enforcement adapter.

## Evidence boundary

This proves the bounded helper behavior and the existing patched retrieval hook location. It does not prove full Onyx-wide enforcement, every retrieval variant, every connector path, or production deployment.
