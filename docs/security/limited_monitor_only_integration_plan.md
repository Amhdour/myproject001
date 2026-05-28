# Limited Monitor-Only Integration Plan

## Issues to Address

Step 27X adds a limited, isolated monitor-only integration bundle without broad live hooks. The bundle reviews eight monitor-only candidates and selects two low-risk helpers:

1. `LMO-002 shared audit/finding/metric sink consolidation`
2. `LMO-004 cache monitor-only dry-run adapter`

## Important Notes

- No new live hook is added.
- Feature flags default to disabled.
- Runtime modes are limited to `disabled` and `monitor_only`.
- Helpers must not block, filter, reorder, mutate payloads, or alter original return values.
- The implementation is not a production-readiness claim.

## Candidate Review Summary

| Candidate | Summary | Step 27X Decision |
|---|---|---|
| LMO-001 | retrieval live ACL check | not selected |
| LMO-002 | shared audit/finding/metric sink consolidation | selected |
| LMO-003 | policy decision summary | not selected |
| LMO-004 | cache monitor-only dry-run adapter | selected |
| LMO-005 | tool invocation summary | not selected |
| LMO-006 | artifact release summary | not selected |
| LMO-007 | ingestion metadata summary | not selected |
| LMO-008 | MCP request summary | not selected |

## Implementation Strategy

- Add `backend/security_layer/monitor_only/` as an isolated helper package.
- Add shared dataclasses and candidate inventory in `models.py`.
- Add disabled-by-default flags in `feature_flags.py`.
- Add a shared in-memory runtime sink consolidator in `shared_sink.py`.
- Add a cache dry-run adapter in `cache_adapter.py` that records observations and preserves the original return value.

## Tests

- Focused unit tests cover models, feature flags, shared sink, and cache adapter behavior.
- Full `backend/security_layer/tests` is run to verify no security-layer regression.

## No-Readiness-Claim Statement

This plan describes limited monitor-only helper scaffolding and evidence. It does not claim production readiness, control effectiveness, or approval to enable enforcement.
