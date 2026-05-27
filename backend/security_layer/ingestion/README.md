# Isolated Secure Ingestion Controls (Step 15B)

This module contains **isolated** secure-ingestion helper controls under `backend/security_layer/ingestion/`.

## Scope
- No live ingestion integration.
- No runtime enforcement activation in production paths.
- No parser/chunker/embedder/vector DB integration.
- No production DB writes.
- No real malware scanner (placeholder only).
- No real DLP scanner (placeholder only).

## Supported checks
- Tenant context present
- Subject context present
- Source metadata safe and non-secret
- ACL snapshot present and non-stale
- Content-type allowlist validation
- File size and file count policy checks
- Provenance required for vector-write authorization
- Prompt-injection marker detection (short text sample)
- Poisoning marker detection (short text sample)
- In-memory audit/finding/metric emission

## Test command
`PYTHONPATH=. python -m pytest backend/security_layer/tests -q`

## Non-claim
This implementation does not claim end-to-end ingestion security enforcement. It is an isolated helper control layer only.
