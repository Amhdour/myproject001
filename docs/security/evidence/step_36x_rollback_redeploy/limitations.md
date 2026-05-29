# Step 36X Limitations

## Scope limitation

This Step 36X validation applies only to the minimal `step34x-health` nginx rollback/redeploy path on `rag-agent-security-staging-v2`.

## Explicit non-claims

- It does not validate full Onyx rollback.
- It does not validate database rollback.
- It does not validate production rollback readiness.
- It does not validate enterprise rollback readiness.
- It does not validate public endpoint reachability because no public curl evidence was provided.
- It does not provide external validation.
- It does not provide compliance certification.

## Readiness boundaries

- Full Onyx rollback: **NO-GO / RESOURCE-BLOCKED**.
- Production rollback readiness: **NO-GO**.
- Enterprise rollback readiness: **NO-GO**.
- External validation: **PENDING**.
- Compliance certification: **NOT CLAIMED**.
