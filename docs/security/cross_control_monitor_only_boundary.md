# Cross-Control Monitor-Only Boundary

## Current Monitor-Only Boundaries
- Live monitor-only applies only to retrieval hook telemetry path.
- All other control families remain isolated/non-live.

## Retrieval Monitor-Only Hook Boundary
- Executes after retrieval guard result handling.
- Must preserve response payload, ranking, and access behavior.
- Must fail-open on telemetry errors.

## Future Monitor-Only Candidate Boundaries
- vector DB candidate: observe query metadata outcomes only.
- cache candidate: observe key/tenant metadata outcomes only.
- tool authorization candidate: observe allow/deny intent only.
- MCP candidate: observe request/credential posture signals only.
- artifact safety candidate: observe scan/classification signals only.
- secure ingestion candidate: observe ingest posture events only.
- shared sink candidate: aggregate audit/finding/metric telemetry only.

## Forbidden Monitor-Only Behavior
- blocking requests
- filtering documents/results
- mutating retrieval/vector/cache/tool/MCP/artifact outputs
- changing user-visible responses

## Allowed Monitor-Only Telemetry Behavior
- emit structured events
- increment counters/histograms
- capture non-sensitive summaries
- attach correlation IDs

## Fail-Open Expectations
Telemetry failure must not interrupt request execution.

## No-Blocking Expectations
No code path may deny or block operations in monitor-only mode.

## No-Filtering Expectations
No code path may remove, reorder, or rewrite payloads in monitor-only mode.

## Evidence Required Before Expanding Monitor-Only
- mode flag design and defaults
- isolated validation tests
- non-regression behavior tests
- rollback procedure evidence
- telemetry sink reliability evidence

## Rollback Requirements
- single-flag disable path
- documented owner and runbook
- verified fail-open fallback

## Known Limitations
- remote/main verification may be unavailable.
- production-like telemetry sink evidence absent.
- shadow-deny and enforce remain blocked.

## Candidate List
1. retrieval monitor-only continuation
2. vector DB future monitor-only candidate
3. cache future monitor-only candidate
4. tool authorization future monitor-only candidate
5. MCP future monitor-only candidate
6. artifact safety future monitor-only candidate
7. secure ingestion future monitor-only candidate
8. shared audit/finding/metric sink future candidate
