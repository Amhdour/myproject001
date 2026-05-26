# Security Architecture Discovery (Step 3 Rebuild)

Status: rebuilt on `architecture-discovery` from baseline commit `a64b428e009b2c7a9ce9f4dd74d8410222d4e239`.

Constraints followed:
- Documentation/evidence-only change.
- No runtime code changes.
- No security-control implementation.
- No behavior modifications.

## Evidence Index

- Repo topology: `docs/security/evidence/architecture_discovery/repo_topology.txt`
- Runtime entrypoints: `docs/security/evidence/architecture_discovery/runtime_entrypoints.txt`
- Frontend entrypoints: `docs/security/evidence/architecture_discovery/frontend_entrypoints.txt`
- Deployment index: `docs/security/evidence/architecture_discovery/deployment_index.txt`
- Authorization/authentication surface map signals: `docs/security/evidence/architecture_discovery/authz_surface_map.txt`
- DB model index: `docs/security/evidence/architecture_discovery/db_model_index.txt`
- Pipeline surface map signals: `docs/security/evidence/architecture_discovery/pipeline_surface_map.txt`

## Repo Topology

Primary code roots identified:
- `backend/onyx/` and `backend/ee/onyx/` for API, auth, DB, indexing, and background work.
- `web/src/` for frontend routes/components/actions.
- `deployment/` for runtime configuration and deployment manifests/scripts.

## Runtime Entrypoints

Discovery confirms security-relevant entrypoint classes:
- API initialization and router registration surfaces in backend server modules.
- Request lifecycle middleware surfaces for identity/session/tenant resolution.
- Celery workers + task modules for asynchronous ingestion/indexing flows.
- Tool/agent-related execution surfaces in chat/tool modules.

## Frontend Entrypoints

Frontend entrypoints mapped at route/page/layout/middleware level:
- App Router pages and route handlers under `web/src/app`.
- Middleware and shared auth/session utilities in frontend utility layers.
- Admin and settings surfaces routed through app pages/actions.

## Deployment Index

Deployment surfaces include:
- Environment/config inputs impacting auth/session/model providers.
- Service manifests for API, workers, web, and supporting services.
- Runtime startup scripts and templates that determine process composition.

## Authz Surface Map

Mapped authn/authz candidates include:
- Identity acquisition (`current_user`, session/token parsing).
- Admin/role checks.
- Workspace/tenant/organization scoping.
- API routers that expose privileged configuration and data operations.

## DB Model Index

DB model and operation surfaces identified under:
- `backend/onyx/db/`
- `backend/ee/onyx/db/`

These are candidate points for future policy-aware read/write controls and audit instrumentation.

## Pipeline Surface Map

End-to-end pipeline surfaces mapped for future patch-pointing:
- Upload/connectors/ingestion/parsing/chunking/embedding/vector write/query.
- Retrieval/rerank/citation/context/prompt/model invocation/streaming.
- Tools and MCP execution surfaces.
- Artifact generation/export, cache, queue/worker, and telemetry surfaces.

## Notes

This rebuild is a structural discovery snapshot only. It intentionally avoids introducing controls or changing behavior.
