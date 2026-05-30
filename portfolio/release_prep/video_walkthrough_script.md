# Seven-Minute Video Walkthrough Script

Use this script only for an optional manually recorded reviewer video. Do not record secrets, private URLs, IPs, credentials, SSH keys, tokens, emails, private customer data, or unsanitized deployment dashboards.

Safe wording to use exactly:

> “This is a production-style portfolio project, not an enterprise production deployment.”

## 0:00–0:45 — Project Positioning

- Open the root README.
- Say: “This is a production-style portfolio project, not an enterprise production deployment.”
- Explain that the repository demonstrates RAG and autonomous-agent security readiness around an Onyx-based system.
- Emphasize that the value is in evidence discipline, claim boundaries, demo attacks, CI gates, and reviewer-ready documentation.
- State that production readiness, enterprise readiness, external validation, and compliance certification are not claimed.

## 0:45–1:30 — Role And Career Objective

- Explain the role focus: Senior AI Trust & Security Readiness Engineer specializing in RAG and Autonomous Agents.
- Describe the career objective: help teams evaluate AI systems before launch by documenting risks, controls, test evidence, and safe release gates.
- Point to the portfolio README as the reviewer route.
- Keep wording focused on readiness and review, not production assurance.

## 1:30–2:20 — Architecture

- Open `portfolio/architecture.md`.
- Walk through the system layers at a high level: Onyx foundation, security-readiness layer, evidence room, CI gates, and demo attack runner.
- Explain that the security-layer tests are isolated helpers and evidence artifacts, not proof of live runtime enforcement.
- Avoid claiming full Onyx live staging unless real repository evidence proves it.

## 2:20–3:20 — Evidence Room And Claim Boundary

- Open `portfolio/evidence_index.md` and the claim-boundary page.
- Explain how the evidence index separates what each artifact proves from what it does not prove.
- Show NO-GO / PENDING / NOT CLAIMED language.
- Say that this evidence room is intentionally conservative and avoids fake deployment claims.

## 3:20–4:20 — CI Gates

- Open the GitHub Actions workflow files or a real passing workflow run if available.
- Explain the security-layer test gate, claim-boundary check, no-fake-claims check, and evidence-link check.
- State that CI gates increase reviewer confidence for this repository scope.
- Clarify that CI gates do not prove production protection, external validation, or compliance certification.

## 4:20–5:20 — Demo Attack Runner

- Open `demo_attacks/README.md` and run or show a real captured terminal output for `python demo_attacks/run_demo_attacks.py`.
- Explain that the runner uses synthetic demo attacks and deterministic expected outcomes.
- State that it demonstrates portfolio-level reasoning about prompt injection, unsafe tool requests, data exfiltration attempts, and related RAG/agent risks.
- Clarify that it does not call live tools, real MCP servers, customer systems, or production enforcement paths.

## 5:20–6:15 — Final Portfolio Case Study

- Open `PORTFOLIO_CASE_STUDY.md`.
- Summarize the reviewer narrative: problem, security-readiness approach, evidence produced, and final boundaries.
- Point to client, employer, and partner demo guides if useful.
- Avoid any claim that the case study is an external validation or production certification.

## 6:15–7:00 — What Is Not Claimed And Next Steps

- Open the remaining gaps or release GO/NO-GO page.
- State clearly:
  - Production readiness: NO-GO.
  - Enterprise readiness: NO-GO.
  - External validation: PENDING.
  - Compliance certification: NOT CLAIMED.
  - Full Onyx live staging: NOT CLAIMED unless future real evidence proves it.
  - Live enforcement, live blocking, and live filtering: NOT CLAIMED.
- Close with next steps: optional sanitized screenshots, optional sanitized video, real reviewer feedback, and future evidence-backed staging work only if it actually occurs.
