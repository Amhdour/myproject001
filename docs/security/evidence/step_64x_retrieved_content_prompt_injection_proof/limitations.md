# Step 64X Limitations

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Command run | `uv run --group backend --group dev -- python -m pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q` |
| Exit code | `2` in this workspace for full dependency sync attempt |
| Result | Full uv-backed dependency execution was blocked by the current CPython 3.14 environment and locked `onnxruntime==1.20.1` wheel availability. Focused tests were run with available system pytest and repository-local modules. |
| Limitation | No full dependency sync, full backend suite, live Onyx request, live staging redeploy, GitHub Actions run, or external review was completed for this step. |
| Safe claim supported | Environment limitations are documented; no fake CI/staging/external-audit claim is added. |

## Additional limitations

- Detection is deterministic and pattern-based; it is not a complete prompt-injection classifier.
- The hook records redacted metadata and counters only; it does not persist to production audit/telemetry systems.
- Monitor mode preserves chunks while recording the decision.
- Shadow-deny and enforce behavior are focused helper/test behavior; live production enforcement is not claimed.
- The source-wiring test confirms the hook is present in the real search runner source, but this evidence does not prove a live deployed request-path run.
