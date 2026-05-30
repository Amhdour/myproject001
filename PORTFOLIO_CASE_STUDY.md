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

- prompt injection;
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

Production-style portfolio readiness is estimated at **97%** after the release-candidate package and checks pass.

This score means the project is strong as a portfolio artifact: it has positioning, evidence packages, demo attacks, CI gates, claim boundaries, and reviewer-specific documents. It does not mean the application is 97% ready for production. Production readiness remains **NO-GO**. Enterprise production-candidate readiness is **NOT CLAIMED / NO-GO**.

## Release Candidate Status

`v0.1.0-portfolio-review` is a portfolio review release candidate. It is not a production release. It is not an enterprise readiness attestation. It is not externally validated. It is not compliance certified.

## 13. Remaining gaps

Remaining gaps include:

- full Onyx live staging not proven unless future repository evidence shows it;
- external validation pending;
- compliance certification not claimed;
- production monitoring, backup, restore, and incident-response evidence not proven;
- live enforcement, live blocking, and live filtering not claimed;
- screenshots or video walkthrough still needed for faster reviewer digestion;
- reviewer-facing release or tag recommended after final merge.

## 14. How I would present this to an agency, client, partner, or employer

For an agency or client, I would present this as evidence that I can run a focused RAG and agent security-readiness review, build launch-gate checklists, design demo attacks, prepare evidence rooms, and keep claims honest.

For a partner, I would walk through the case study, claim boundary, demo attack runner, CI checks, and known limitations before discussing any future staging or integration work.

For an employer, I would use this repository to demonstrate threat modeling, evidence discipline, security-control design, pytest usage, CI gates, and careful separation between portfolio evidence and unsupported production claims.

## 15. Final claim boundary

Safe final claim: this is a production-style portfolio project demonstrating RAG and autonomous-agent security-readiness work with evidence packaging, demo attacks, isolated tests, and CI gates.

Required final non-claims:

- Production readiness: **NO-GO**.
- Enterprise readiness: **NO-GO**.
- External validation: **PENDING**.
- Compliance certification: **NOT CLAIMED**.
- Live enforcement/blocking/filtering: **NOT CLAIMED**.
- Full Onyx live staging: **NOT CLAIMED** unless future repository evidence proves otherwise.
