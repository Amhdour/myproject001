# Web Healthcheck Mismatch

## Docker healthcheck target

The Docker healthcheck target for the web container is:

```text
http://127.0.0.1:3000/
```

## Manual probe evidence

| Probe target from inside web container | Result |
|---|---|
| `127.0.0.1:3000` | `ECONNREFUSED` |
| Container hostname `97bb92b88641:3000` | HTTP `200` |
| Container IP `10.0.3.11:3000` | HTTP `200` |

## Socket evidence

Listening socket evidence showed Next.js listening on container IP `10.0.3.11:3000`, not on `127.0.0.1:3000`.

## Decision

The web status is classified as a web healthcheck target mismatch:

- Web app internal reachability: GO by hostname/IP.
- Web Docker health status: NOT GO due to healthcheck mismatch.
- Full live app GO: NOT CLAIMED.

## Next action

Do not patch automatically in Step 50X. A follow-up Step 51X or Step 50Y can safely patch the staging healthcheck target and rerun health evidence.
