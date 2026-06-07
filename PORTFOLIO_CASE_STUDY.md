# RAG & Agent Security Readiness Portfolio Case Study

## 1. Executive summary

This repository is a production-style portfolio project built around an Onyx-based RAG and agent platform. The portfolio work demonstrates how I approach AI trust, safety, security-readiness, evidence packaging, and launch-gate decisioning for retrieval-augmented generation and autonomous-agent systems.

The project is intentionally scoped as reviewer-facing portfolio evidence. It is not enterprise production-ready, and it does not claim production readiness. Production readiness remains **NO-GO**. Enterprise readiness remains **NO-GO**. External validation remains **PENDING**. Compliance certification is **NOT CLAIMED**. Live enforcement, live blocking, and live filtering are **NOT CLAIMED**.

## 2. Problem statement

RAG and autonomous-agent systems introduce risks that traditional web application checklists do not fully cover. They combine retrieval, model reasoning, prompt construction, tool use, connector permissions, generated artifacts, cache behavior, and agent autonomy. A team evaluating such a system needs evidence that security assumptions are explicit, testable, and bounded by honest claims.

This portfolio project addresses that problem by turning an existing RAG and agent codebase into a structured security-readiness case study with evidence indexes, demo attacks, CI gates, claim boundaries, and clearly documented remaining gaps.

## 3. Why RAG and autonomous agents need readiness gates

RAG and agent systems need readiness gates because failures can cross boundaries between data access, prompt behavior, generated output, tool execution, and user trust. Useful gates include:

- retrieval ACL and cross-tenant leakage checks;
- prompt-injection and instruction-conflict reviews;
- tool authorization and argument validation reviews;
- MCP and external-action risk reviews;
- sensitive-data exposure checks;
- artifact safety and release-policy reviews;
- evidence-room checks before launch or partner review;
- claim-boundary checks so demos do not overstate readiness.

These gates reduce ambiguity. They help reviewers distinguish isolated helper evidence from live runtime enforcement, documentation evidence from external validation, and portfolio readiness from production readiness.

## 4. Project architecture

The underlying application foundation is Onyx, an open-source RAG and agent platform. This portfolio layer is organized around:

- root-level reviewer documents;
- the `/portfolio` reviewer package;
- `docs/security/` readiness and evidence documentation;
- `.github/workflows/` CI checks for claim boundary, evidence integrity, and security-layer tests;
- `demo_attacks/` synthetic attack cases and runner;
- `backend/security_layer/` isolated Python helpers and tests.

The architecture should be interpreted as a security-readiness portfolio wrapped around an application platform. It is not proof of a fully live, production Onyx deployment.

## 5. My contribution

My contribution is the trust-and-security readiness layer around the platform, including:

- evidence-room structure and reviewer navigation;
- safe claim-boundary governance;
- risk and launch-gate language;
- isolated security helper design;
- pytest coverage for helper behavior;
- synthetic demo attack design;
- CI gate setup for portfolio integrity;
- known-limitation documentation;
- final reviewer-facing case study and evidence package.

This contribution demonstrates how I would help a team make security posture reviewable before making stronger deployment or compliance claims.

## 6. Security controls and evidence areas

The portfolio organizes evidence around these areas:

- prompt injection and instruction hierarchy risk;
- retrieved-content prompt-injection detection at a retrieval/context boundary;
- retrieval ACL and cross-tenant leakage risk;
- sensitive data exposure risk;
- unsafe tool-call and tool-authorization risk;
- MCP confused-deputy and credential-isolation risk;
- cache and vector metadata contracts;
- artifact safety and release-policy considerations;
- monitor-only and future-mode boundaries;
- evidence integrity and claim-boundary checks.

These areas are evidence and readiness artifacts. They do not prove live enforce-mode protection, live blocking, live filtering, or production deployment.

## 7. Demo attack coverage

The synthetic demo attack runner covers reviewer-safe scenarios such as:

- direct prompt injection;
- retrieved-content prompt injection;
- retrieval cross-tenant leakage;
- sensitive data exposure;
- unsafe tool call;
- MCP confused deputy.

The demo is useful for showing security thinking, test discipline, and repeatable evidence. Passing it does not mean the live application is protected in production.

## 8. CI and validation gates

The repository includes CI-style gates for:

- security-layer tests;
- portfolio claim-boundary checks;
- fake or unsupported claim checks;
- evidence-link presence checks.

These gates support portfolio quality and evidence consistency. They do not replace penetration testing, independent assessment, production monitoring, operational runbooks, backup and restore tests, or compliance audits.

## 9. Oracle/Coolify/minimal staging status

The repository contains minimal Oracle/Coolify staging-path evidence where documented. That evidence should be interpreted narrowly. Minimal staging artifacts can demonstrate deployment planning and limited smoke-test thinking, but full Onyx live staging is not claimed unless directly supported by repository evidence.

Full Onyx live staging remains **not claimed** in this final case study. Production readiness remains **NO-GO**.

## 10. What is proven

This portfolio proves that the repository contains:

- a professional security-readiness narrative;
- reviewer-facing claim boundaries;
- evidence indexes and final package documentation;
- synthetic demo attack scenarios;
- CI gate definitions for portfolio checks;
- isolated security-layer helper tests;
- focused retrieved-content prompt-injection detector tests and real-path hook wiring proof;
- explicit known limitations and NO-GO/PENDING/NOT CLAIMED status language.

## 11. What is not proven

This portfolio does not prove:

- production readiness;
- enterprise readiness;
- compliance certification;
- external validation;
- full Onyx live staging;
- live enforce-mode behavior;
- live shadow-deny runtime behavior;
- live blocking, live filtering, or live security-control activation;
- production monitoring, incident response, backup, or restore maturity.

## 12. Current readiness score

Current aggregate readiness is separated by claim type:

| Dimension | Current wording |
|---|---|
| Portfolio presentation readiness | 94% |
| Technical portfolio proof readiness | 88% |
| Client demo readiness | 85% |
| Production-style runtime proof readiness | 70% for bounded retrieval/context hook proof only |
| Enterprise production-candidate readiness | 20% / NO-GO |
| Real production readiness | 8% / NO-GO |
| Production readiness | NO-GO |
| Enterprise readiness | NO-GO |
| External validation | PENDING |
| Compliance certification | NOT CLAIMED |

These scores mean the project is strong as a portfolio artifact with bounded technical proof. They do not mean the application is production-ready or enterprise-ready. Older step-specific evidence percentages are historical snapshots and are not current aggregate readiness claims.

## Release Candidate Status

`v0.1.0-portfolio-review` is a portfolio review release candidate. It is not a production release. It is not an enterprise readiness attestation. It is not externally validated. It is not compliance certified.

## 13. Remaining gaps

Remaining gaps include:

- full Onyx live staging not proven unless future repository evidence shows it;
- external validation pending;
- compliance certification not claimed;
- production monitoring, backup, restore, and incident-response evidence not proven;
- live enforcement, live blocking, and live filtering not claimed;
- full prompt-injection defense not claimed; retrieved-content prompt-injection detection is bounded to tested/demoed paths;
- screenshots or video walkthrough still needed for faster reviewer digestion;
- reviewer-facing release or tag recommended after final merge.

## 14. How I would present this to an agency, client, partner, or employer

For an agency or client, I would present this as evidence that I can run a focused RAG and agent security-readiness review, build launch-gate checklists, design demo attacks, prepare evidence rooms, and keep claims honest.

For a partner, I would walk through the case study, claim boundary, demo attack runner, CI checks, and known limitations before discussing any future staging or integration work.

For an employer, I would use this repository to demonstrate threat modeling, evidence discipline, security-control design, pytest usage, CI gates, and careful separation between portfolio evidence and unsupported production claims.

## 15. Final claim boundary

Safe final claim: this is an Onyx-based AI security-readiness portfolio focused on RAG and agent runtime controls, including policy-as-code structure, retrieval ACL testing, retrieved-content prompt-injection detection, tool authorization, MCP governance, sandbox/artifact safety checks, audit/evidence reporting, demo attacks, CI workflow definitions, and strict claim-boundary documentation.

Required final non-claims:

- Production readiness: **NO-GO**.
- Enterprise readiness: **NO-GO**.
- External validation: **PENDING**.
- Compliance certification: **NOT CLAIMED**.
- Live enforcement/blocking/filtering: **NOT CLAIMED**.
- Full prompt-injection defense: **NOT CLAIMED**.
- Full Onyx live staging: **NOT CLAIMED** unless future repository evidence proves otherwise.

## Historical addenda note

The addenda below preserve historical step-level snapshots from earlier implementation passes. Their percentages are not current aggregate readiness claims; use Section 12 and `CLAIM_BOUNDARY.md` for current public-facing readiness wording.

## Step 39X Runtime Enforcement Proof Addendum

Step 39X adds a narrow real runtime-facing retrieval enforcement proof. The hook is placed after retrieval candidates are produced in the backend search runner and before chunks are returned from that runtime path. It supports `disabled`, `monitor_only`, and `enforce` modes, with `disabled` as the safe default.

This addendum is intentionally scoped: it demonstrates one minimal allow/deny enforcement path with structured audit evidence and safe denial behavior. It does not claim enterprise production readiness, external validation, compliance certification, live staging/cloud validation, real customer deployment, full Onyx-wide enforcement, or complete RAG/agent security coverage.


## Step 40X Runtime Enforcement PR Review Gate Addendum

Step 40X reviewed the Step 39X runtime-facing retrieval enforcement proof and preserved its narrow claim boundary. The review gate added evidence under `docs/security/evidence/step_40x_runtime_enforcement_pr_review_merge_gate/`, fixed narrow runtime-safety/test hardening issues, and re-ran the required local gates.

The Step 40X status remains intentionally bounded: production readiness is **NO-GO**, enterprise production-candidate readiness is **NO-GO**, external validation is **PENDING**, compliance certification is **NOT CLAIMED**, live staging/cloud validation is **PENDING**, and full Onyx-wide enforcement is **NOT CLAIMED**.

## Step 42X Actual Live Staging Deployment Evidence Addendum

Step 42X attempted the first actual staging-deployment evidence step and recorded the result honestly. Real cloud/VPS staging was unavailable because this checkout had no origin remote, no staging host, no Coolify target, no OCI configuration, and no deployment access markers. Docker Compose local staging was then selected as the fallback path, but it was blocked because Docker and Docker Compose were not installed in the execution environment.

The Step 42X status is **DEPLOYMENT_BLOCKED**. Live staging/cloud validation remains **PENDING**, local staging validation remains **PENDING**, external validation remains **PENDING**, compliance certification is **NOT CLAIMED**, and enterprise production-candidate readiness remains **NO-GO**. Historical step-level readiness snapshot was recorded after Step 42X, but it is superseded by the current separated readiness matrix and does not indicate production readiness.

## Step 43X Addendum — GitHub Remote PR CI Verification Gate

Step 43X attempted to close the Step 42X local-only evidence gap by configuring the expected GitHub origin, checking branch push feasibility, checking PR metadata feasibility, and inventorying local GitHub Actions workflow files. The local origin now points to `https://github.com/Amhdour/myproject001.git`, but remote reachability failed from the sandbox with HTTP CONNECT tunnel 403, GitHub CLI was unavailable, and the Step 42X branch/commit identifiers requested for remote sync were not present locally.

The Step 43X classification is **REMOTE_SYNC_BLOCKED**. Historical step-level readiness snapshot remains superseded by the current separated readiness matrix, enterprise production-candidate readiness remains **NO-GO**, live staging/cloud validation remains **PENDING**, external validation remains **PENDING**, and compliance certification remains **NOT CLAIMED**. Step 43X does not claim GitHub CI success, remote sync resolution, production readiness, enterprise readiness, external validation, certification, full Onyx-wide enforcement, or customer deployment.

## Step 45X Addendum — GitHub PR Chain Reconciliation and CI Actions Verification

Step 45X reconciled the earlier Step 44X repository-recovery blocker with the local merge history now visible in the workspace. The local repository contains merge commits whose messages identify PR #102, #103, #104, #105, and #106, and those local merge commits resolve as git commit objects.

The Step 45X classification is **PR_CHAIN_PARTIALLY_VERIFIED**. This partially supersedes Step 44X for local PR-chain visibility, but it does not resolve GitHub-side verification. GitHub CLI is unavailable, direct GitHub API access is blocked by HTTP CONNECT 403, local `main` checkout fails, no `origin` remote is configured, and GitHub Actions runs/conclusions remain unavailable.

Historical step-level readiness snapshot remains superseded by the current separated readiness matrix, enterprise production-candidate readiness remains **NO-GO**, live staging/cloud validation remains **PENDING**, external validation remains **PENDING**, and compliance certification remains **NOT CLAIMED**. Step 45X does not claim GitHub Actions success, production readiness, enterprise readiness, customer deployment, external validation, certification, real cloud deployment, or full Onyx-wide enforcement.

## Step 46X CI Evidence Update

Step 46X added a GitHub Actions CI run trigger and verification evidence package. The local workflow inventory confirms three workflows are present and configured for `pull_request` plus `workflow_dispatch`, but this environment could not trigger or query real GitHub Actions because `gh` is unavailable, no `origin` remote is configured, and GitHub API access fails with HTTP CONNECT 403. The Step 46X classification is `CI_ACTIONS_BLOCKED`.

Historical step-level readiness snapshot remains superseded by the current separated readiness matrix because CI evidence is blocked rather than verified pass. Enterprise production-candidate readiness remains **NO-GO**. Live staging/cloud validation remains **PENDING**, external validation remains **PENDING**, and compliance certification remains **NOT CLAIMED**.

## Step 47X Docker Local Compose Staging Proof

Step 47X added a Docker/local compose staging evidence package. The result was intentionally conservative: `DOCKER_STAGING_BLOCKED`. Docker was not installed in the workspace, so Docker Compose config validation and local stack startup could not run. The selected compose path was inspected (`deployment/docker_compose/docker-compose.yml`, `deployment/docker_compose/docker-compose.onyx-lite.yml`, and `deployment/docker_compose/docker-compose.dev.yml`), but local Docker staging was not proven.

Readiness after Step 47X remains bounded: historical step-level readiness snapshot is superseded by the current separated readiness matrix; enterprise production-candidate readiness is NO-GO; local Docker staging evidence is BLOCKED; live staging/cloud validation is PENDING; CI Actions evidence remains BLOCKED from Step 46X; external validation is PENDING; compliance certification is NOT CLAIMED.

## Step 50X Oracle Staging Evidence Addendum

Step 50X adds a claim-bounded Oracle VPS staging evidence package. The Oracle VPS evidence shows SSH access, Ubuntu 24.04.4 LTS on ARM64, Docker `29.5.2`, Docker Compose `v5.1.4`, Coolify, and Traefik/Coolify proxy readiness. It also records a real Onyx staging blocker: the API expected MinIO at `http://minio:9000`, but MinIO was missing.

A manual staging diagnostic MinIO container was added to the Onyx Docker network with alias `minio`, the `onyx-file-store-bucket` bucket was created, and the API became healthy after service restart. This is documented as staging diagnostic evidence, not durable production architecture.

The web service remains Docker-unhealthy because its healthcheck targets `http://127.0.0.1:3000/`, while manual probes showed `127.0.0.1:3000` returned `ECONNREFUSED` and container hostname/IP probes returned HTTP `200`. Host/proxy curl evidence shows the host layer responds: port `8000` redirects to `/login`, port `8088` returns nginx `200 OK`, and port `80` returns `404` because no matching route/domain is configured.

The Step 50X classification is `ORACLE_ONYX_STAGING_PARTIAL_GO`. Historical step-level readiness snapshot is superseded by the current separated readiness matrix, enterprise production-candidate readiness remains NO-GO, Oracle staging evidence is PARTIAL GO, live full app GO is NOT CLAIMED, external validation is PENDING, and compliance certification is NOT CLAIMED.

## Step 52X Addendum — Custom Onyx Backend Image Runtime-Code Deployment Attempt

Step 52X attempted to move from source-level Step 39X runtime enforcement evidence toward a custom Onyx backend image deployment. The repository contains the Step 39X runtime enforcement package and retrieval hook, and `backend/Dockerfile` now copies `backend/security_layer` into `/app/backend/security_layer` so future backend images built from the repository can include the runtime enforcement package expected at `/app/backend/security_layer/runtime_enforcement`.

The execution result is intentionally bounded: `ORACLE_CUSTOM_IMAGE_BUILD_BLOCKED`. Docker and Docker Compose are unavailable in this workspace, so no custom image was built or runtime-checked. SSH hostname resolution for `rag-agent-security-staging-v2` also failed, so no Oracle VPS deployment or deployed-container verification occurred. The project therefore does not claim Oracle runtime enforcement is deployed or active.

Readiness impact after Step 52X: historical step-level readiness snapshot remains superseded by the current separated readiness matrix; enterprise production-candidate readiness remains NO-GO; runtime enforcement behavior smoke testing remains NOT EXECUTED; external validation remains PENDING; compliance certification remains NOT CLAIMED.

## Step 57X Addendum — Independent Reviewer Package + Review Request

Step 57X adds a clean reviewer-facing package at `docs/security/evidence/step_57x_independent_reviewer_package_request/`. The package is designed for a mentor, security engineer, AI agency, potential client, or external reviewer to judge whether the evidence supports the bounded portfolio claims.

The Step 57X classification is `INDEPENDENT_REVIEW_PACKAGE_READY_EXTERNAL_VALIDATION_REQUEST_PENDING`. This means the request package is ready, not that external validation is complete. No independent reviewer response, third-party approval, production readiness, enterprise production-candidate readiness, compliance certification, full Onyx-wide enforcement, customer deployment, complete CI verification, full domain/TLS route, full web health GO, or security certification is claimed.

Readiness after Step 57X remains bounded: historical step-level readiness snapshot is superseded by the current separated readiness matrix; enterprise production-candidate readiness is NO-GO; Oracle staging evidence is PARTIAL GO; runtime enforcement behavior is PARTIAL GO; external validation is REQUEST PACKAGE READY / NOT YET COMPLETED; compliance certification is NOT CLAIMED.

## Step 58X Addendum — External Reviewer Response Intake + Finding Tracker

Step 58X adds a structured external reviewer response intake and finding tracker package at `docs/security/evidence/step_58x_external_reviewer_response_intake_finding_tracker/`. The package prepares templates and process controls for future reviewer feedback, severity assignment, evidence mapping, remediation planning, retest evidence, and closure decisions.

The Step 58X classification is `EXTERNAL_REVIEW_INTAKE_READY_NO_RESPONSE_YET`. This means the intake system and finding tracker are ready, not that a reviewer response has been received or external validation is complete. No reviewer approval, third-party validation, production readiness, enterprise production-candidate readiness, compliance certification, independent red-team report, or finding closure is claimed.

Readiness after Step 58X remains bounded: historical step-level readiness snapshot is superseded by the current separated readiness matrix; enterprise production-candidate readiness is NO-GO; external validation is REQUEST PACKAGE READY / NO RESPONSE YET; compliance certification is NOT CLAIMED. The finding tracker remains empty until a real reviewer response is received.

## Step 62X Addendum — Durable Coolify/Compose Deployment Architecture

Step 62X addresses simulated finding `SIM-F-004`, which identified that the prior Oracle staging deployment was diagnostic rather than durable. The selected remediation is Option B: a dedicated Oracle staging Compose override at `deployment/docker_compose/docker-compose.oracle-staging.override.yml`.

The override documents/configures the custom backend image path for both `api_server` and `background`, durable MinIO service wiring, the required `onyx-file-store-bucket`, explicit S3 file-store variables, and service-local MinIO discovery through `http://minio:9000`. It preserves the Step 61X web healthcheck patch by keeping the `WEB_HEALTHCHECK_HOST` override and hostname-compatible default in the base compose files.

Step 62X is classified as `DURABLE_DEPLOYMENT_ARCHITECTURE_READY_RETEST_PENDING`. It does not claim Oracle VPS verification, full staging GO, production readiness, enterprise production-candidate readiness, real external validation, customer deployment, independent red-team completion, or compliance certification. Historical step-level readiness snapshot remains superseded by the current separated readiness matrix; enterprise production-candidate remains NO-GO; external validation remains simulated response only / real validation pending; compliance certification is NOT CLAIMED.
