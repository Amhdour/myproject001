# Oracle VPS Staging Foundation - Security Boundary Checklist

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-BOUNDARY
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Redaction status: required before publication

## Boundary Checklist

| Boundary area | Required control | Evidence target | Status |
|---|---|---|---|
| Network exposure | Only SSH, HTTP, and HTTPS intentionally exposed | firewall/security-list notes | pending |
| SSH access | Key-based access preferred; password login disabled if possible | SSH config evidence, redacted | pending |
| Deployment user | Non-root user used for deployment | user/group evidence, redacted | pending |
| Secrets | Secrets kept outside git | `.env` location note, redacted | pending |
| TLS | HTTPS enabled through Caddy/Traefik | certificate/routing evidence | pending |
| Database | Database not publicly exposed | compose/network evidence | pending |
| Vector DB | Vector DB not publicly exposed unless intentionally protected | compose/network evidence | pending |
| Logs | Logs centralized and redacted | Loki/Grafana evidence | pending |
| Metrics | Metrics collected without leaking secrets | Prometheus/Grafana evidence | pending |
| Backups | Backup/restore path documented | backup evidence | pending |
| Rollback | Previous release rollback documented and tested | rollback evidence | pending |
| Demo data | Synthetic data only | seeded demo evidence | pending |
| Attack tests | Prompt-injection/retrieval/tool abuse tests executed only against staging | test evidence | pending |
| Readiness claim | No production-readiness claim before go/no-go evidence | go/no-go record | pending |

## Minimum Pass Rule

This step can pass only if:

- secrets are not committed
- SSH access is controlled
- public exposure is intentionally documented
- database/vector services are not directly exposed to the internet
- evidence is redacted before publication

## Notes

This checklist defines staging security boundaries only. It does not prove enterprise production readiness.
