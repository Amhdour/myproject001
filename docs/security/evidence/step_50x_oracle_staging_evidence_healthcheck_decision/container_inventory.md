# Container Inventory Summary

## Observed container state

| Service / container role | Observed state |
|---|---|
| MinIO | Running after manual staging diagnostic addition. |
| `api_server` | Healthy after MinIO file-store fix and service restart. |
| `web_server` | Running, but Docker-unhealthy. |
| `background` | Running. |
| Postgres | Healthy. |
| Redis | Running. |
| OpenSearch | Running. |
| Model server containers | Healthy. |
| Coolify / Traefik | Running / healthy. |
| nginx health container | Responding `200 OK` on host port `8088`. |

## Claim boundary

This inventory supports an Oracle staging PARTIAL GO only. It is not a full production health claim, not a full live app GO claim, and not an enterprise production-candidate claim.
