# Step 34X Oracle Free VPS Evidence

## Final status

**Step 34X is COMPLETE for minimal live VPS staging evidence.**

This evidence bundle records the completed Step 34X Oracle Free Tier VPS work and separates the validated minimal deployment path from non-validated production, enterprise, external-validation, and compliance claims.

## Environment

| Field | Value |
|---|---|
| Provider | Oracle Cloud Free Tier |
| Operating system | Ubuntu 22.04 ARM64 |
| Public IP | `84.8.223.251` |
| Coolify status | Installed and healthy |
| GitHub import | Validated |
| Minimal deployment container | `step34x-health` |
| Minimal deployment image | `nginx:alpine` |
| Container binding | `0.0.0.0:8088->80/tcp` |

## Exact evidence summary

- VPS access on Oracle Ubuntu 22.04 ARM64 was validated for Step 34X work.
- Coolify was installed and reported healthy on the VPS.
- GitHub import was validated.
- A minimal live staging deployment was validated with an `nginx:alpine` container named `step34x-health`.
- The minimal container binding was `0.0.0.0:8088->80/tcp`.
- The local health check `curl -I http://localhost:8088` returned `HTTP/1.1 200 OK` with `Server: nginx/1.31.1`.
- Public mobile browser access to `http://84.8.223.251:8088` worked, but was slow.
- Full Onyx deployment remains **RESOURCE-BLOCKED** on this VPS class.

## Evidence files

- `access_check.md` — VPS access status.
- `vps_environment.md` — VPS capacity and environment summary.
- `coolify_installation.md` — Coolify/GitHub/repository setup status.
- `repository_remote.md` — Repository import and target branch/compose information.
- `full_onyx_resource_blocker.md` — Failed full-stack Onyx deployment evidence and resource-blocker decision.
- `minimal_staging_deployment.md` — Validated minimal nginx deployment status.
- `secret_injection.md` — Secret handling boundary.
- `smoke_tests.md` — Minimal staging smoke-test evidence and pending external validation boundary.
- `go_no_go.md` — Step 34X go/no-go status.
- `limitations.md` — Explicit evidence limitations and non-claims.
- `deployment_run.md` — Earlier deployment-run evidence retained for audit continuity.
- `final_status.md` — Final Step 34X completion status, percentage, and non-claims.

## Current conclusion

- Step 34X minimal live VPS staging evidence: **COMPLETE**.
- Minimal staging: **VALIDATED** for the nginx health container only.
- Full Onyx: **RESOURCE-BLOCKED** on this Oracle Free Tier VPS class.
- Production readiness: **NO-GO**.
- Enterprise readiness: **NO-GO**.
- External validation: **PENDING**.
- Compliance certification: **NOT CLAIMED**.

## Explicit non-claims

- This evidence does not claim full Onyx production readiness.
- This evidence does not claim enterprise readiness.
- This evidence does not claim compliance certification.
- This evidence does not claim completed independent external validation.
- This evidence validates only the minimal live VPS staging path, not the full Onyx runtime.
