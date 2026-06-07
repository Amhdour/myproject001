# RAG Prompt-Injection Scanner Evidence

This evidence bundle covers the runtime retrieved-context prompt-injection scanner abstraction.

## Scope

- Scanner package: `backend/onyx/security_layer/scanners/`
- Runtime seam: after OPA retrieval ACL filtering and before final context serialization in `backend/onyx/tools/tool_implementations/utils.py`
- Safe evidence export: `backend/onyx/security_layer/langfuse_evidence.py`, `backend/onyx/security_layer/redaction.py`, and `backend/onyx/security_layer/tracing.py`
- Demo attack: `scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py`

## Behavior

The scanner is gated by:

```bash
SECURITY_RAG_INJECTION_SCANNER_ENABLED=true
```

When enabled, the default local heuristic scanner checks each already-authorized retrieved chunk for obvious prompt-injection phrases, including requests to ignore previous instructions, reveal the system prompt, override security policy, exfiltrate hidden documents, or call unauthorized tools.

Configured scanner action is controlled by:

```bash
SECURITY_RAG_INJECTION_SCANNER_MODE=deny       # default high-risk action
SECURITY_RAG_INJECTION_SCANNER_MODE=sanitize
SECURITY_RAG_INJECTION_SCANNER_MODE=monitor
SECURITY_RAG_INJECTION_SCANNER_MODE=shadow_deny
SECURITY_RAG_INJECTION_SCANNER_MODE=allow
```

- `allow`: keep the chunk.
- `deny`: exclude the chunk from final RAG context.
- `sanitize`: replace detected instruction text with a placeholder and keep the chunk.
- `monitor`: record evidence and keep the chunk.
- `shadow_deny`: record that the chunk would be denied and keep it.

OPA authorization and scanner decisions are separate. OPA decides whether a chunk is authorized for the subject; the scanner only inspects chunks that remain after that authorization step.

## Failure fallback

Scanner failures are controlled by:

```bash
SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE=monitor  # default
SECURITY_RAG_INJECTION_SCANNER_FAILURE_MODE=deny
```

The default is `monitor`, which preserves current context behavior on scanner failure while recording fallback evidence. Higher-risk deployments can set `deny` to exclude chunks when the scanner fails. This is a risk configuration choice, not a production-readiness claim.

## Evidence metadata

The OpenTelemetry span name is:

```text
security.rag_injection.scan
```

Langfuse-safe evidence metadata is allowlisted to:

- `scanner_name`
- `scanner_decision`
- `risk_type`
- `risk_score`
- `sanitized`
- `resource_chunk_id`
- `correlation_id`
- `fallback_used`

Raw retrieved chunk text is not exported. Evidence payloads go through the security-layer redaction helper as defense in depth.

## Adapter boundary

This implementation is a local heuristic scanner first. LlamaFirewall/PurpleLlama and AgentShield classes are extension-point adapters only; they are not implemented or proven in this change. No PyRIT, garak, promptfoo, Ragas, Authensor, OpenGuardrails, or full external project is vendored here.
