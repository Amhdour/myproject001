# Oracle VPS Staging Deployment Prep

## Purpose

Prepare a public-safe, open-source staging deployment foundation for the security-readiness project on an Oracle VPS.

## Status

Planning and deployment preparation only. This directory does not prove production readiness, enterprise readiness, compliance, or live runtime control effectiveness.

## Directory Contents

- `bootstrap_ubuntu.sh` - host bootstrap commands for Ubuntu-based Oracle VPS instances.
- `compose.staging.example.yml` - placeholder Docker Compose staging skeleton.
- `.env.staging.example` - public-safe environment example with placeholders only.
- `Caddyfile.example` - HTTPS reverse proxy example with placeholders only.
- `security_boundary.md` - deployment boundary notes for staging.

## Expected Execution Order

1. Provision Oracle VPS.
2. Record VPS inventory in `docs/security/evidence/oracle_vps_staging_foundation/vps_inventory.md`.
3. SSH into the VPS.
4. Create a non-root deployment user.
5. Run the bootstrap script after reviewing it.
6. Create `/opt/myproject001-staging`.
7. Copy compose and Caddy examples into that directory.
8. Create a real `.env.staging` file outside git.
9. Start services privately first.
10. Expose HTTPS only after health checks pass.
11. Record evidence and go/no-go decision.

## Secret Handling

Never commit real `.env` files, SSH keys, API keys, database passwords, model-provider keys, or raw logs containing secrets.

## Readiness Limitation

This deployment prep is a staging foundation only. Live enforcement, CI evidence, telemetry, attack tests, rollback proof, and go/no-go review are still required before any Enterprise production-candidate claim.
