# Oracle VPS Staging Foundation - Open-source Stack Decision

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-STACK
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Redaction status: public-safe after review

## Decision

Use Docker Compose before K3s for the first Oracle VPS staging foundation.

## Selected Stack

| Capability | Selected component | Decision status | Reason |
|---|---|---|---|
| Container orchestration | Docker Compose | selected | Lowest-complexity first staging target |
| HTTPS reverse proxy | Caddy or Traefik | pending final selection | Automatic TLS and simple routing |
| Database | PostgreSQL | selected | Common production-style relational backend |
| Vector database | Qdrant or Weaviate | pending final selection | RAG retrieval security testing |
| Metrics | Prometheus + Grafana | selected | Open-source observability baseline |
| Logs | Loki + Grafana Alloy/Promtail | selected | Centralized log evidence |
| Identity provider | Keycloak | planned | User/tenant/role authorization demos |
| Policy engine | Open Policy Agent | planned | Policy-as-code enforcement and launch gates |
| Security scans | Trivy, Gitleaks, Semgrep | selected | Supply-chain and secret scanning evidence |
| CI | GitHub Actions | selected | Repeatable validation and evidence generation |

## Deferred Stack

| Component | Deferred until | Reason |
|---|---|---|
| K3s | After Docker Compose staging passes | Avoid premature Kubernetes complexity |
| Rancher | After K3s is stable | Enterprise-style management layer only after stable cluster |
| OCI Vault | After basic secret flow is proven | Useful later, but not required for first compose staging |
| Managed load balancer | After service exposure strategy is stable | Avoid cost/complexity during first staging |

## Acceptance Criteria

- Stack choice is documented.
- Deferred components are explicitly listed.
- No component is presented as production-ready before deployment and validation evidence exists.
- The first implementation path remains Docker Compose first, K3s later.

## Notes

This is a decision record only. It does not prove deployment success or runtime enforcement.
