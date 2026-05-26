# Known Limitations

## Purpose
Track known blockers and constraints affecting security-readiness verification.

## Scope
Limitations impacting local baseline validation, remote sync verification, and readiness assertions.

## Status
draft

## Owner
AI Trust & Security Readiness Engineer

## Evidence Required
- Command outputs demonstrating failure conditions.
- Logs/screenshots of dependency and network blockers.
- Follow-up remediation records.

## Related Links
- [Baseline Commit](../../BASELINE_COMMIT.md)
- [Baseline Validation](./baseline_validation.md)
- [Architecture Discovery](./architecture_discovery.md)
- [Patch Points](./patch_points.md)
- [Known Limitations](./known_limitations.md)


## Current Known Limitations
1. **Baseline blocker**: `fastapi_users` missing during backend unit collection.
2. **Remote verification blocker**: GitHub fetch unavailable due HTTP 403 tunnel error (`git fetch origin --prune` against `https://github.com/Amhdour/myproject001.git`).
3. **Readiness constraint**: No production readiness is claimed while the above blockers remain unresolved.

## TODO Future Implementation Evidence
- [ ] Capture successful baseline run after dependency resolution.
- [ ] Capture successful remote sync verification after network/auth issue resolution.
- [ ] Add dated closure entries per limitation.

## Non-Claim Statement
This document records unresolved limitations and does **not** assert that baseline verification, remote sync integrity, or production readiness has been achieved.
