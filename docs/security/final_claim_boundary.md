# Final Claim Boundary

## Allowed Claims

- Sanitized partner-demo evidence is organized for review.
- Isolated final-review helper models and decision helpers are covered by focused tests.
- Retrieved-content prompt-injection detection is implemented with focused tests, synthetic demo evidence, redacted audit samples, telemetry samples, and bounded hook-wiring proof.
- Runtime safety boundaries remain unchanged unless a specific tested mode is explicitly invoked in the focused helper tests.

## Disallowed Claims

- Do not claim production readiness.
- Do not claim enterprise production readiness.
- Do not claim live staging validation without real staging evidence.
- Do not claim external validation completion.
- Do not claim compliance certification.
- Do not claim full prompt-injection defense.
- Do not claim enforce mode, shadow-deny runtime mode, live blocking, or live filtering is enabled.

## Required Status Language

| Area | Status |
|---|---|
| Portfolio presentation readiness | 94% |
| Technical portfolio proof readiness | 88% |
| Client demo readiness | 85% |
| Production-style runtime proof readiness | 70% for bounded retrieval/context hook proof only |
| Enterprise production-candidate readiness | 20% / NO-GO |
| Real production readiness | 8% / NO-GO |
| Production readiness decision | NO-GO |
| Enterprise production readiness decision | NO-GO |
| Live staging validation status | PENDING unless specific evidence exists |
| External validation status | PENDING |
| Compliance certification status | NOT CLAIMED |

## Claim-Boundary Consistency Note

Older evidence files may contain historical step-level percentages. Do not reuse those as current aggregate readiness claims. Use this file and `CLAIM_BOUNDARY.md` for current public-facing wording.
