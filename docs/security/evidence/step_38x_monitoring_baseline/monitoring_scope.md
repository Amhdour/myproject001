# Step 38X Monitoring Scope

## Baseline Monitoring Targets

Step 38X baseline monitoring evidence should cover the following targets for the Oracle VPS + Coolify minimal staging environment.

| Target | Evidence Needed | Status |
|---|---|---|
| VPS uptime | `uptime` output showing current host uptime and load averages. | PENDING USER EXECUTION |
| CPU/load | `uptime` load averages and Docker resource usage from `sudo docker stats --no-stream`. | PENDING USER EXECUTION |
| RAM and swap | `free -h` output showing memory and 8 GiB active swap state. | PENDING USER EXECUTION |
| Disk usage | `df -h` output showing filesystem capacity and usage for the about 193 GB disk. | PENDING USER EXECUTION |
| Docker running containers | `sudo docker ps` output showing running containers, including `step34x-health` if still deployed. | PENDING USER EXECUTION |
| Docker resource usage | `sudo docker stats --no-stream` output showing CPU, memory, network, block I/O, and PIDs. | PENDING USER EXECUTION |
| Coolify container health | Coolify container status, health output, deployment logs, or screenshot if available. | PENDING USER EXECUTION |
| Minimal app health endpoint | `curl -I http://localhost:8088` output showing expected HTTP response. | PENDING USER EXECUTION |
| Public endpoint check if available | Optional `curl -I http://84.8.223.251:8088` output from an allowed network path. | OPTIONAL / PENDING USER EXECUTION |
| Deployment logs from Coolify | Coolify deployment or application logs for the minimal `step34x-health` app. | PENDING USER EXECUTION |
| Backup/restore status from Step 37X | Explicit record that backup plan is complete while actual backup/restore execution remains pending unless separately captured. | PLAN COMPLETE / EXECUTION PENDING |

## Scope Boundary

This scope is intentionally minimal. It captures point-in-time operational visibility only. It does not establish production monitoring readiness, enterprise observability readiness, alerting readiness, uptime/SLO/SLA readiness, external validation, or compliance certification.
