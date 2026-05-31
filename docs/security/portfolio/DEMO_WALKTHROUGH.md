# Demo Walkthrough: Runtime Security Readiness Portfolio

## Demo Goal

The demo goal is to show a reviewer how the portfolio frames RAG and autonomous-agent runtime-security risks without overstating production readiness.

Use this walkthrough to demonstrate evidence organization, claim boundaries, and remaining work.

## Required Opening Disclaimer

Start the demo with this disclaimer:

> This is a production-style AI Trust & Security Readiness portfolio for RAG and autonomous agent systems. Step 3 is `PASS_WITH_LIMITATIONS`, and the portfolio is approximately `~99%` complete as a portfolio artifact. This is not an enterprise production-readiness claim, external validation claim, full authenticated RBAC claim, full real-user tenant-isolation claim, full real tool-blocking claim, or full real MCP server-blocking claim.

## Suggested Demo Flow

### 1. Open the Portfolio README

Show `docs/security/portfolio/README.md` and point out:

- purpose;
- positioning;
- Step 3 result;
- readiness estimate;
- explicit claim boundaries;
- remaining work.

### 2. Show the Evidence Index

Open `docs/security/portfolio/step3_runtime_security_evidence_index.json` and explain that it is a public-safe machine-readable index. Emphasize that raw staging details and secrets are excluded.

### 3. Review the Step 3 Evidence Report

Open `docs/security/portfolio/STEP3_RUNTIME_SECURITY_EVIDENCE_REPORT.md` and discuss:

- why the result is `PASS_WITH_LIMITATIONS`;
- what evidence categories are covered;
- why remaining validation is required.

### 4. Review Claim Boundaries

Open `docs/security/portfolio/PORTFOLIO_RUNTIME_SECURITY_CLAIMS.md` and show the difference between safe claims and forbidden claims.

### 5. Walk Through Security Themes

Use `docs/security/portfolio/CASE_STUDY.md` to discuss:

- prompt injection;
- retrieval access controls;
- tenant-boundary risks;
- sensitive data exposure;
- safe denial;
- auditability;
- tool authorization;
- MCP risks.

### 6. Close With Go/No-Go

Open `docs/security/portfolio/FINAL_PORTFOLIO_GO_NO_GO.md` and close with the final decision matrix.

## Demo Do's

- Say `PASS_WITH_LIMITATIONS` exactly.
- Say `~99% production-style portfolio coverage` exactly.
- Say the package is public-safe and reviewer-ready.
- Say remaining work is clearly documented.

## Demo Don'ts

Do not say:

- production-ready;
- enterprise-ready;
- externally validated;
- full authenticated RBAC is proven;
- full real-user tenant isolation is proven;
- full real tool execution blocking is proven;
- full real MCP server blocking is proven.

## Closing Script

> The portfolio is ready for reviewer presentation as a production-style AI Trust & Security Readiness package. The honest status is `PASS_WITH_LIMITATIONS` with `~99% production-style portfolio coverage`. The remaining work is host/reverse-proxy route polish, authenticated RBAC tests, seeded real-document retrieval tests, real configured tool execution tests, real MCP server execution tests, external validation, and backup/restore plus incident drills.
