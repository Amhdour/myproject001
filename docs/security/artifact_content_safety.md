# Artifact Content Safety Rules (Planned)

Status: planned

- allowed artifact types
- forbidden artifact types
- forbidden raw secrets
- forbidden credential/token/API-key/private-key/password patterns
- forbidden tenant internals
- forbidden policy internals
- forbidden raw connector secrets
- unauthorized document/chunk text detection
- cross-tenant data detection
- sensitive-data placeholder strategy
- generated code safety checks
- path traversal checks for archives
- dangerous command checks
- unsafe URL checks
- prompt-injection marker checks
- poisoning marker checks
- max size checks
- scan-before-release expectations
- quarantine expectations
- redaction expectations
- evidence expectations
- known limitations

All items above are design-only and not wired into live behavior in this step.


## Step 23C Update (2026-05-28)
- Isolated artifact safety validation cleanup completed for controls/tests/docs/evidence only.
- No live artifact/export/download/sandbox/tool/MCP/retrieval/vector/cache integration changed.
- Enforce and shadow-deny remain inactive.
