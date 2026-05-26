# Patch-Point Mapping (Step 4A Rebuild)

Status: rebuilt cleanly on `architecture-discovery` from baseline `a64b428e009b2c7a9ce9f4dd74d8410222d4e239`.

**Scope constraint:** discovery and documentation only; no control implementation, no refactor, no bugfix, no behavior change.

## Field Definitions
Each patch point includes:
- Patch Point ID
- Area
- Candidate file/path
- Function/class/route (if known)
- Security purpose
- Future control type
- Required context fields
- Audit event needed
- Tests needed
- Demo attack relevance
- Confidence
- Unknowns/blockers

## Mapped Patch Points

| ID | Area | Candidate file/path | Function/class/route | Security purpose | Future control type | Required context fields | Audit event needed | Tests needed | Demo attack relevance | Confidence | Unknowns/blockers |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP-001 | backend startup | backend/onyx/server | app/bootstrap modules | establish global request guard hooks | startup policy initialization | env, deployment mode, tenant mode | server_startup_policy_loaded | startup integration check | unsafe defaults on startup | Medium | exact bootstrap file variants by edition |
| PP-002 | request middleware | backend/onyx/server/middleware | middleware chain | normalize identity/tenant context | centralized middleware policy gate | request id, user id, tenant id, path | request_context_resolved | middleware unit+integration | bypass via unguarded path | High | middleware order across EE/CE |
| PP-003 | auth verification | backend/onyx/auth | auth dependency functions | token/auth source verification | authentication verifier | auth type, token id, issuer, user id | auth_verified/auth_failed | auth integration tests | forged/mis-scoped token | High | provider-specific branches |
| PP-004 | session verification | backend/onyx/server | session dependencies | session integrity/liveness checks | session validation policy | session id, user id, expiry | session_validated/session_rejected | session flow tests | stale or hijacked session use | Medium | mixed stateless/stateful session modes |
| PP-005 | user identity resolution | backend/onyx/auth + server deps | current_user style deps | canonical principal resolution | identity binding/check | user id, email, groups, source | identity_resolved | dependency tests | identity confusion | High | service-account vs human mapping |
| PP-006 | role/admin authorization | backend/onyx/server/manage | admin routes/deps | enforce admin boundaries | RBAC enforcement | user id, role set, route | authz_granted/denied | admin API integration | privilege escalation | High | route coverage completeness |
| PP-007 | tenant/workspace/org resolution | backend/onyx/server + ee | tenant/workspace resolvers | isolate tenant data/actions | tenancy scoping guard | tenant id, workspace id, org id | tenant_scope_bound | multitenant integration | cross-tenant data access | Medium | enterprise-only branches |
| PP-008 | admin APIs | backend/onyx/server/manage | /admin, /manage routes | protect sensitive config operations | endpoint-level policy checks | actor id, role, target resource | admin_action_attempted | admin endpoint tests | unauthorized config mutation | High | all admin routes inventory |
| PP-009 | file uploads | backend/onyx/server + web/api | upload handlers | ensure upload trust boundaries | upload validation policy | actor, filename, mime, size, tenant | file_upload_received | upload integration tests | malicious file ingress | Medium | exact handler fan-out |
| PP-010 | connector ingestion | backend/onyx/connectors + celery tasks | connector sync tasks | constrain connector-originated data | source trust policy | connector id, source type, credential ref | connector_ingest_started | connector integration | poisoned source ingestion | Medium | per-connector adapter variance |
| PP-011 | document parsing | backend/onyx/document_index | parser pipeline functions | sanitize/track parsed content source | parsing guardrails | doc id, source id, parser type | document_parsed | parser pipeline tests | payload-based parser abuse | Medium | parser implementation spread |
| PP-012 | chunking | backend/onyx/document_index | chunking functions | preserve provenance per chunk | provenance propagation | doc id, chunk id, tenant, acl hash | chunk_created | chunk metadata tests | context boundary manipulation | Medium | chunker variants |
| PP-013 | embedding | backend/onyx/llm + indexing | embedding calls | control model request metadata | model call policy | model, provider, tenant, doc scope | embedding_requested | external-dep tests | data exfil via embeddings | Medium | provider adapter indirection |
| PP-014 | vector writes | backend/onyx/document_index/vespa* | index upsert paths | enforce scoped vector indexing | index write policy | index name, tenant, doc/chunk ids | vector_write | indexing integration | unauthorized corpus write | Medium | CE/EE index split |
| PP-015 | vector queries | backend/onyx/document_index/vespa* | search query paths | enforce scoped retrieval query | query policy filter | user, tenant, filters, index | vector_query | retrieval integration | cross-scope retrieval | Medium | dynamic filter composition |
| PP-016 | retrieval/search | backend/onyx/chat + search | retrieval orchestration | ensure ACL-aware retrieval | retrieval policy checks | query id, user, tenant, acl context | retrieval_executed | chat retrieval tests | prompt context poisoning | High | federated connector interactions |
| PP-017 | reranking | backend/onyx/llm + chat | rerank calls | enforce consistent context lineage | rerank policy hooks | model, result ids, acl tokens | rerank_executed | rerank path tests | ranking sensitive docs higher | Medium | rerank provider plurality |
| PP-018 | citation/source attribution | backend/onyx/chat | citation assembly | citation integrity and source trace | provenance integrity checks | answer id, source ids, offsets | citation_generated | citation integration | source spoofing | Medium | mixed answer modes |
| PP-019 | context assembly | backend/onyx/chat | context build functions | prevent forbidden context inclusion | context assembly policy | user, tenant, source ids, permissions | context_assembled | end-to-end chat tests | hidden data leakage in context | High | branch complexity by features |
| PP-020 | prompt construction | backend/onyx/chat | prompt templates/builders | constrain prompt injection surface | prompt hardening hooks | prompt template id, user role, tool flags | prompt_built | prompt unit tests | prompt injection escalation | Medium | many template entrypoints |
| PP-021 | model-provider calls | backend/onyx/llm | provider invoke wrappers | ensure provider-safe outbound calls | outbound model policy | provider, model, tenant, flow tag | llm_call_sent | provider contract tests | unintended provider routing | High | direct vs wrapped call sites |
| PP-022 | streaming responses | backend/onyx/server/query_and_chat | stream endpoints | preserve authz during stream lifecycle | stream authorization continuity | request id, user id, session id | stream_started/ended | stream integration tests | stream hijack/leakage | Medium | reconnect/resume semantics |
| PP-023 | tool registry | backend/onyx/tools | registry construction | limit exposed tool surface | tool allowlist policy | tool id, actor role, tenant mode | tool_registry_resolved | tool list tests | unauthorized tool visibility | Medium | dynamic tool loading |
| PP-024 | tool invocation | backend/onyx/tools | invoke dispatch paths | enforce pre-exec checks | invocation gate | tool id, actor, args hash | tool_invocation_attempt | tool execution tests | dangerous action execution | High | nested/agent-driven dispatch |
| PP-025 | tool argument validation | backend/onyx/tools | arg schema validators | prevent unsafe arg payloads | schema + semantic validation | tool id, args schema version | tool_args_validated/rejected | validator tests | command/data injection | High | inconsistent schema use |
| PP-026 | MCP server entrypoints | backend/onyx/tools/mcp* | mcp init/handlers | protect MCP boundary crossing | MCP session policy | mcp server id, actor id, tenant | mcp_session_started | MCP integration tests | unauthorized MCP bridging | Low | exact MCP modules uncertain |
| PP-027 | MCP tools/resources/prompts | backend/onyx/tools/mcp* | MCP exposed interfaces | govern accessible MCP capabilities | MCP capability policy | capability id, resource URI | mcp_capability_invoked | MCP functional tests | overbroad capability access | Low | inventory pending |
| PP-028 | MCP credential handling | backend/onyx/tools/mcp* + db | credential storage/access funcs | secure secret usage paths | credential access control | credential ref, actor, tenant | mcp_credential_accessed | secret-handling tests | credential misuse | Low | credential indirection unknown |
| PP-029 | artifact generation | backend/onyx/chat + tools | artifact creation funcs | bind artifacts to request identity | artifact policy | artifact id, request id, actor | artifact_generated | artifact integration | untrusted artifact creation | Medium | file backend differences |
| PP-030 | artifact export/download | backend/onyx/server | download routes | enforce download authorization | download gate | artifact id, actor, tenant, expiry | artifact_downloaded/denied | download endpoint tests | data exfil via download | Medium | signed-url pathways |
| PP-031 | sandbox/code execution | backend/onyx/server/features/build/sandbox | sandbox executor paths | isolate code execution requests | execution policy guard | actor, sandbox id, limits | sandbox_exec_started/completed | sandbox integration tests | sandbox breakout attempts | Medium | multiple sandbox backends |
| PP-032 | cache reads/writes | backend/onyx/*cache* + redis usage | cache helper APIs | prevent cross-tenant cache bleed | cache key policy | cache key, tenant, namespace | cache_read/write | cache isolation tests | data bleed via cache keys | Medium | scattered cache call sites |
| PP-033 | workers/queues | backend/onyx/background/celery | task enqueue/dequeue funcs | enforce trusted task submission | task dispatch policy | task name, tenant, expires, actor | task_enqueued/task_run | celery integration | malicious task replay/flood | High | all task producers inventory |
| PP-034 | audit/logging/telemetry | backend/onyx/tracing + logging | telemetry wrappers | complete security event trails | audit schema enforcement | trace id, user, tenant, action | security_audit_event | audit consistency tests | missing forensic trail | High | sink coverage and retention |
| PP-035 | findings/metrics | backend/onyx/server/manage + telemetry | findings endpoints/jobs | trusted metrics generation | findings integrity policy | metric source, window, actor | findings_generated | metrics endpoint tests | metrics tampering | Low | feature ownership unclear |
| PP-036 | admin UI | web/src/app/admin* | admin pages/actions/routes | UI-side privileged path hygiene | frontend authz gating | user role, session, route | admin_ui_access | e2e admin tests | UI privilege bypass | Medium | server/client split points |
| PP-037 | deployment/configuration | deployment/ + env loaders | config load paths | fail-safe security-sensitive config | config validation policy | env source, config keys, mode | config_loaded/invalid | deployment validation tests | insecure misconfiguration | Medium | multi-env template spread |

## Evidence Artifacts

- `docs/security/evidence/patch_points/patch_point_matrix.csv`
- `docs/security/evidence/patch_points/high_confidence_patch_points.txt`
- `docs/security/evidence/patch_points/low_confidence_unknowns.txt`

No application code, runtime logic, or behavior was modified.
