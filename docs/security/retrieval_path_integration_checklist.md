# Retrieval Path Integration Checklist (Step 17B)

## pre-implementation checks
- [ ] Step 16B/16C isolated retrieval ACL controls verified present.
- [ ] Step 17A patch-point map reviewed.
- [ ] Step 17B scope confirmed as planning-only.

## branch readiness
- [ ] Working branch is `retrieval-path-integration-plan`.
- [ ] No unrelated file deltas present.

## dependency checks
- [ ] `backend/security_layer/retrieval/models.py` available.
- [ ] `backend/security_layer/retrieval/validators.py` available.
- [ ] `backend/security_layer/retrieval/controls.py` available.

## feature flag checks
- [ ] Default mode planned as `disabled` or `monitor_only`.
- [ ] Mode transitions documented: monitor -> shadow -> enforce.
- [ ] Emergency rollback mode documented.

## context builder checks
- [ ] Subject context extraction fields listed.
- [ ] Tenant/workspace extraction fields listed.
- [ ] Missing subject/tenant safe-handling behavior defined.

## monitor-only mode checks
- [ ] Decision hook planned for non-blocking operation.
- [ ] Decision logging and audit mapping captured.

## shadow-deny mode checks
- [ ] Shadow decision capture planned.
- [ ] User-visible blocking explicitly disabled in shadow mode.

## enforce-mode checks
- [ ] Enforce gating criteria documented.
- [ ] Candidate filter + citation/context boundary checks mapped.

## audit/finding/metric checks
- [ ] Audit event schema expectations captured.
- [ ] Findings mapping for unsafe patterns documented.
- [ ] Metrics list and counters documented.

## safe denial checks
- [ ] Safe denial category mapping included.
- [ ] No identifier-leak rule noted for deny outputs.

## rollback checks
- [ ] Mode rollback path documented.
- [ ] Rollback verification tests planned.

## test command checks
- [ ] Unit/integration test targets identified for future implementation.
- [ ] CI security-gate checks planned.

## evidence checks
- [ ] Phase inventory evidence file prepared.
- [ ] Checklist summary evidence file prepared.
- [ ] Traceability/test-plan evidence files prepared.

## PR review checks
- [ ] Documentation-only diff confirmed.
- [ ] No runtime retrieval enforcement wiring introduced.

## merge readiness checks
- [ ] Step 17B execution tracker updated.
- [ ] Remaining blockers documented.
