# Optional AgentShield-Style RAG Scanner Adapter

This repository keeps the proven local heuristic RAG prompt-injection scanner as the default provider. The AgentShield path is an optional adapter only; it is loaded at runtime when configured and when a compatible dependency is installed in the environment.

## Configuration

```bash
SECURITY_RAG_INJECTION_SCANNER_ENABLED=true
SECURITY_RAG_SCANNER_PROVIDER=heuristic        # default, proven local scanner
SECURITY_RAG_SCANNER_PROVIDER=llamafirewall    # optional runtime-loaded adapter
SECURITY_RAG_SCANNER_PROVIDER=agentshield      # optional runtime-loaded adapter
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=heuristic  # default
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=monitor
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=deny
```

## Dependency behavior

- The full AgentShield repository is not vendored.
- AgentShield is not imported when the heuristic provider is used.
- If no compatible AgentShield-style module is installed, or if the installed backend cannot be called through a recognized scan/evaluate/detect/classify entry point, the adapter does not crash the RAG scanner path.
- Fallback behavior is controlled by `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER`:
  - `heuristic`: run the proven local heuristic scanner and mark `fallback_used=true`.
  - `monitor`: preserve context and emit a monitor scanner-failure result.
  - `deny`: remove the chunk through a deny scanner-failure result.

## Safe evidence fields

The scanner evidence allowlist includes only metadata that is safe for Langfuse/OpenTelemetry export:

- `scanner_provider`
- `scanner_backend_available`
- `scanner_backend_version`
- `scanner_decision`
- `risk_type`
- `risk_score`
- `drift_score` when the backend provides it
- `fallback_used`

Raw retrieved chunk text, prompts, full documents, scanner debug payloads, and document content are intentionally excluded.

## Claim boundary

The local heuristic scanner is proven by the targeted tests and demo in this evidence package. The LlamaFirewall/PurpleLlama adapter path is optional. The AgentShield adapter path is optional. Real AgentShield backend behavior is not proven unless a compatible dependency is installed and the targeted tests/demos are rerun in that environment. This is not a production-readiness claim.
