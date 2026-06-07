# Final Known Limitations

This document lists the limitations that remain in scope for the final portfolio package.

## Required limitations

- Full backend tests are not globally proven unless they were actually run in the current environment.
- Real PyRIT executions are not proven unless dependency-backed runs were performed.
- Real garak executions are not proven unless dependency-backed runs were performed.
- Real Ragas executions are not proven unless dependency-backed runs were performed.
- Real promptfoo executions are not proven unless dependency-backed runs were performed.
- Real LlamaFirewall backend behavior is not proven unless dependency-backed runs were performed.
- Real AgentShield backend behavior is not proven unless dependency-backed runs were performed.
- Production deployment is not proven.
- Enterprise audit is not proven.
- Some integrations are env-gated.
- Some external adapters are optional or fallback-tested.
- Live production traffic was not validated.

## Additional context

- The package is intentionally portfolio-oriented, not production-attestation oriented.
- Several controls are proven through local unit tests, fixture-backed demo attacks, or deterministic evidence scripts rather than a deployed production environment.
- Optional adapters are designed to fail safely when their dependency is absent.
- Evidence exporters intentionally redact or allowlist metadata so raw prompts, raw chunks, secret tokens, and similar content do not appear in the public-safe package.

## Boundary reminder

These limitations are not defects in the evidence package; they are the explicit boundary between what is proven locally and what would require separate live, independent, or enterprise-scale validation.
