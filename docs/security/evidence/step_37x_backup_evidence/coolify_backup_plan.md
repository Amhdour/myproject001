# Coolify Backup Plan

## Persistent Data Path

The primary Coolify persistent data path for this staging environment is:

```text
/data/coolify/
```

This path is the planned filesystem target for Coolify configuration and state backup evidence.

## Coolify `.env` Warning

The Coolify environment file path is:

```text
/data/coolify/source/.env
```

This path is documented as a reference only. Values from this file must not be printed, copied into evidence, or committed to git.

## Secret Storage

- Store the Coolify `.env` contents securely outside the server, for example in a password manager or secret manager.
- Never commit `.env` to git.
- Never include secret values in evidence files.
- When application-level environment variables are documented, export or record names only, not values.

## Recovery Dependencies

Recovery requires, at minimum:

1. A fresh VPS.
2. Docker installed and running.
3. Coolify installed or restorable.
4. Restored `/data/coolify/` data/config as appropriate.
5. Secret values restored from a secure off-repo secret store.
6. GitHub App or repository integration reconnected if needed.
7. Minimal `step34x-health` redeployed.
8. Local health check rerun against `http://localhost:8088`.

## Status

- Coolify backup plan: **COMPLETE**.
- Coolify backup execution: **PENDING**.
- Coolify restore drill: **PENDING**.
