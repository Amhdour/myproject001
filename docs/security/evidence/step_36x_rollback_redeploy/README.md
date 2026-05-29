# Step 36X Rollback/Redeploy Evidence

## Status

Step 36X status is **VALIDATED for minimal rollback/redeploy only**.

This validation applies only to the minimal `step34x-health` nginx deployment on the VPS `rag-agent-security-staging-v2`. It does not validate full Onyx rollback, database rollback, production rollback readiness, enterprise rollback readiness, external validation, or compliance certification.

## Evidence scope

| Field | Value |
|---|---|
| VPS | `rag-agent-security-staging-v2` |
| Validated app | Minimal `step34x-health` nginx deployment |
| Image | `nginx:alpine` |
| Port binding | `0.0.0.0:8088->80/tcp` |
| Before-stop health | `HTTP/1.1 200 OK`; `Server: nginx/1.31.1` |
| Stop result | No `step34x-health` output from `sudo docker ps -a | grep step34x-health || true` |
| After-stop health | `curl: (7) Failed to connect to localhost port 8088 after 0 ms: Couldn't connect to server` |
| Redeployed container ID | `be0db257c549` |
| Redeployed container name | `step34x-health-pdegb9g6obvbmmayzijiifjt-155959540822` |
| After-redeploy health | `HTTP/1.1 200 OK`; `Server: nginx/1.31.1`; `Content-Type: text/html`; `Content-Length: 896` |

## Evidence files

- `rollback_execution.md` — before-stop, after-stop, and after-redeploy command evidence.
- `rollback_go_no_go.md` — scoped go/no-go decision for Step 36X.
- `evidence_checklist.md` — checklist of evidence items and non-claims.
- `final_status.md` — final Step 36X percentage and claim boundary.
- `limitations.md` — explicit non-claims and blocked areas.
- `rollback_commands.md` — commands captured for the rollback/redeploy validation.

## Current conclusion

- Minimal `step34x-health` rollback/redeploy: **VALIDATED**.
- Full Onyx rollback: **NO-GO / RESOURCE-BLOCKED**.
- Database rollback: **NOT VALIDATED**.
- Production rollback readiness: **NO-GO**.
- Enterprise rollback readiness: **NO-GO**.
- External validation: **PENDING**.
- Compliance certification: **NOT CLAIMED**.
