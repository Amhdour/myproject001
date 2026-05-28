# Shadow-Deny Rollout Gates (Planned)

| gate ID | purpose | required inputs | required tests | required evidence | pass criteria | fail criteria | current status | blocker notes |
|---|---|---|---|---|---|---|---|---|
| SD-1 | monitor-only evidence complete | monitor-only reports + validations | SDP-005,SDP-006 | evidence index links | all required monitor-only evidence present | missing/uncorrelated monitor evidence | planned | monitor-only coverage limited |
| SD-2 | feature flags documented | flag catalog | SDP-001 | shadow_deny_feature_flags.md | all required flags documented with disabled defaults | missing flag/default/owner/gate | planned | none |
| SD-3 | rollback plan documented | rollback workflow + runbook | SDP-012 | rollout plan + rollback evidence template | documented reversible rollback steps | rollback path incomplete | planned | rollback drill pending |
| SD-4 | non-leakage tests passing | deny outputs + schema rules | SDP-007 | non-leakage report | no sensitive data leakage findings | any leakage finding | planned | tests not executed yet |
| SD-5 | safe denial tests passing | denial category model | SDP-002,SDP-003,SDP-007 | safe denial report | live effect stays no_change and safe categories valid | live effect changed or unsafe denial | planned | tests not executed yet |
| SD-6 | audit/finding/metric evidence present | sink integrations + IDs | SDP-008,SDP-009,SDP-010 | correlated sink artifacts | all three sinks correlated per sample set | missing sink artifacts or broken correlation | planned | shared sink readiness incomplete |
| SD-7 | CI test evidence present | CI logs/results | SDP-001..SDP-021 | CI evidence package | planned suite executed with passing required subset | missing CI evidence | planned | CI plan not run |
| SD-8 | staging dry-run complete | staging dry-run output | SDP-013..SDP-021 | staging report | all families dry-run with no live impact | live impact or incomplete run | planned | staging run pending |
| SD-9 | false-positive review complete | divergence tickets | SDP-011 | FP review records | FP threshold met + approvals recorded | unresolved FP backlog | planned | review workflow pending |
| SD-10 | approval to activate shadow-deny | SD-1..SD-9 pass + signoff | SDP-020,SDP-021 | approval artifact | formal approval recorded | missing gate pass or approval | planned | blocked from activation |
