# Retrieval Path Live Patch Go/No-Go (Step 17D)

## decision
- **Enforce mode:** **NO-GO**.
- **Future monitor-only integration:** **GO** (limited scope only).

## rationale
Isolated controls and hooks exist, but no runtime retrieval-path integration evidence exists yet. Enforce mode would be premature and is prohibited until monitor-only and shadow-deny evidence is complete.

## allowed next implementation scope
- Live-path patching only for **monitor-only** hook insertion.
- Non-blocking decision capture only.
- No candidate blocking/denial in runtime responses.

## forbidden implementation scope
- No enforce-mode activation.
- No production blocking behavior.
- No runtime retrieval ACL denial wired into user-facing responses.
- No modifications outside approved retrieval integration patch points.

## feature flag defaults
- Default must remain `disabled` or `monitor_only`.
- Enforce path must remain off by default and operationally gated.

## rollback requirement
- One-step rollback must exist: set mode to `disabled`.
- If needed, bypass hook path entirely with neutral behavior fallback.

## test requirements
- Baseline isolated retrieval tests pass.
- Monitor-only integration tests must prove no user-visible blocking.
- Regression checks required for retrieval result stability in disabled mode.

## evidence requirements
- Monitor-only decision samples.
- Non-blocking assertion outputs.
- Rollback rehearsal output.
- Traceability update covering monitor-only live patch.

## reviewer checklist
- [ ] Scope limited to monitor-only.
- [ ] Enforce mode unchanged and no-go status preserved.
- [ ] Flag defaults remain safe.
- [ ] Evidence artifacts attached.
- [ ] Rollback path verified.

## merge checklist
- [ ] No runtime enforcement enabled.
- [ ] No unrelated runtime/search/web/worker/deploy changes.
- [ ] Tests pass and outputs captured.
- [ ] Execution tracker and evidence report updated.

## explicit enforcement hold
No production enforcement may be enabled until a **separate, evidence-backed approval** explicitly authorizes enforce mode.
\n\n## Step 17E Update (2026-05-27)\n- Added first live retrieval monitor-only hook at  after existing retrieval guard result handling.\n- Mode is disabled by default (), and monitor_only is the only live-enabled behavior for this step.\n- Enforce mode remains NO-GO and is not wired into live retrieval path.\n- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.\n

## Step 17E Update (2026-05-27)
- Added first live retrieval monitor-only hook at `backend/onyx/context/search/retrieval/search_runner.py` after existing retrieval guard result handling.
- Mode is disabled by default (`default_retrieval_integration_config`), and monitor_only is the only live-enabled behavior for this step.
- Enforce mode remains NO-GO and is not wired into live retrieval path.
- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.


## Step 17F Update (2026-05-27)
- Retrieval monitor-only validation completed.
- Disabled mode preserves retrieval behavior.
- Monitor-only mode preserves retrieval behavior.
- Enforce mode remains NO-GO/inactive.
- Retrieval blocking/filtering/denial remains disabled in live path.

## Step 18A Gate Update (2026-05-27)
- Shadow-deny and enforce modes remain blocked until the Step 18A retrieval security test suite is implemented and passing with evidence.

## Step 18B Guardrail Confirmation (2026-05-27)
- Shadow-deny remains blocked.
- Enforce mode remains blocked.
- Future modes require implemented and passing evidence before any activation consideration.
