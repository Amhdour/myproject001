# Oracle VPS Staging Security Boundary

## Purpose

Define the minimum security boundary for the first Oracle VPS staging deployment.

## Boundary Rules

1. Only ports 22, 80, and 443 should be intentionally exposed at the host firewall/security-list layer.
2. PostgreSQL, Qdrant, OPA, Prometheus, Loki, and Grafana must not be directly exposed to the public internet in the first staging step.
3. The real `.env.staging` file must live outside git on the VPS.
4. All demo data must be synthetic.
5. Logs must be reviewed for secrets before evidence is published.
6. Monitor-only controls must be labeled as monitor-only evidence, not enforcement evidence.
7. No raw IP, token, private key, password, or customer data should be committed.
8. Rollback must be documented before any public demo claim.

## First Go/No-Go Questions

- Can the VPS be reached by SSH?
- Is the deployment user non-root?
- Is Docker Compose installed?
- Are only intended ports exposed?
- Are databases and internal services private?
- Is HTTPS planned before public demo?
- Are secrets outside git?
- Is evidence redacted?

## Non-Claim Statement

This file defines staging boundaries only. It does not certify enterprise readiness, production readiness, compliance, or live security-control effectiveness.
