# Claim Boundary

This root claim boundary summarizes safe and forbidden claims for the portfolio. For the detailed portfolio boundary, see [`portfolio/claim_boundary.md`](portfolio/claim_boundary.md). For partner wording, see [`docs/security/partner_safe_claims.md`](docs/security/partner_safe_claims.md). For limitations, see [`docs/security/known_limitations.md`](docs/security/known_limitations.md).

## Safe claims

- This is a production-style portfolio project for RAG and autonomous-agent security readiness.
- The repository contains reviewer-facing evidence packages, demo attack scenarios, CI gates, and isolated security-layer tests.
- The project demonstrates evidence discipline, launch-gate thinking, and careful claim-boundary governance.
- The current portfolio-readiness estimate is 80% as a portfolio artifact, not as a production system.

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- external validation;
- compliance certification;
- full Onyx live staging;
- live enforce-mode operation;
- live shadow-deny runtime operation;
- live blocking;
- live filtering;
- managed production security guarantees.

## Current status matrix

| Area | Status |
|---|---|
| Production-style portfolio readiness | 80% |
| Production readiness | NO-GO |
| Enterprise readiness | NO-GO |
| External validation | PENDING |
| Compliance certification | NOT CLAIMED |
| Full Onyx live staging | NOT CLAIMED unless future repository evidence proves otherwise |
| Live enforcement/blocking/filtering | NOT CLAIMED |
| Runtime code change in final package | NO |
| Enforcement enabled in final package | NO |
