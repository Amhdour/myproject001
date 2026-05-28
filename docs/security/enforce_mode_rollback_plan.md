# Enforce Mode Rollback Plan (Step 26A)

- Rollback triggers: threshold breach, false-positive spike, leakage risk, telemetry failure, operational incident.
- Rollback owner: Security readiness owner with SRE on-call support.
- Rollback decision record: required incident/change record with timestamp, owner, rationale, and scope.
- Kill-switch behavior: immediate stop of enforce decisions; system returns to non-blocking behavior.
- Feature-flag disable behavior: disable global enforce flag and all family flags.
- Telemetry preservation: preserve pre/post rollback telemetry for review.
- Audit/finding/metric preservation: retain all deny/event artifacts for investigation.
- User-impact review: assess denied requests and restoration impact.
- Incident-response handoff: if security impact suspected, hand off to IR lead.
- Post-rollback validation: verify no blocking/filtering remains and behavior matches pre-enforce baseline.
- Known limitations: rollback process is planning-only until enforce runtime exists.
