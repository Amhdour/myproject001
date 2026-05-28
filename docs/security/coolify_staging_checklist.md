# Coolify Staging Checklist

## Required Pre-Deployment Checks
- [x] Required Step 29X documentation paths prepared.
- [x] Isolated staging helper package prepared.
- [x] Focused staging tests planned and run.
- [x] Full security-layer tests planned and run.
- [x] Environment template uses placeholders only.
- [x] Evidence folder prepared.
- [ ] Real Coolify staging deployment executed by an approved operator.
- [ ] Smoke tests executed against a real staging deployment.

## Runtime Mode Checks
- [x] Enforce mode is not enabled.
- [x] Shadow-deny runtime mode is not enabled.
- [x] Live blocking is not enabled.
- [x] Live filtering is not enabled.
- [x] Application behavior is not changed.
- [x] No production-readiness claim is made.

## Evidence Capture Checks
- [x] Test output captured in the evidence bundle.
- [x] Test exit code captured in the evidence bundle.
- [x] Live staging execution is explicitly marked pending when no deployment is
      performed.
- [x] Remote sync limitation is documented when no remote sync verification is
      performed.
