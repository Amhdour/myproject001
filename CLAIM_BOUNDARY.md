# Claim Boundary

This root claim boundary is the current source of truth for public readiness wording. For the detailed portfolio boundary, see [`portfolio/claim_boundary.md`](portfolio/claim_boundary.md). For partner wording, see [`docs/security/partner_safe_claims.md`](docs/security/partner_safe_claims.md). For limitations, see [`docs/security/known_limitations.md`](docs/security/known_limitations.md).

## Safe current public claim

> “I built an Onyx-based AI security-readiness portfolio focused on RAG and agent runtime controls, including policy-as-code structure, retrieval ACL testing, retrieved-content prompt-injection detection, tool authorization, MCP governance, sandbox/artifact safety checks, audit/evidence reporting, demo attacks, CI workflow definitions, and strict claim-boundary documentation.”

This claim is limited to repository evidence, focused tests, synthetic demo attacks, and CI workflow definitions. It is not a production, enterprise, staging, compliance, or external-validation claim.

## Readiness dimensions

These dimensions are intentionally separated so reviewer-facing portfolio maturity is not confused with production security readiness.

| Dimension | Current wording | Reviewer interpretation |
|---|---|---|
| Portfolio presentation readiness | 94% | Reviewer package, navigation, evidence indexes, and claim-boundary language are largely consistent. |
| Technical portfolio proof readiness | 88% | Focused tests and local evidence cover the portfolio controls that are implemented. |
| Client demo readiness | 85% | Synthetic demo attacks and reviewer commands are suitable for a bounded demo conversation. |
| Production-style runtime proof readiness | 70% | Bounded real-path hook wiring and focused tests exist for retrieval ACL/runtime proof and retrieved-content prompt-injection detection; this is not full live runtime coverage. |
| Enterprise production-candidate readiness | 20% | Enterprise production-candidate readiness remains a NO-GO because operational, scale, deployment, external-review, monitoring, and governance proof is incomplete. |
| Real production readiness | 8% | Real production readiness remains a NO-GO because live deployment, incident, rollback, monitoring, data-governance, and external assurance evidence is incomplete. |
| Production readiness | NO-GO | Do not claim production readiness. |
| Enterprise readiness | NO-GO | Do not claim enterprise deployment readiness. |
| External validation | PENDING | No completed independent external validation is claimed. |
| Compliance certification | NOT CLAIMED | No SOC 2, ISO, HIPAA, PCI, GDPR, or similar certification/compliance claim is made. |

## Claim-boundary consistency note

Older step-specific evidence files may retain historical percentage snapshots from the step when they were written. Those historical percentages must not be reused as current aggregate readiness claims. The current public-facing readiness language is the separated matrix above.

## Evidence level boundaries

| Evidence level | Current status |
|---|---|
| Implemented | Isolated security-layer helpers, retrieval ACL proof helpers, retrieved-content prompt-injection detector, tool/MCP/artifact helpers, demo runner, evidence scripts, and reviewer docs exist in the repository. |
| Tested | Focused local tests exist for the retrieved-content prompt-injection detector and real-path hook wiring, plus existing isolated security-layer tests. |
| Demo-proven | Synthetic demo attacks can be run locally; they demonstrate portfolio-level evaluation coverage only. |
| CI-proven | CI workflow definitions exist. Do not claim GitHub Actions pass for this branch unless a real Actions run URL/evidence exists. |
| Staging-proven | Only the narrow historical staging evidence already documented in the repository may be referenced. The new retrieved-content prompt-injection control has no staging proof. |
| Not yet proven | Full live Onyx-wide enforcement, full production monitoring, full staging redeploy proof for this control, external validation completion, compliance certification, customer deployment, and enterprise production readiness. |

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- external validation completion;
- compliance certification;
- full Onyx live staging;
- full prompt-injection defense;
- live enforce-mode operation;
- live shadow-deny runtime operation;
- live blocking;
- live filtering;
- managed production security guarantees.
