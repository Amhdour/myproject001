from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RuntimeAction(str, Enum):
    INGESTION = "ingestion"
    RETRIEVAL = "retrieval"
    VECTOR_QUERY = "vector_query"
    CACHE_ACCESS = "cache_access"
    TOOL_CALL = "tool_call"
    MCP_ACTION = "mcp_action"
    ARTIFACT_RELEASE = "artifact_release"
    SANDBOX_EXECUTION = "sandbox_execution"
    MODEL_CALL = "model_call"
    PROMPT_USE = "prompt_use"
    HUMAN_APPROVAL = "human_approval"


@dataclass(frozen=True)
class RequestContext:
    request_id: str
    operation: str


@dataclass(frozen=True)
class SubjectContext:
    subject_id: str
    subject_type: str = "user"


@dataclass(frozen=True)
class TenantContext:
    tenant_id: str


@dataclass(frozen=True)
class SessionContext:
    session_id: str | None = None


@dataclass(frozen=True)
class IngestionContext:
    source_type: str | None = None
    connector_id: str | None = None


@dataclass(frozen=True)
class RetrievalContext:
    query_hash: str | None = None
    document_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class VectorContext:
    index_name: str | None = None
    top_k: int | None = None


@dataclass(frozen=True)
class CacheContext:
    cache_namespace: str | None = None
    cache_key_hash: str | None = None


@dataclass(frozen=True)
class ToolContext:
    tool_name: str | None = None
    tool_action: str | None = None


@dataclass(frozen=True)
class MCPContext:
    server_name: str | None = None
    action_name: str | None = None


@dataclass(frozen=True)
class ArtifactContext:
    artifact_type: str | None = None
    redaction_applied: bool = False


@dataclass(frozen=True)
class SandboxContext:
    execution_type: str | None = None
    command_hash: str | None = None


@dataclass(frozen=True)
class ApprovalContext:
    approval_id: str | None = None
    approval_reason: str | None = None


@dataclass(frozen=True)
class ModelContext:
    model_name: str | None = None
    provider_name: str | None = None


@dataclass(frozen=True)
class PromptContext:
    prompt_id: str | None = None
    prompt_hash: str | None = None


@dataclass(frozen=True)
class SecurityDecisionContext:
    request: RequestContext
    subject: SubjectContext | None = None
    tenant: TenantContext | None = None
    session: SessionContext | None = None
    ingestion: IngestionContext | None = None
    retrieval: RetrievalContext | None = None
    vector: VectorContext | None = None
    cache: CacheContext | None = None
    tool: ToolContext | None = None
    mcp: MCPContext | None = None
    artifact: ArtifactContext | None = None
    sandbox: SandboxContext | None = None
    approval: ApprovalContext | None = None
    model: ModelContext | None = None
    prompt: PromptContext | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def has_required_identity(context: SecurityDecisionContext) -> bool:
    return bool(context.subject and context.subject.subject_id)


def has_required_tenant(context: SecurityDecisionContext) -> bool:
    return bool(context.tenant and context.tenant.tenant_id)
