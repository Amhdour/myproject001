# Cross-Control Test Strategy

## Strategy
- Keep security-layer testing isolated and monitor-only.
- Verify cross-control interaction contracts before any live integration.
- Require explicit no-behavior-change checks.

## Planned Cross-Control Test Groups
1. context propagation integrity
2. denial contract consistency
3. retrieval/vector/cache compatibility
4. tool + argument validator compatibility
5. MCP + credential scope compatibility
6. ingestion + provenance propagation
7. audit/finding emission continuity
8. rollout-mode invariant checks

Cross-control tests planned count: **8**.
