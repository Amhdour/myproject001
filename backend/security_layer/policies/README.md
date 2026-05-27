# Minimal Isolated Policy Engine (Step 12B)

This module contains a minimal, isolated policy engine implementation under `backend/security_layer/policies`.

## Important status

- This engine is **not wired into runtime request paths**.
- There is **no active production enforcement**.
- Backend APIs are **not modified to enforce these policies**.

## Supported features

- Typed policy models (dataclasses + enums)
- Policy file loading from JSON (and YAML when `PyYAML` is available)
- Validation of required fields/effects/scope/rules
- Deterministic minimal evaluation with deny precedence
- Explainable decision string and policy content hashing

## Limitations

- Isolated only (no runtime integration)
- No API enforcement behavior
- Minimal matcher supports action plus required context key presence only
- YAML loading depends on environment dependency availability

## Test command

```bash
python -m pytest backend/security_layer/tests -q
```

## Non-claim statement

This implementation is a development milestone only and does **not** claim production readiness.
