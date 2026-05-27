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
