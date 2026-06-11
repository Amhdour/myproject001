# Production Readiness Limitations

## Purpose
Document blockers to production/security-audit credibility for RAG security claims.

## Commands or search methods used
- Consolidated from repository inspection and local test outcomes.

## Files found
See all topic inventory files.

## Relevant code paths found
- Retrieval code and tests exist, but live deployment evidence was not found.

## Findings
Current blockers/limitations:
- Missing full live integration test execution for RAG retrieval ACL behavior.
- Missing staging validation artifacts.
- Missing deployment evidence.
- Missing external audit validation.
- Missing proof of CI pass status for this branch.
- Missing comprehensive retrieved-content prompt-injection defenses and tests.
- Missing complete citation leakage negative tests against live answer generation.
- Missing proof of production audit-log durability/retention/export.
- Missing proof of production telemetry dashboards/alerts for RAG security decisions.
- Missing incident-response/runbook evidence specific to RAG retrieval security in this review.
- Missing rollback validation for any new or existing RAG security enforcement changes in this review.

## Gaps
This review did not attempt to remediate these limitations; it documents them for future work.

## Claim boundary
The repository may contain additional controls not inspected or not executed here, but they cannot be used for strong claims until evidence is captured.
