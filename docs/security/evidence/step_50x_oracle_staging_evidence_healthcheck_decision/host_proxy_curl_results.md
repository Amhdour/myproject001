# Host / Proxy Curl Results

## Observed host/proxy responses

| Command target | Result |
|---|---|
| `http://localhost` | `404 Not Found` |
| `http://127.0.0.1` | `404 Not Found` |
| `http://localhost:8000` | `302 Found` redirect to `/login` |
| `http://127.0.0.1:8000` | `302 Found` redirect to `/login` |
| `http://localhost:8088` | `200 OK` nginx default page |

## Interpretation

- The host/proxy layer is responding.
- Port `80` returns `404 Not Found` because no matching route/domain is configured there.
- Coolify login is reachable on port `8000` and redirects to `/login`.
- The nginx health container is reachable on port `8088` and returns `200 OK`.

## Claim boundary

Host/proxy evidence is PARTIAL GO. It does not prove a configured application domain/TLS route or full live app GO.
