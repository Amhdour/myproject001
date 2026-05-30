# Reviewer Response Intake Process

This process applies only after a real independent reviewer response is received. Until then, the finding tracker remains empty and external validation remains `REQUEST PACKAGE READY / NO RESPONSE YET`.

## Reviewer-Response Flow

1. **Receive reviewer response.**
   - Record the receipt channel and preserve the original response outside the public repository if confidentiality is unclear.
2. **Confirm reviewer identity/role, date, and scope.**
   - Confirm reviewer name, role, organization if provided, date received, and what evidence or claims were reviewed.
3. **Redact sensitive data.**
   - Remove private contact details, confidential reviewer text, secrets, tokens, cookies, environment dumps, SSH keys, OCI credentials, and other sensitive operational data before committing any summary.
4. **Store response summary.**
   - Store a sanitized summary in the intake package or later evidence package. Keep raw confidential responses outside the public repo unless explicit permission allows inclusion.
5. **Extract findings.**
   - Convert each reviewer-identified issue into a discrete finding with a title, category, affected claim, and evidence path.
6. **Assign severity.**
   - Apply `finding_severity_model.md` and record the severity in `finding_tracker.md`.
7. **Map finding to evidence.**
   - Use `evidence_mapping_template.md` to identify current evidence, evidence weakness, required proof, and claim impact.
8. **Decide remediation action.**
   - Use `remediation_plan_template.md` to document fix owner, planned fix, affected files/docs, test plan, rollback plan, evidence to collect, and any claim-boundary update.
9. **Track status.**
   - Track each finding through an allowed status value: `OPEN`, `TRIAGED`, `ACCEPTED_RISK`, `IN_PROGRESS`, `FIXED_PENDING_RETEST`, `CLOSED_VERIFIED`, or `REJECTED_WITH_REASON`.
10. **Re-test and collect evidence.**
    - Collect objective retest evidence before marking remediation complete, especially for critical/high findings or claim-affecting findings.
11. **Close finding only after evidence exists.**
    - Do not close a finding by assertion. Closure requires evidence, rationale, and claim wording updates where applicable.
12. **Update final validation status.**
    - Update external validation status only from explicit reviewer outcome text. Do not infer approval, certification, or validation from silence.
