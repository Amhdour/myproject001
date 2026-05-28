# Enforce Mode Blast Radius Plan (Step 26A)

- Initial allowed scope: **none**.
- Future pilot scope rules: explicit allowlist + owner approval + rollback readiness required.
- Tenant allowlist model: closed-by-default explicit tenant IDs.
- Workspace allowlist model: closed-by-default explicit workspace IDs.
- User/group allowlist model: closed-by-default explicit user/group IDs for pilot.
- Control-family allowlist model: one family at a time for initial pilot.
- Stage allowlist model: staging first, production only after approved pilot evidence.
- Deny-rate threshold: planned max 1% above baseline for pilot cohort.
- False-positive threshold: planned <=0.1% validated by owner review.
- Error-rate threshold: planned no increase above baseline SLO.
- Latency threshold: planned p95 regression <=5% for pilot cohort.
- Automatic rollback conditions: threshold breach, telemetry gap, or non-leakage failure.
- Manual rollback conditions: owner decision, legal/compliance concern, incident signal.
- Emergency kill-switch behavior: immediate disable of global and family enforce flags.
- Post-activation observation period: planned minimum 7 days per pilot stage.
- Known limitations: thresholds are planning assumptions pending implementation and staged measurements.
