# Five-Minute Demo Script

Use this script for a professional reviewer walkthrough. The language is intentionally conservative and avoids production, enterprise, certification, external-validation, and live-enforcement claims.

## 30 seconds: Project Positioning

**Exact phrasing:**

"This is a RAG and agent security-readiness portfolio built around an Onyx-based system. The contribution I want you to evaluate is not a production-readiness claim. It is the security-readiness layer: evidence discipline, launch-gate language, isolated security helpers, tests, and a reviewer-facing claim boundary that makes clear what is proven, pending, and not claimed. Current status is in progress; production readiness and enterprise readiness are both NO-GO."

## 60 seconds: Threat Model and Why RAG/Agents Need Readiness Gates

**Exact phrasing:**

"RAG and agent systems introduce risks that traditional web-app reviews often miss: prompt injection, unsafe tool use, retrieval poisoning, over-broad context exposure, untrusted connector content, insecure artifact handling, and ambiguous responsibility between model behavior and application controls. This portfolio treats those risks as readiness questions. The goal is to show how I would structure gates, evidence, and limitations before anyone makes stronger claims about deployment."

Cover these points:

- RAG/agent risk is not only model quality; it includes retrieval, tools, context, policies, and operational evidence.
- A readiness gate should say what is safe to claim, what is pending, and what remains blocked.
- The repository preserves NO-GO / PENDING / NOT CLAIMED language instead of overclaiming.

## 60 seconds: Security Layer and Evidence Room

**Exact phrasing:**

"The security layer is intentionally scoped. Many controls are isolated helpers, design artifacts, or monitor-only concepts unless the repository evidence proves otherwise. I am not claiming live enforce-mode, live shadow-deny runtime, live blocking, or live filtering. The evidence room under docs/security captures what was planned, what was implemented in isolated form, what was tested, and what remains out of scope."

Show:

- `portfolio/architecture.md` for the layered view.
- `docs/security/evidence_report.md` for evidence discipline.
- `docs/security/execution_tracker.md` for step tracking.
- `docs/security/known_limitations.md` for blockers and limitations.

## 60 seconds: Tests and Demo Attacks

**Exact phrasing:**

"The local tests are useful because they make isolated security-layer behavior reviewable. They do not prove production security, and I would not present them as live enforcement evidence. The right interpretation is: these tests demonstrate that specific helper behavior exists and is covered in isolation. They are one component of a readiness package, not a substitute for integration, staging, monitoring, or external validation."

Run or reference:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

Explain:

- Passing tests are scoped to `backend/security_layer/tests`.
- Test success does not remove NO-GO status for production or enterprise readiness.
- Demo attacks should be framed as controlled demonstrations, not proof of production protection.

## 60 seconds: Staging/Deployment Evidence and Limitations

**Exact phrasing:**

"The staging evidence is minimal and must stay scoped. Where the repository documents Oracle/Coolify or docker-compose minimal staging artifacts, those artifacts support a narrow reviewer demo path. They do not prove full Onyx live staging, production monitoring, backup, rollback, enterprise hardening, or live security enforcement. Full Onyx live staging remains NO-GO unless real repository evidence proves otherwise."

Show if present:

- `docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md`
- `deployment/docker_compose/docker-compose.step34x-minimal.yml`

## 30 seconds: Final Claim Boundary and Next Steps

**Exact phrasing:**

"The final claim boundary is the most important part of this portfolio. Safe claims are: AI security-readiness portfolio, Onyx-based RAG/agent security case study, isolated helper tests, evidence-room and launch-gate discipline, minimal staging evidence where documented, and a production-style demo. Forbidden claims include production-ready, enterprise-ready, compliance-certified, externally validated, full live Onyx staging, and live enforce-mode protection. Next steps would be CI gates, stronger evidence automation, and real integration or staging only when evidence can support those claims."
