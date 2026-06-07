# Red-team Evidence Limitations

- This is a lightweight fixture-based evidence foundation only.
- PyRIT and garak remain optional and are not hard dependencies.
- If PyRIT or garak are unavailable, fixture-based campaign/report parsing still works and documents that limitation.
- True PyRIT execution is not proven unless a dependency-backed PyRIT campaign run is executed in an environment with PyRIT installed.
- True garak execution is not proven unless a dependency-backed garak scanner run is executed in an environment with garak installed.
- This change does not alter OPA, scanner, tool governance, MCP governance, gateway governance, or evaluation behavior.
- This evidence does not claim production readiness.
- Raw prompts, retrieved context, tenant content, model outputs, and secrets are intentionally not exported.

## Adapter status at generation time

- PyRIT dependency available: `False`
- garak dependency available: `False`
- Raw evidence exported: `False`
