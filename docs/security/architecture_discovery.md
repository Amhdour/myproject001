# Architecture Discovery (Step 3)

Date: 2026-05-26
Branch: architecture-discovery
Starting HEAD: a64b428e009b2c7a9ce9f4dd74d8410222d4e239

## Scope and Constraints
- Discovery-only update from current baseline HEAD.
- No runtime code modified.
- No backend/web/deployment behavior changes.

## 1) Repository and Runtime Entry Discovery
- Top-level structure captured in evidence file `repo_topology.txt`.
- Backend framework identified as FastAPI with API composition in `backend/onyx/main.py`.
- Frontend framework identified as Next.js (app router style) from `web/package.json` and `web/src/app` routes.
- Background workers identified via Celery task and worker surfaces in backend modules.
- Deployment entry surfaces identified under `deployment/` (docker compose, helm, terraform, ECS/Fargate).

## 2) Backend Entrypoints
Primary backend/API entrypoints discovered:
- `backend/onyx/main.py` (FastAPI app construction and router inclusion)
- `backend/onyx/mcp_server/api.py` (dedicated MCP FastAPI app)
- `backend/onyx/mcp_server_main.py` (MCP uvicorn runner)
- Security/admin route aggregation under `backend/onyx/server/security/`

## 3) Frontend Entrypoints
Primary frontend entrypoints discovered:
- `web/package.json` scripts (`next dev`, `next build`, `next start`)
- `web/src/app/**` app-router routes (including API proxy routes)
- `web/src/proxy.ts` route gating/proxy middleware behavior

## 4) Worker/Background Entrypoints
Discovered worker/background surfaces:
- Celery tasks and worker-specific modules across backend packages.
- Build/sandbox daemon FastAPI sidecar entrypoint at sandbox daemon server module.
- Monitoring/queue/task surfaces represented in Celery/task-related files and scheduling surfaces.

## 5) Deployment Entrypoints
Discovered deployment/control-plane surfaces:
- `deployment/docker_compose/**`
- `deployment/helm/**`
- `deployment/terraform/**`
- `deployment/aws_ecs_fargate/**`

## 6) Security-Relevant Flow Mapping (High-Level)

### Authentication Flow
- Auth API routes and providers observed across backend auth/server modules, including OAuth/SAML/SCIM and password/PAT endpoints.
- Frontend route protection observed in Next.js proxy layer and auth pages.

### Session Flow
- Session surfaces discovered in chat/query/build routes and frontend state providers.
- Build/session API modules present under build feature API namespace.

### User/Role/Admin Flow
- User/admin management routes observed in manage/admin router modules.
- Role and permission-related endpoints spread across management/security and connector/document access surfaces.

### Tenant/Workspace/Organization Flow
- Tenant APIs present under enterprise tenant modules (`backend/ee/onyx/server/tenants/**`).
- Multi-tenant controls also represented in scheduler/tasks and tenant-specific server routes.

## 7) Data Model Mapping Targets
Database model index generated for the following areas to support deeper review:
- users
- roles
- tenants/workspaces
- documents
- chunks
- permissions
- connectors
- chats
- agents
- tools
- MCP
- audit/logging

## 8) Retrieval/LLM/Agent Pipeline Mapping Targets
Pipeline surface map generated for:
- document ingestion
- file upload
- connector ingestion
- parsing/chunking/embedding
- vector index (vespa) write/read flow
- retrieval/search and reranking
- citation/source attribution
- context assembly
- prompt construction
- model-provider call path
- streaming response flow
- tool/agent execution flow
- MCP integration flow
- artifact/export generation flow
- sandbox/code execution flow

## 9) Admin/API/UI Surfaces
- Admin API surfaces found across `/admin/*` backend routers.
- Admin/security APIs mapped under security namespace and feature-specific admin routers.
- Admin UI surfaces inferred from frontend app routes and settings/management pages.

## 10) Logging/Audit/Telemetry/Cache/Queue Surfaces
- Logging and uvicorn logger setup located in backend logging utilities and main bootstrap.
- Audit/security reporting routes found under security server package.
- Cache/queue hints detected from Redis/Celery references across backend modules.

## 11) Trust Boundaries (Initial)
Identified trust boundaries to be validated in deep review:
- Browser client ↔ Next.js web server/API routes
- Web server ↔ backend FastAPI APIs
- Backend APIs ↔ Celery workers
- Backend/workers ↔ Postgres/Redis/Vespa/object stores
- Backend ↔ external connector/provider APIs (LLM, OAuth, SaaS connectors)
- Build/sandbox orchestration ↔ sandbox runtime sidecars
- MCP clients ↔ MCP server/API surfaces

## 12) Sensitive Data Flows (Initial)
Potential sensitive data flows requiring deep verification:
- Authentication credentials/tokens (OAuth/SAML/password/PAT/session tokens)
- Connector credentials and sync metadata
- User-uploaded files and derived chunks/embeddings
- Chat prompts/responses and citations
- Admin and tenant management actions
- Audit/security findings and artifacts

## 13) Security-Relevant Patch Candidates (Do Not Patch Yet)
Potential hardening candidates identified for future steps (not implemented here):
- Route-level authz consistency checks across admin and tenant endpoints
- Session/token lifecycle and revocation coverage review
- MCP/tool execution boundary validation
- Sandbox escape/egress control validation
- Citation/source sanitization and prompt injection defenses
- Audit log completeness and tamper-resistance review

## 14) Unknowns / Deeper Review Required
- Exact canonical API entrypoint set for all deployment modes (community vs enterprise combinations)
- Precise DB table ownership for role/tenant/workspace entities across CE/EE splits
- Exact end-to-end connector ingestion state machine and retry semantics per connector class
- Final authorization decision points for tool execution, MCP flows, and sandbox launches
- Exact provenance path for citations and source-attribution metadata in streaming chat responses

## 15) Evidence Handling
- Supporting evidence saved under `docs/security/evidence/architecture_discovery/`.
- No secrets intentionally copied.
- If future evidence captures sensitive values, redact before storage.
