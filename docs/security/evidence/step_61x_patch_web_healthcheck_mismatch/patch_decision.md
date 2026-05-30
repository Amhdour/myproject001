# Patch Decision

## Options considered

| Option | Decision | Rationale |
|---|---|---|
| Option A: configure Next.js to listen on `0.0.0.0` | Not selected as the primary Step 61X patch | `web/Dockerfile` already documents and sets `HOSTNAME="0.0.0.0"` for the standalone Next.js runner, but the Oracle staging evidence still showed loopback healthcheck mismatch. Changing only that setting does not directly remediate the located compose healthcheck source. |
| Option B: change the healthcheck to probe a container hostname/IP-compatible interface | Selected | A dynamic call to `require('os').hostname()` avoids hardcoding a container IP or container ID and matches the interface family that was reachable in Oracle staging. |
| Option C: replace with a service-local endpoint that reflects web readiness | Deferred | A dedicated readiness endpoint could be stronger, but it would require app-level endpoint design and validation beyond the single SIM-F-003 remediation item. |
| Option D: document only | Not selected | The healthcheck source was located and can be safely patched at repo level. |

## Selected fix

Use the container's runtime hostname as the default probe host:

```text
process.env.WEB_HEALTHCHECK_HOST || require('os').hostname()
```

The patch keeps an operational override (`WEB_HEALTHCHECK_HOST`) for unusual runtimes, avoids hardcoding `10.0.3.11`, avoids hardcoding container hostname `97bb92b88641`, and should survive redeploys because Docker updates the runtime hostname automatically.

## Claim boundary

The patch is prepared locally. Oracle VPS retest has not been executed by Codex, so this step does not claim that the Oracle `web_server` Docker health status is fixed.
