# Evidence Index

This index points reviewers to existing repository evidence and explains both what each artifact proves and what it does not prove. Evidence should be interpreted through the claim boundary in [`claim_boundary.md`](claim_boundary.md).

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`README.md`](../README.md) | Documentation | Provides the top-level portfolio positioning, current status language, safe claims, forbidden claims, and reviewer orientation. | Does not prove production readiness, enterprise readiness, external validation, compliance certification, full live staging, or live enforcement. |
| [`docs/security/README.md`](../docs/security/README.md) | Documentation | Shows the security-readiness documentation structure, completed steps, deliverables, and non-claim posture. | Does not prove runtime integration, production security, or that controls are live in application request paths. |
| [`docs/security/execution_tracker.md`](../docs/security/execution_tracker.md) | Documentation / claim-boundary evidence | Tracks security-readiness execution metadata, evidence links, blockers, and non-claim rules across steps. | Does not prove production readiness, compliance, external validation, or validated live control effectiveness. |
| [`docs/security/evidence_report.md`](../docs/security/evidence_report.md) | Documentation / isolated test evidence index | Summarizes evidence bundles and the evidence discipline used for security-readiness work. | Does not convert isolated helper evidence into production enforcement or full integration evidence. |
| [`docs/security/known_limitations.md`](../docs/security/known_limitations.md) | Claim-boundary evidence | Lists blockers, limitations, inactive runtime enforcement, and other constraints reviewers must consider. | Does not prove readiness; it intentionally documents why stronger claims remain blocked or out of scope. |
| [`docs/security/partner_safe_claims.md`](../docs/security/partner_safe_claims.md) | Claim-boundary evidence | Defines partner-safe wording and required non-claims such as no production readiness, no external validation, and no live enforcement. | Does not prove partner acceptance, external validation, certification, or production deployment. |
| [`docs/security/final_claim_boundary.md`](../docs/security/final_claim_boundary.md) | Claim-boundary evidence | Records final allowed/disallowed claims and required status language where present. | Does not prove live staging validation, compliance certification, external validation, enforce mode, shadow-deny runtime, live blocking, or live filtering. |
| [`docs/security/final_evidence_package_index.md`](../docs/security/final_evidence_package_index.md) | Documentation / evidence-room index | Lists the final pilot-partner evidence bundle, source documents, helper package, and test evidence files where present. | Does not prove that every helper is wired into live Onyx runtime paths or that production controls are active. |
| [`docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md`](../docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md) | Minimal staging evidence / claim-boundary evidence | Records scoped Step 34X Oracle/Coolify go/no-go status, including validated infrastructure steps and explicit NO-GO/PENDING statuses. | Does not prove full Onyx live staging, production readiness, enterprise readiness, external validation, compliance certification, or live enforcement. |
| [`deployment/docker_compose/docker-compose.step34x-minimal.yml`](../deployment/docker_compose/docker-compose.step34x-minimal.yml) | Minimal staging evidence | Provides a minimal nginx health-check docker-compose artifact labeled as Step 34X minimal live-staging evidence with full Onyx marked resource-blocked. | Does not prove full Onyx deployment, application security, production monitoring, rollback, backup, or runtime blocking/filtering. |

## Reviewer Interpretation Rules

- Treat documentation evidence as scope, decision, and traceability evidence.
- Treat isolated test evidence as proof of isolated helper behavior only.
- Treat minimal staging evidence as narrow deployment-path evidence only.
- Treat claim-boundary evidence as authoritative for what must not be claimed.
- Do not infer production readiness, enterprise readiness, compliance certification, external validation, full live staging, live enforce-mode protection, live shadow-deny runtime, live blocking, or live filtering from this package.
