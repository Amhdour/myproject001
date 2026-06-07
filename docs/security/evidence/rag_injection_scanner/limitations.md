# RAG Prompt-Injection Scanner Limitations

- This is a local heuristic scanner first, not a comprehensive prompt-injection defense.
- LlamaFirewall/PurpleLlama and AgentShield are represented by planned adapter classes only. They are not implemented, evaluated, or proven by this change.
- This change does not vendor full external projects and does not add PyRIT, garak, promptfoo, Ragas, Authensor, or OpenGuardrails.
- The heuristic detector can produce false positives for benign text that discusses prompt injection.
- The heuristic detector can produce false negatives for obfuscated, multilingual, indirect, or novel attacks.
- `sanitize` mode only removes matched obvious instruction phrases. It does not guarantee that the remaining text is safe.
- `monitor` and `shadow_deny` preserve chunks in final context by design; use them for observation or rollout only.
- Scanner failure defaults to `monitor` unless `SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE=deny` is configured. Teams must choose the fallback behavior based on risk tolerance.
- OPA authorization semantics are unchanged. Authorization denials still come from OPA retrieval ACL filtering, not the scanner.
- Evidence metadata is intentionally raw-content-free. Do not add raw retrieved chunk text, prompts, or document text to Langfuse or OpenTelemetry evidence fields.
- This evidence package makes no production-readiness, compliance, or external validation claim.
