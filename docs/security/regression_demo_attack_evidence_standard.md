# Step 28X Regression + Demo Attack Evidence Standard

## Valid demo evidence

Valid evidence is generated from synthetic fixtures, isolated scenario definitions, isolated runner output, pytest output, exit codes, and documentation summaries under `docs/security/evidence/regression_demo_attack_bundle/`.

## Invalid demo evidence

Invalid evidence includes real tenant/customer/user/document/credential data, raw prompt text, raw document/chunk text, production logs with sensitive content, live traffic claims, production blocking/filtering claims, or staging attack claims not produced by this bundle.

## Synthetic fixture requirements

Fixtures must use safe IDs such as `tenant_alpha`, `tenant_beta`, `subject_demo`, `workspace_demo`, and `doc_hash_demo`. Fixtures must include markers only and must set explicit indicators that no real data, raw prompts, raw documents, raw chunks, or raw secrets are present.

## Command output requirements

Test evidence must include the exact command output for focused regression/demo tests and full security-layer tests. Output should be sanitized and should not include raw secrets, tokens, emails, prompts, documents, chunks, tenant internals, policy internals, or source internals.

## Exit-code requirements

Evidence must capture exit code `0` for passing focused tests and full security-layer tests. Nonzero exit codes must be reported as blockers.

## Non-leakage proof requirements

Evidence must show that result and summary outputs pass non-leakage validation and that forbidden output patterns are either absent or sanitized.

## Behavior-preservation proof requirements

Evidence must show `live_effect=no_change`, `live_blocking_enabled=False`, `live_filtering_enabled=False`, disabled enforce mode, and disabled shadow-deny runtime mode.

## No-production-claim requirements

Evidence and demo materials must state that this is not production readiness, not live enforcement, not live blocking/filtering, and not staging attack execution.

## Partner-demo evidence boundary

Partner demos may use this package to demonstrate isolated regression/demo coverage and sanitized evidence. They must not represent it as production protection, production readiness, or live attack validation.

## Current limitations

The bundle is isolated, synthetic-only, not connected to staging, not validated under production load, and not based on live traces.
