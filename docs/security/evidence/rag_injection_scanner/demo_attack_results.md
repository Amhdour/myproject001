# Demo Attack Results

The demo attack uses two same-tenant, OPA-authorized chunks:

1. A clean chunk with release-date context.
2. A malicious retrieved chunk containing obvious prompt-injection instructions.

The script intentionally demonstrates the scanner boundary:

- OPA authorization allows both chunks in the demo because they are same-tenant fixtures.
- The RAG injection scanner then inspects the authorized chunks before final context serialization.
- In `deny` mode, the malicious chunk is removed from final context.
- In `sanitize` mode, the malicious instruction phrases are replaced with a neutral placeholder.

Example command:

```bash
python scripts/security/demo_attacks/rag_injection/retrieved_chunk_prompt_injection_demo.py
```

Example expected JSON fields:

```json
{
  "disabled_contains_attack": true,
  "deny_contains_attack": false,
  "sanitize_contains_attack_phrase": false,
  "sanitize_contains_placeholder": true
}
```

The output does not prove production readiness. It is a local deterministic demo of the initial heuristic scanner and runtime integration point.
