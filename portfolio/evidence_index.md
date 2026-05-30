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

## Final Portfolio Package

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`PORTFOLIO_CASE_STUDY.md`](../PORTFOLIO_CASE_STUDY.md) | Final case study | Provides the final professional narrative for agencies, clients, partners, and employers. | Does not prove production readiness, enterprise readiness, external validation, compliance certification, full live staging, or live enforcement. |
| [`CLIENT_README.md`](../CLIENT_README.md) | Client-facing guide | Explains safe service offers and portfolio/demo scope for clients or small AI agencies. | Does not provide a managed production security guarantee. |
| [`EMPLOYER_README.md`](../EMPLOYER_README.md) | Employer-facing guide | Maps the repository to AI Trust & Security Readiness Engineer skills and interview topics. | Does not prove live production operations or external assessment. |
| [`PARTNER_DEMO_README.md`](../PARTNER_DEMO_README.md) | Partner/demo guide | Gives a five-minute demo flow, commands, PASS interpretation, and status matrix. | Does not prove full Onyx live staging or live blocking/filtering. |
| [`CLAIM_BOUNDARY.md`](../CLAIM_BOUNDARY.md) | Root claim boundary | Summarizes safe claims, forbidden claims, current status, and links to detailed boundaries. | Does not remediate the listed NO-GO/PENDING/NOT CLAIMED gaps. |
| [`docs/security/evidence/final_portfolio_package/README.md`](../docs/security/evidence/final_portfolio_package/README.md) | Final evidence package index | Bundles the final evidence summary, readiness score, checklist, and remaining gaps. | Does not create runtime enforcement, production deployment, or compliance certification. |
| [`docs/security/evidence/final_portfolio_package/evidence_summary.md`](../docs/security/evidence/final_portfolio_package/evidence_summary.md) | Evidence summary | Maps final evidence categories to links, proof statements, and limitations. | Does not convert isolated tests into live application enforcement. |
| [`docs/security/evidence/final_portfolio_package/readiness_score.md`](../docs/security/evidence/final_portfolio_package/readiness_score.md) | Readiness score | Explains the 80% production-style portfolio-readiness score. | Does not mean the system is 80% ready for production. |
| [`docs/security/evidence/final_portfolio_package/reviewer_checklist.md`](../docs/security/evidence/final_portfolio_package/reviewer_checklist.md) | Reviewer checklist | Gives reviewers a concise checklist and local commands. | Does not replace independent validation or production acceptance testing. |
| [`docs/security/evidence/final_portfolio_package/remaining_gaps.md`](../docs/security/evidence/final_portfolio_package/remaining_gaps.md) | Remaining gaps | Lists unresolved gaps and final boundaries. | Does not show those gaps are remediated. |

## Release Preparation Evidence

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`portfolio/release_prep/README.md`](release_prep/README.md) | Release-prep index | Collects screenshot, video, release-note, reviewer, publication, and sanitization checklists for professional review preparation. | Does not prove production readiness, enterprise readiness, external validation, compliance certification, full live staging, or live enforcement. |
| [`portfolio/release_prep/screenshot_checklist.md`](release_prep/screenshot_checklist.md) | Manual screenshot plan | Defines which screenshots may be captured manually and how to interpret them safely. | Does not create screenshots, fabricate evidence, or prove live deployment. |
| [`portfolio/release_prep/video_walkthrough_script.md`](release_prep/video_walkthrough_script.md) | Optional video script | Provides safe wording for a seven-minute reviewer walkthrough. | Does not prove a video exists, external validation occurred, or runtime controls are active. |
| [`portfolio/release_prep/github_release_notes_draft.md`](release_prep/github_release_notes_draft.md) | Draft release notes | Gives safe release-note language for a future portfolio-review tag. | Does not create a tag or add production/enterprise/compliance claims. |
| [`portfolio/release_prep/final_reviewer_checklist.md`](release_prep/final_reviewer_checklist.md) | Final reviewer checklist | Gives reviewers a final reading, demo, CI, and evidence review sequence. | Does not replace independent validation or production acceptance testing. |
| [`portfolio/release_prep/publication_readiness_checklist.md`](release_prep/publication_readiness_checklist.md) | Publication checklist | Lists checks before making the repository public or sharing with agencies/employers. | Does not prove the checks were completed for every future publication event. |
| [`portfolio/release_prep/sanitization_checklist.md`](release_prep/sanitization_checklist.md) | Sanitization checklist | Lists secret, screenshot, deployment-evidence, log, and public-sharing sanitization steps. | Does not prove the absence of secrets without an actual scan and human review. |
| [`docs/security/evidence/release_prep/README.md`](../docs/security/evidence/release_prep/README.md) | Release-prep evidence note | Defines release-prep evidence scope and claim boundary. | Does not create runtime behavior or live enforcement evidence. |
| [`docs/security/evidence/release_prep/release_go_no_go.md`](../docs/security/evidence/release_prep/release_go_no_go.md) | Release GO/NO-GO matrix | Records GO/NO-GO/PENDING/NOT CLAIMED status for release-prep decisions. | Does not approve production use, enterprise use, certification, or live protection claims. |


## Public Sharing Audit Evidence

| Evidence link | Evidence type | What it proves | What it does NOT prove |
|---|---|---|---|
| [`portfolio/public_sharing_audit/README.md`](public_sharing_audit/README.md) | Public-sharing audit index | Defines the purpose, scope, required checks, and claim boundary for professional sharing preparation. | Does not prove production readiness, enterprise readiness, external validation, compliance certification, full live staging, or live enforcement. |
| [`portfolio/public_sharing_audit/repo_hygiene_checklist.md`](public_sharing_audit/repo_hygiene_checklist.md) | Repository hygiene checklist | Lists manual checks for portfolio positioning, evidence visibility, sanitization, attribution, and reviewer-path clarity. | Does not prove every future share is sanitized without a current human review. |
| [`portfolio/public_sharing_audit/public_review_path.md`](public_sharing_audit/public_review_path.md) | Reviewer path | Gives reviewers a recommended reading order with proof and non-proof statements for each file. | Does not replace independent validation or production acceptance testing. |
| [`portfolio/public_sharing_audit/attribution_and_license_check.md`](public_sharing_audit/attribution_and_license_check.md) | Attribution and license reminder | Preserves the upstream Onyx attribution, license, and non-endorsement boundaries. | Does not create an official Onyx endorsement or ownership claim. |
| [`portfolio/public_sharing_audit/final_safe_claims.md`](public_sharing_audit/final_safe_claims.md) | Safe public wording | Provides safe final portfolio wording for agencies, partners, employers, and reviewers. | Does not authorize production, enterprise, compliance, external-validation, or live-enforcement claims. |
| [`portfolio/public_sharing_audit/final_forbidden_claims.md`](public_sharing_audit/final_forbidden_claims.md) | Forbidden public wording | Lists claims that must not be used as positive public claims. | Does not itself make those forbidden claims. |
| [`scripts/portfolio/check_public_sharing_readiness.py`](../scripts/portfolio/check_public_sharing_readiness.py) | Lightweight validation script | Checks required public-sharing, claim-boundary, and CI files exist. | Does not scan secrets, validate deployment, or prove runtime security. |
| [`docs/security/evidence/public_sharing_audit/README.md`](../docs/security/evidence/public_sharing_audit/README.md) | Evidence note | Records the evidence category, scope, proof statements, non-proof statements, and claim boundary. | Does not add runtime behavior or live enforcement evidence. |
| [`docs/security/evidence/public_sharing_audit/public_sharing_go_no_go.md`](../docs/security/evidence/public_sharing_audit/public_sharing_go_no_go.md) | Public-sharing GO/NO-GO matrix | Records GO/NO-GO/PENDING/NOT CLAIMED status for public sharing decisions. | Does not approve production use, enterprise use, certification, or live protection claims. |
