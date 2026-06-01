# Demo Attack Results

## Demo attack

`demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py`

## Scenario

- Acting subject: `user-a`
- Acting tenant: `tenant-a`
- Authorized candidate: `tenant-a-roadmap`
- Unauthorized candidate: `tenant-b-secret-plan`

## Expected result

The unauthorized `tenant-b-secret-plan` chunk must be removed from the allowed chunk set in enforce mode.

## Expected command

```bash
python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## Expected successful output

```text
PASS: unauthorized cross-tenant retrieval was blocked.
decision=deny reason=retrieval_authorization_failed denied_chunk_count=1
audit_event=retrieval_authorization_failed telemetry=retrieval_acl_decision_total
```

## Current status

`PENDING_EXECUTION_IN_WORKSPACE_OR_CI`

This file records the expected demo-attack evidence format. It must be updated with real command output after local, CI, or staging execution.
