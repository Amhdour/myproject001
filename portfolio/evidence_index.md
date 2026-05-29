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

## CI Evidence Gates

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`.github/workflows/security-layer-tests.yml`](../.github/workflows/security-layer-tests.yml) | CI workflow | Runs the isolated security-layer pytest suite in GitHub Actions for pull requests and manual workflow dispatches. | Does not prove production security, live enforcement, live blocking, live filtering, full Onyx staging, enterprise readiness, or compliance certification. |
| [`.github/workflows/portfolio-claim-boundary.yml`](../.github/workflows/portfolio-claim-boundary.yml) | CI workflow | Runs claim-boundary and fake-claim wording checks against reviewer-facing portfolio/security docs. | Does not prove external validation, compliance certification, production readiness, enterprise readiness, or runtime protection. |
| [`.github/workflows/evidence-integrity.yml`](../.github/workflows/evidence-integrity.yml) | CI workflow | Verifies that required reviewer evidence files are present. | Does not validate that optional infrastructure exists, that Onyx is fully deployed, or that controls are active in live request paths. |
| [`docs/security/evidence/ci_security_gates/README.md`](../docs/security/evidence/ci_security_gates/README.md) | CI evidence note | Explains the purpose, scope, workflows, and reviewer interpretation for the CI gates. | Does not create deployment evidence, external audit evidence, certification evidence, or production/enterprise readiness evidence. |

## Demo Attack Evidence

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`demo_attacks/README.md`](../demo_attacks/README.md) | Demo documentation | Explains the purpose, scope, synthetic-data-only posture, run command, and claim boundary for demo attacks. | Does not prove production protection, live blocking, live filtering, live enforcement, external validation, compliance, or runtime integration. |
| [`demo_attacks/attack_matrix.md`](../demo_attacks/attack_matrix.md) | Demo attack matrix | Maps five synthetic RAG and agent attack categories to deterministic expected outcomes and evidence. | Does not prove live controls, production readiness, enterprise readiness, compliance certification, or external validation. |
| [`demo_attacks/run_demo_attacks.py`](../demo_attacks/run_demo_attacks.py) | Deterministic demo runner | Defines and evaluates five synthetic cases with expected `denied_or_flagged` outcomes using Python standard library only. | Does not call real tools, real MCP servers, network resources, secret stores, or application runtime paths. |
| [`docs/security/evidence/demo_attack_runner/README.md`](../docs/security/evidence/demo_attack_runner/README.md) | Evidence interpretation note | Describes the command, expected result, interpretation, scope, and claim boundary for demo attack evidence. | Does not prove deployed protection, full live staging, external audit evidence, certification evidence, or security-control activation. |
| [`docs/security/evidence/demo_attack_runner/expected_results.md`](../docs/security/evidence/demo_attack_runner/expected_results.md) | Expected synthetic results | Lists the five deterministic expected outcomes and explains that results are synthetic portfolio demo evidence. | Does not prove live blocking, live filtering, live enforcement, production protection, external validation, compliance certification, production readiness, or enterprise readiness. |

## Reviewer Interpretation Rules

- Treat documentation evidence as scope, decision, and traceability evidence.
- Treat isolated test evidence as proof of isolated helper behavior only.
- Treat minimal staging evidence as narrow deployment-path evidence only.
- Treat claim-boundary evidence as authoritative for what must not be claimed.
- Do not infer production readiness, enterprise readiness, compliance certification, external validation, full live staging, live enforce-mode protection, live shadow-deny runtime, live blocking, or live filtering from this package.
