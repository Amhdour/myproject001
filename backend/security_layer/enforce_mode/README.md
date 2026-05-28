# Enforce-Mode Readiness Simulation

This directory contains isolated planning and gate-simulation helpers for a future enforce mode.

## Boundary

- No runtime enforce activation is implemented here.
- No live blocking or live filtering is enabled.
- No production database, cache, vector database, artifact, retrieval, tool, MCP, ingestion, prompt, worker, web, or deployment state is written.
- Outputs are in-memory simulation records with sanitized summaries and placeholder IDs only.

## Supported simulations

The harness can simulate activation gates for retrieval ACL, vector DB security, cache security, tool authorization, MCP hardening, artifact safety, secure ingestion, safe denial, and audit/finding/metric sinks.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_enforce_mode_models.py backend/security_layer/tests/test_enforce_mode_feature_flags.py backend/security_layer/tests/test_enforce_mode_gates.py backend/security_layer/tests/test_enforce_mode_blast_radius.py backend/security_layer/tests/test_enforce_mode_simulator.py backend/security_layer/tests/test_enforce_mode_controls.py -q
```

## Non-claim statement

This package supports readiness planning and isolated gate simulation only. It does not claim production readiness and does not authorize real enforce activation.
