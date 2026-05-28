# Real Coolify Staging Evidence Capture Template

## Sanitization Rules

Do not record secrets, domains, IPs, credentials, tokens, SSH keys, API keys, private keys, customer identifiers, or private endpoint values. Replace sensitive values with placeholders such as `<staging-app>`, `<redacted-url>`, `<redacted-commit>`, and `<redacted-operator>`.

## Deployment Evidence

- Real Coolify deployment executed: `yes/no`
- Staging deployment timestamp: `<redacted-or-date-only>`
- Branch deployed: `real-coolify-staging-execution-bundle`
- Commit deployed: `<redacted-or-short-sha>`
- Operator: `<redacted-operator>`
- Deployment result: `passed/failed/pending`
- Sanitized notes: `<summary>`

## Smoke Validation Evidence

- Live staging validation status: `PENDING/PASSED`
- Health check result: `passed/failed/pending`
- Login/authentication smoke result: `passed/failed/pending`
- Core page load smoke result: `passed/failed/pending`
- Security boundary check result: `passed/failed/pending`
- Sanitized logs reviewed: `yes/no`
- Sanitized notes: `<summary>`

## Required Decision Fields

- Partner-demo evidence review decision: `GO`
- Production readiness decision: `NO-GO`
- Enterprise production readiness decision: `NO-GO`
- External validation status: `PENDING`
- Compliance certification status: `NOT CLAIMED`
