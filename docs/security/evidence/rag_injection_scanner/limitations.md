# RAG Prompt-Injection Scanner Limitations

- This is a local heuristic scanner first, not a comprehensive prompt-injection defense.
- The local heuristic scanner is proven by the targeted tests and demo in this evidence package.
- The LlamaFirewall/PurpleLlama adapter path is optional and runtime-loaded only; the full PurpleLlama repository is not vendored.
- Real LlamaFirewall backend behavior is not proven unless a compatible dependency is installed and the tests/demos are rerun in that environment.
- The AgentShield adapter path is optional and runtime-loaded only; the full AgentShield repository is not vendored.
- Real AgentShield backend behavior is not proven unless a compatible dependency is installed and the tests/demos are rerun in that environment.
- This change does not vendor full external projects and does not add PyRIT, garak, promptfoo, Ragas, Authensor, or OpenGuardrails.
- The heuristic detector can produce false positives for benign text that discusses prompt injection.
- The heuristic detector can produce false negatives for obfuscated, multilingual, indirect, or novel attacks.
- `sanitize` mode only removes matched obvious instruction phrases. It does not guarantee that the remaining text is safe.
- `monitor` and `shadow_deny` preserve chunks in final context by design; use them for observation or rollout only.
- Generic scanner failure defaults to `monitor` unless `SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE=deny` is configured. Teams must choose the fallback behavior based on risk tolerance.
- Optional LlamaFirewall/PurpleLlama backend unavailability follows `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=heuristic|monitor|deny`, defaulting to the proven local heuristic scanner.
- Optional AgentShield backend unavailability follows `SECURITY_RAG_SCANNER_FALLBACK_PROVIDER=heuristic|monitor|deny`, defaulting to the proven local heuristic scanner.
- OPA authorization semantics are unchanged. Authorization denials still come from OPA retrieval ACL filtering, not the scanner.
- Evidence metadata is intentionally raw-content-free. Do not add raw retrieved chunk text, prompts, or document text to Langfuse or OpenTelemetry evidence fields.
- This evidence package makes no production-readiness, compliance, or external validation claim.
