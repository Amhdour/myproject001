# Oracle VPS Staging Foundation

## Purpose

Define the first infrastructure step for moving this repository from documentation/isolated security evidence toward a production-style staging environment on an Oracle VPS using open-source components.

## Scope

This step is planning and evidence preparation only. It does not claim production readiness, enterprise readiness, compliance certification, or runtime security-control effectiveness.

## Target Outcome

Create a reproducible Oracle VPS staging foundation that can later support:

- Docker Compose deployment
- HTTPS reverse proxy
- environment-specific secret injection
- database and vector-store services
- logs and metrics capture
- demo attack execution
- rollback evidence
- staging go/no-go review

## Recommended First Stack

| Area | Open-source component | Purpose |
|---|---|---|
| Deployment | Docker Compose | First live staging target before K3s |
| Reverse proxy | Caddy or Traefik | HTTPS entrypoint and routing |
| Database | PostgreSQL | Application state and audit data |
| Vector DB | Qdrant or Weaviate | RAG retrieval security tests |
| Metrics | Prometheus + Grafana | Service health and security telemetry |
| Logs | Loki + Grafana Alloy/Promtail | Centralized runtime logs |
| Identity | Keycloak | Tenant/user/role demo identity provider |
| Policy | Open Policy Agent | Policy-as-code checks and launch-gate decisions |
| Scanning | Trivy, Gitleaks, Semgrep | CI and deployment security checks |

## Oracle VPS Prerequisites

Record the following before deployment work begins:

- VPS provider: Oracle Cloud Infrastructure
- VPS shape: TBD
- Region: TBD
- Public IPv4: TBD / redacted before publication
- OS image: TBD
- SSH access method: TBD / redacted before publication
- Firewall/security-list rules: TBD
- Domain/subdomain: TBD
- TLS strategy: Caddy or Traefik automatic certificate management
- Secrets source: out-of-git `.env` or OCI Vault later
- Deployment user: non-root user preferred
- Backup target: TBD
- Rollback method: previous image/tag and database snapshot/backup

## Required Evidence Files

Create or update these evidence records during execution:

- `docs/security/evidence/oracle_vps_staging_foundation/prerequisite_check.md`
- `docs/security/evidence/oracle_vps_staging_foundation/vps_inventory.md`
- `docs/security/evidence/oracle_vps_staging_foundation/open_source_stack_decision.md`
- `docs/security/evidence/oracle_vps_staging_foundation/security_boundary_checklist.md`
- `docs/security/evidence/oracle_vps_staging_foundation/go_no_go.md`

## Step-by-Step Execution Order

1. Confirm branch and commit baseline.
2. Record Oracle VPS inventory without publishing secrets or raw IPs if the repo remains public.
3. Confirm SSH access and OS version.
4. Create non-root deployment user.
5. Enable host firewall.
6. Install Docker and Docker Compose plugin.
7. Create staging directory outside the git repo.
8. Prepare out-of-git environment file.
9. Add reverse proxy configuration.
10. Add database/vector/logging/metrics service plan.
11. Run local compose validation before public exposure.
12. Enable HTTPS only after service health checks pass.
13. Run security scans and collect outputs.
14. Execute smoke tests.
15. Execute demo attack tests when controls are wired.
16. Capture logs, metrics, and screenshots as evidence.
17. Record rollback procedure and test result.
18. Write staging go/no-go decision.

## Security Rules

- Do not commit private keys, tokens, passwords, raw `.env` files, database dumps, or live customer data.
- Do not publish the raw public IP in portfolio evidence unless intentionally accepted.
- Use synthetic users, tenants, documents, tools, and attack payloads only.
- Use least-privilege firewall rules.
- Keep runtime secrets outside the repository.
- Treat monitor-only controls as monitoring evidence only, not enforcement evidence.
- Do not claim production readiness until live enforcement, tests, CI, telemetry, rollback, and go/no-go evidence are complete.

## Initial Acceptance Criteria

This step is complete when:

- Oracle VPS staging prerequisites are documented.
- Open-source stack choice is recorded.
- Security boundary checklist is created.
- Required evidence templates exist.
- No secrets are committed.
- The result remains a planning/foundation step with no unsupported readiness claim.

## Staging Progress Impact

This foundation step can improve staging-package completeness after the VPS is reachable and evidence is complete.

This does not by itself activate live security enforcement.
