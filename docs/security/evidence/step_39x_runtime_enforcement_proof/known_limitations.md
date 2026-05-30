# Step 39X Known Limitations

- The Step 39X hook is a minimal retrieval-facing proof, not full Onyx-wide enforcement.
- Default mode is `disabled`; enforce behavior requires explicit `STEP_39X_RUNTIME_ENFORCEMENT_MODE=enforce`.
- The adapter uses minimal metadata (`tenant_id` and optional `allowed_subject_ids`) for deterministic proof tests; it is not a complete enterprise ACL model.
- The audit sink is structured in-process proof evidence, not a production SIEM integration.
- External validation remains PENDING.
- Compliance certification remains NOT CLAIMED.
- Live staging/cloud validation remains PENDING because no cloud, VPS, K3s, Rancher, Coolify, or real customer deployment was executed for this step.
