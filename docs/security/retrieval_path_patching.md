# Retrieval Path Patching (Step 17A)

## Purpose / Scope / Status
Design-only documentation for retrieval path patching. No runtime wiring is included in Step 17A.

## Non-Claim
This step does **not** enable live retrieval enforcement.

## Rollout Modes
- Observe-only
- Enforce-deny

## Expectations
- Fail-closed behavior for indeterminate patch decisions
- Safe-denial behavior for disallowed retrieval paths

## Feature Flag and Rollback
Future implementation must include explicit flag gating and rollback controls.

## Patch Candidate Catalog
RPC-001, RPC-002, RPC-003, RPC-004, RPC-005, RPC-006, RPC-007, RPC-008, RPC-009, RPC-010, RPC-011, RPC-012, RPC-013, RPC-014, RPC-015, RPC-016, RPC-017.
