# Optional External Red-team Evidence Foundation

This directory contains a lightweight, fixture-based evidence foundation for optional PyRIT and garak red-team tooling.
It does not make PyRIT or garak hard dependencies and does not claim production readiness.

## Contents

- `fixtures/`: sanitized PyRIT-style campaign and garak-style report inputs.
- `redteam_summary.md`: generated fixture-based findings summary.
- `findings_to_controls.md`: generated mapping from finding categories to existing controls.
- `reproduction_commands.md`: local commands for reproducing fixture parsing.
- `limitations.md`: explicit limitations and claim boundary.

## Evidence boundary

Lightweight fixture-based PyRIT and garak evidence foundation only. External red-team tooling is optional, no production readiness is claimed, and true PyRIT/garak execution is not proven unless dependency-backed runs occur.
Raw prompts, retrieved context, model outputs, tenant content, and secrets are intentionally not exported in these artifacts.
