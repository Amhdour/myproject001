# Oracle VPS Staging Foundation - Staging Smoke Test

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-SMOKE-TEST
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Operator: AI Trust & Security Readiness Engineer
- Redaction status: required before publication

## Smoke Test Command

Run from the staging directory on the Oracle VPS, after copying the real compose file and real out-of-git `.env.staging` file:

```bash
STAGING_URL="https://staging.example.com" \
COMPOSE_FILE="compose.staging.yml" \
ENV_FILE=".env.staging" \
bash smoke_test_staging.sh
```

If HTTPS is not ready yet, omit `STAGING_URL` and record the HTTPS check as skipped:

```bash
COMPOSE_FILE="compose.staging.yml" \
ENV_FILE=".env.staging" \
bash smoke_test_staging.sh
```

## Expected Checks

| Check | Expected result | Actual result | Status |
|---|---|---|---|
| Docker Compose available | `docker compose` exists | TBD | pending |
| Compose file exists | `compose.staging.yml` present | TBD | pending |
| Env file exists outside git | `.env.staging` present on VPS only | TBD | pending |
| Compose config renders | config command succeeds | TBD | pending |
| Compose service listing works | `docker compose ps` succeeds | TBD | pending |
| HTTPS endpoint reachable | `curl` succeeds when `STAGING_URL` is set | TBD | pending/skipped |
| Secrets reviewed | output redacted before publication | TBD | pending |
| Script exit code | `0` when required checks pass | TBD | pending |

## Raw Output

Paste redacted output here:

```text
TBD
```

## Exit Code

```text
TBD
```

## Evidence Artifacts

Potential raw artifacts, stored only after redaction review:

- `/tmp/myproject001-staging-compose-rendered.yml`
- `/tmp/myproject001-staging-compose-ps.txt`
- `/tmp/myproject001-staging-http-response.txt`

## Interpretation

- PASS means the staging runtime foundation is reachable enough for deeper deployment validation.
- SKIP on HTTPS is acceptable before DNS/TLS setup, but it blocks public-demo readiness.
- FAIL blocks staging go/no-go until remediated.

## Non-Claim Statement

This smoke test validates staging foundation health only. It does not prove runtime security enforcement, attack resistance, enterprise readiness, production readiness, or compliance.
