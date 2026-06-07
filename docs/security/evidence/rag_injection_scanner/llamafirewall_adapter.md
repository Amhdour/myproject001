# Optional LlamaFirewall/PurpleLlama RAG Scanner Adapter

This repository keeps the proven local heuristic RAG prompt-injection scanner as the default provider. The LlamaFirewall/PurpleLlama path is an optional adapter only; it is loaded at runtime when configured and when a compatible dependency is installed in the environment.

## Configuration

```bash
SECURITY_RAG_INJECTION_SCANNER_ENABLED=true
SECURITY_RAG_SCANNER_PROVIDER=heuristic        # default
SECURITY_RAG_SCANNER_PROVIDER=llamafirewall
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=heuristic  # default
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=monitor
SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=deny
```

## Dependency behavior

- The full PurpleLlama repository is not vendored.
- LlamaFirewall/PurpleLlama is not imported when the heuristic provider is used.
- If the optional backend is unavailable or cannot be called through a recognized runtime entry point, the adapter does not crash the RAG scanner path.
- Fallback behavior is controlled by `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER`:
  - `heuristic`: run the local heuristic scanner and mark `fallback_used=true`.
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
- `fallback_used`

Raw retrieved chunk text, prompts, full documents, scanner debug payloads, and document content are intentionally excluded.

## Claim boundary

The local heuristic scanner is proven by the targeted tests and demo in this evidence package. The LlamaFirewall/PurpleLlama adapter path is optional. Real LlamaFirewall backend behavior is not proven unless a compatible dependency is installed and the targeted tests/demos are run in that environment. This is not a production-readiness claim.
