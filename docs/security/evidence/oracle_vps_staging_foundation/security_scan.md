# Oracle VPS Staging Foundation - Security Scan Evidence

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-SECURITY-SCAN
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: local, CI, or Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Operator: AI Trust & Security Readiness Engineer
- Redaction status: required before publication

## Scan Command

```bash
bash deploy/oracle-vps/security_scan_staging_prep.sh
```

## Expected Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Built-in secret-pattern scan | no common private-key/API-token patterns | TBD | pending |
| Env placeholder scan | example env uses placeholder values | TBD | pending |
| Gitleaks scan | pass or skipped if unavailable | TBD | pending/skipped |
| Trivy config scan | pass or skipped if unavailable | TBD | pending/skipped |
| Semgrep scan | pass or skipped if unavailable | TBD | pending/skipped |
| Raw scan outputs created | outputs stored under scan output directory | TBD | pending |
| Redaction review | outputs reviewed before publication | TBD | pending |
| Script exit code | `0` when required checks pass | TBD | pending |

## Raw Output

Paste redacted console output here:

```text
TBD
```

## Output Artifacts

Potential output directory:

```text
docs/security/evidence/oracle_vps_staging_foundation/raw_scan_outputs/
```

Potential files:

- `secret_pattern_scan_<timestamp>.txt`
- `env_placeholder_scan_<timestamp>.txt`
- `gitleaks_<timestamp>.json`
- `trivy_config_<timestamp>.txt`
- `semgrep_<timestamp>.txt`

## Findings Summary

| Finding ID | Tool/check | Severity | Status | Decision |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## Non-Claim Statement

This scan evidence covers staging-prep templates and repository files only. It does not prove live host hardening, runtime security-control effectiveness, enterprise readiness, production readiness, or compliance.
