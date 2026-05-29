# Step 34X Oracle Free VPS Evidence

## Purpose

This evidence bundle records Step 34X live VPS staging work for the Oracle Free Tier Coolify environment and distinguishes validated infrastructure setup from the failed full-Onyx deployment.

## Environment

| Field | Value |
|---|---|
| Provider | Oracle Cloud Free Tier |
| Operating system | Ubuntu 22.04 ARM64 |
| Public IP | `84.8.223.251` |
| RAM | Approximately 5.8 GiB |
| Swap | 8 GiB active |
| Disk | Approximately 193 GB |
| Coolify project | `rag-agent-security-minimal-staging` |

## Evidence files

- `access_check.md` — VPS access status.
- `vps_environment.md` — VPS capacity and environment summary.
- `coolify_installation.md` — Coolify/GitHub/repository setup status.
- `repository_remote.md` — Repository import and target branch/compose information.
- `full_onyx_resource_blocker.md` — Failed full-stack Onyx deployment evidence and resource-blocker decision.
- `minimal_staging_deployment.md` — Minimal nginx deployment target and pending redeploy status.
- `secret_injection.md` — Secret handling boundary.
- `smoke_tests.md` — Planned post-redeploy smoke-test commands.
- `go_no_go.md` — Step 34X go/no-go status.
- `limitations.md` — Explicit evidence limitations and non-claims.
- `deployment_run.md` — Earlier deployment-run evidence retained for audit continuity.

## Current conclusion

- Full Onyx: **RESOURCE-BLOCKED** on this Oracle Free Tier VPS class.
- Minimal staging: **READY FOR REDEPLOY** using `deployment/docker_compose/docker-compose.step34x-minimal.yml`.
- Production readiness: **NO-GO**.

## Exact next Coolify action

Set compose path to `deployment/docker_compose/docker-compose.step34x-minimal.yml` and deploy.
