# Evidence Standard

## Purpose
Define a consistent evidence format for security-readiness documentation so that claims, validations, and review outcomes are reproducible, auditable, and traceable.

## Scope
This standard applies to documentation and evidence artifacts under `docs/security/` and `docs/security/evidence/`. It does not implement controls and does not change application behavior.

## Evidence Principles
1. **Traceable:** Every artifact links to requirement, risk, and patch-point IDs where applicable.
2. **Reproducible:** Evidence includes exact command/action context and commit SHA.
3. **Minimal-claim:** Artifacts report observed facts only.
4. **Reviewable:** Evidence contains clear reviewer and status metadata.
5. **Sanitized:** Sensitive values are redacted before publication.

## Valid Evidence Types
- Command output captures.
- Test execution summaries and logs.
- Architecture/patch-point mapping records.
- CI artifact references and checksums.
- Review and sign-off records.
- Staging and launch-gate validation records.
- Demonstration attack evidence packages (documentation-only unless otherwise approved).

## Invalid Evidence Types
- Unattributed screenshots or logs with no metadata.
- Claims without linked artifact path.
- Edited output without redaction markers.
- Personal or private notes that cannot be independently reviewed.
- Production-readiness assertions without gate evidence.

## Evidence Naming Convention
Use lowercase snake_case file names:
- `<category>_<yyyy-mm-dd>_<short_descriptor>.<ext>` for dated files.
- `<category>_template.md` for templates.

Recommended category prefixes: `baseline`, `architecture`, `patch_point`, `requirement`, `risk`, `traceability`, `ci`, `staging`, `launch_gate`, `demo_attack`, `review`.

## Directory Structure
- `docs/security/evidence/` root for evidence artifacts.
- `docs/security/evidence/templates/` for canonical templates.
- `docs/security/evidence/<step_or_topic>/` for step-specific artifacts.

## Required Metadata
Each evidence record should include:
- Evidence ID.
- Linked requirement ID(s).
- Linked risk ID(s).
- Linked patch-point ID(s).
- Environment name.
- Commit SHA.
- Operator.
- Timestamp (UTC).
- Command or action performed.
- Expected result.
- Actual result.
- Status (`pass`, `fail`, `skipped`).
- Raw artifact path.
- Redaction status.
- Reviewer.
- Notes.

## Redaction Rules
- Replace secrets and tokens with `[REDACTED:<type>]`.
- Preserve enough surrounding context for reviewer validation.
- Mark whether redaction occurred and who performed it.
- Do not delete lines silently; use explicit redaction markers.

## Secret-Handling Rules
- Never store plaintext API keys, tokens, passwords, or private credentials.
- If command output includes secret material, sanitize before committing.
- Prefer referencing secure secret stores rather than embedding values.

## Timestamp Requirements
- Use UTC timestamps in ISO-8601 format, e.g., `2026-05-26T14:35:00Z`.
- Capture start/end ranges for long-running validations when relevant.

## Environment Naming
Use one of: `local-dev`, `ci`, `staging`, `pre-prod`, `prod`.
If a custom environment is needed, define it in the artifact notes.

## Command-Output Capture Rules
- Include exact command text.
- Capture exit status where possible.
- Save raw outputs in evidence paths and summarize in markdown.
- Distinguish between environment blocker vs. functional failure.

## Screenshot Rules
- Include capture timestamp and environment.
- Annotate what is being demonstrated.
- Ensure secrets and personal data are obscured.
- Link screenshot file path from the evidence record.

## CI Artifact Rules
- Store build/test job identifiers and run URLs when available.
- Record artifact filename/checksum references.
- Note retention window from CI platform policy.

## Demo Attack Evidence Rules
- Document test objective, scope, and authorization context.
- Record tools and commands used.
- Capture expected vs. observed behavior.
- Include explicit non-production statement for simulated scenarios.

## Staging Evidence Rules
- Require environment label `staging`.
- Include deployed commit SHA and configuration profile reference.
- Record pass/fail/skipped outcomes for planned validations.

## Launch Gate Evidence Rules
- Aggregate prerequisite evidence IDs.
- Record approvers, decision, and date.
- Include explicit unresolved blocker list.
- Require no-readiness-claim if blockers remain.

## Retention Expectations
- Keep evidence artifacts for the project lifecycle or according to organization policy.
- Do not delete historical evidence without documented archival reason.

## Review Requirements
- At least one reviewer must verify metadata completeness and traceability links.
- Reviews should confirm redaction status and non-claim wording where applicable.
- Evidence acceptance should be documented with reviewer name and timestamp.

## Non-Claim Statement
This standard defines documentation and evidence formatting only. It does not indicate security control implementation, control effectiveness, compliance certification, or production readiness.
