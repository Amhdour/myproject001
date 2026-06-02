# Oracle VPS Staging Foundation - Prerequisite Check

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-PREREQ
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: TBD
- Operator: AI Trust & Security Readiness Engineer
- Commit SHA: TBD
- Timestamp: TBD
- Redaction status: required before publication

## Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Repository branch created | `oracle-vps-staging-foundation` exists | TBD | pending |
| Baseline commit recorded | Source commit SHA recorded | TBD | pending |
| Oracle VPS available | VPS reachable by SSH | TBD | pending |
| OS identified | OS/version recorded | TBD | pending |
| Non-root user available | Deployment user created or planned | TBD | pending |
| Firewall baseline planned | SSH/HTTP/HTTPS rules documented | TBD | pending |
| Docker plan selected | Docker Compose selected for first staging | Docker Compose selected | complete |
| Secret handling defined | No secrets committed to git | Out-of-git `.env` planned | complete |
| Evidence redaction planned | Public evidence excludes sensitive values | TBD | pending |

## Notes

This prerequisite check is evidence preparation only. It does not prove runtime enforcement, deployment success, or production readiness.
