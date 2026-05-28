# Enforce-Mode Blast-Radius Plan

## Initial allowed scope: none
No tenant, workspace, user/group, control family, or stage is currently allowed for live enforce mode.

## Future pilot scope rules
Any future pilot must use a tenant allowlist, workspace allowlist, user/group allowlist, control-family allowlist, and stage allowlist. Broad scope blocks activation.

## Allowlist models
- Tenant allowlist model: one explicitly approved placeholder tenant maximum during future pilot.
- Workspace allowlist model: one explicitly approved placeholder workspace maximum.
- User/group allowlist model: a small approved subject/group cohort only.
- Control-family allowlist model: one control family at a time.
- Stage allowlist model: staging before production; production requires separate approval.

## Thresholds
- Deny-rate threshold: exceedance triggers rollback.
- False-positive threshold: exceedance triggers rollback and review.
- Error-rate threshold: exceedance triggers rollback.
- Latency threshold: exceedance triggers rollback.

## Rollback conditions
Automatic rollback conditions include threshold breaches, telemetry gaps, unexpected denial, leakage, or safety-test failure. Manual rollback conditions include owner request, incident response request, compliance request, or ambiguous user impact.

## Emergency kill-switch behavior
The kill switch must force no blocking/no filtering and preserve audit, finding, and metric evidence.

## Post-activation observation period
Any future pilot requires continuous observation for deny rate, false positives, errors, latency, user impact, and telemetry delivery.

## Known limitations
This plan is not active and does not enable enforce mode.
