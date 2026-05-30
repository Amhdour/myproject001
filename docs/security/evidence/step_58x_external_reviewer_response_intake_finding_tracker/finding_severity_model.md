# Finding Severity Model

Use this model to classify reviewer findings. Severity is based on claim impact, security impact, evidence integrity, and reproducibility impact.

## CRITICAL

- **Definition:** Invalidates a core security claim or exposes secrets.
- **Example:** Reviewer identifies committed credentials, private keys, or evidence proving a stated runtime security control is absent while the package claims it is active.
- **Expected response time:** Immediate triage; stop affected publication or sharing until redaction or claim downgrade is complete.
- **Closure requirement:** Verified remediation evidence, secret rotation or exposure analysis if applicable, updated claim boundaries, and retest evidence.

## HIGH

- **Definition:** Blocks a portfolio claim or runtime enforcement claim.
- **Example:** Reviewer shows that a smoke test does not exercise the claimed enforcement path, or that a stated staging control is not deployed where the claim says it is.
- **Expected response time:** Triage within 1 business day and remediation plan before further reliance on the affected claim.
- **Closure requirement:** Retest evidence that directly exercises the affected claim, plus updated documentation if wording changed.

## MEDIUM

- **Definition:** Weakens evidence or reproducibility.
- **Example:** Reviewer cannot reproduce a check because the command, environment assumption, expected output, or evidence link is incomplete.
- **Expected response time:** Triage within 3 business days and schedule remediation based on publication priority.
- **Closure requirement:** Added or corrected evidence, reproduction instructions, or traceability updates showing the issue is resolved.

## LOW

- **Definition:** Documentation clarity issue or minor evidence gap that does not materially change the claim boundary.
- **Example:** Reviewer requests clearer labels for a table, a better explanation of a known limitation, or a link to a nearby supporting artifact.
- **Expected response time:** Triage within 5 business days or before the next public-facing evidence refresh.
- **Closure requirement:** Documentation update or rationale explaining why no change is needed.

## INFO

- **Definition:** Reviewer suggestion with no claim impact.
- **Example:** Reviewer suggests an optional formatting improvement, additional context, or a future enhancement that does not affect current readiness claims.
- **Expected response time:** Triage during normal backlog review.
- **Closure requirement:** Record the decision, optional follow-up, or accepted backlog item; no retest evidence is required unless a claim later changes.
