from __future__ import annotations

from typing import Any

from onyx.configs.constants import DocumentSource
from onyx.context.search.models import InferenceChunk
from onyx.context.search.models import InferenceSection
from onyx.security_layer.opa.decision_mapper import OPADecision
from onyx.security_layer.opa.decision_mapper import OPADecisionValue
from onyx.security_layer.opa.retrieval_context_filter import (
    filter_sections_for_opa_retrieval_acl_context,
)
from onyx.tools.tool_implementations.utils import (
    convert_inference_sections_to_llm_string,
)


class RecordingOPAClient:
    def __init__(self, unavailable: bool = False) -> None:
        self.unavailable = unavailable
        self.inputs: list[dict[str, Any]] = []

    def evaluate_retrieval_acl(self, opa_input: dict[str, object]) -> OPADecision:
        typed_input = dict(opa_input)
        self.inputs.append(typed_input)
        subject = typed_input["subject"]
        resource = typed_input["resource"]
        assert isinstance(subject, dict)
        assert isinstance(resource, dict)

        if self.unavailable:
            return OPADecision(
                decision=OPADecisionValue.DENY,
                reason="OPA unavailable; denied high-risk retrieval decision: test outage",
                correlation_id=str(typed_input["correlation_id"]),
                fallback_used=True,
                subject_user_id=str(subject.get("user_id")),
                subject_tenant_id=str(subject.get("tenant_id")),
                resource_document_id=str(resource.get("document_id")),
                resource_tenant_id=str(resource.get("tenant_id")),
            )
        if resource.get("deleted") is True:
            return _decision(typed_input, "deny", "deleted document")
        if subject.get("tenant_id") != resource.get("tenant_id"):
            return _decision(typed_input, "deny", "cross-tenant resource")
        if subject.get("user_id") in resource.get("allowed_users", []):
            return _decision(typed_input, "allow", "same tenant allowed user")
        return _decision(typed_input, "deny", "subject is not permitted for resource")


def _decision(opa_input: dict[str, Any], decision: str, reason: str) -> OPADecision:
    subject = opa_input["subject"]
    resource = opa_input["resource"]
    assert isinstance(subject, dict)
    assert isinstance(resource, dict)
    return OPADecision(
        decision=OPADecisionValue(decision),
        reason=reason,
        correlation_id=str(opa_input["correlation_id"]),
        subject_user_id=str(subject.get("user_id")),
        subject_tenant_id=str(subject.get("tenant_id")),
        resource_document_id=str(resource.get("document_id")),
        resource_tenant_id=str(resource.get("tenant_id")),
    )


def _chunk(
    *,
    document_id: str,
    chunk_id: int,
    content: str,
    tenant_id: str = "tenant-a",
    deleted: bool = False,
    allowed_user: str = "user-a",
) -> InferenceChunk:
    chunk = InferenceChunk(
        document_id=document_id,
        chunk_id=chunk_id,
        blurb=content,
        content=content,
        source_type=DocumentSource.FILE,
        semantic_identifier=document_id,
        title=document_id,
        boost=0,
        score=1.0,
        hidden=False,
        metadata={},
        match_highlights=[],
        doc_summary="",
        chunk_context="",
        updated_at=None,
    )
    chunk.metadata["onyx_acl"] = {
        "tenant_id": tenant_id,
        "user_ids": [allowed_user],
        "group_ids": [],
        "connector_id": "connector-test",
        "deleted": deleted,
        "permission_version": "pv-test",
    }
    return chunk


def _section(chunks: list[InferenceChunk]) -> InferenceSection:
    return InferenceSection(
        center_chunk=chunks[0],
        chunks=chunks,
        combined_content="\n".join(chunk.content for chunk in chunks),
    )


def test_allowed_same_tenant_chunk_enters_final_context(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT", "true")
    opa_client = RecordingOPAClient()

    docs_str, citation_mapping = convert_inference_sections_to_llm_string(
        [
            _section(
                [_chunk(document_id="doc-a", chunk_id=0, content="tenant a allowed")]
            )
        ],
        opa_subject_user_id="user-a",
        opa_subject_tenant_id="tenant-a",
        opa_client=opa_client,
    )

    assert "tenant a allowed" in docs_str
    assert citation_mapping == {1: "doc-a"}
    assert opa_client.inputs[0]["action"] == "rag.context.include"


def test_cross_tenant_chunk_excluded_from_final_context(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT", "true")
    opa_client = RecordingOPAClient()

    docs_str, citation_mapping = convert_inference_sections_to_llm_string(
        [
            _section(
                [
                    _chunk(document_id="doc-a", chunk_id=0, content="tenant a allowed"),
                    _chunk(
                        document_id="doc-b",
                        chunk_id=0,
                        content="tenant b secret",
                        tenant_id="tenant-b",
                        allowed_user="user-b",
                    ),
                ]
            )
        ],
        opa_subject_user_id="user-a",
        opa_subject_tenant_id="tenant-a",
        opa_client=opa_client,
    )

    assert "tenant a allowed" in docs_str
    assert "tenant b secret" not in docs_str
    assert citation_mapping == {1: "doc-a"}


def test_deleted_document_chunk_excluded_from_final_context(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT", "true")
    opa_client = RecordingOPAClient()

    docs_str, citation_mapping = convert_inference_sections_to_llm_string(
        [
            _section(
                [
                    _chunk(
                        document_id="doc-deleted",
                        chunk_id=0,
                        content="deleted document content",
                        deleted=True,
                    )
                ]
            )
        ],
        opa_subject_user_id="user-a",
        opa_subject_tenant_id="tenant-a",
        opa_client=opa_client,
    )

    assert "deleted document content" not in docs_str
    assert citation_mapping == {}


def test_opa_unavailable_fallback_denies_and_records_evidence() -> None:
    result = filter_sections_for_opa_retrieval_acl_context(
        sections=[
            _section([_chunk(document_id="doc-a", chunk_id=0, content="blocked")])
        ],
        subject_user_id="user-a",
        subject_tenant_id="tenant-a",
        subject_groups=None,
        correlation_id="test-opa-unavailable",
        opa_client=RecordingOPAClient(unavailable=True),
    )

    assert result.sections == []
    assert len(result.decisions) == 1
    assert result.decisions[0].decision == OPADecisionValue.DENY
    assert result.decisions[0].fallback_used is True
    assert result.decisions[0].audit_details["fallback_used"] is True


def test_opa_retrieval_acl_tracing_records_metadata_without_chunk_text(
    monkeypatch,
) -> None:
    spans: list[tuple[str, dict[str, object]]] = []

    class FakeSecuritySpan:
        def __init__(self, name: str) -> None:
            self.name = name
            self.attributes: dict[str, object] = {}

        def set_attribute(self, key: str, value: object) -> None:
            self.attributes[key] = value

    class FakeSecuritySpanContext:
        def __init__(self, name: str, attributes: dict[str, object | None]) -> None:
            self.span = FakeSecuritySpan(name)
            for key, value in attributes.items():
                if value is not None:
                    self.span.set_attribute(key, value)

        def __enter__(self) -> FakeSecuritySpan:
            return self.span

        def __exit__(self, *args: object) -> None:
            spans.append((self.span.name, dict(self.span.attributes)))

    def fake_security_span(
        name: str, attributes: dict[str, object | None] | None = None
    ) -> FakeSecuritySpanContext:
        return FakeSecuritySpanContext(name, attributes or {})

    def fake_set_security_span_attributes(
        span: FakeSecuritySpan | None, attributes: dict[str, object | None]
    ) -> None:
        if span is None:
            return
        for key, value in attributes.items():
            if value is not None:
                span.set_attribute(key, value)

    import onyx.security_layer.opa.retrieval_context_filter as retrieval_context_filter

    monkeypatch.setattr(retrieval_context_filter, "security_span", fake_security_span)
    monkeypatch.setattr(
        retrieval_context_filter,
        "set_security_span_attributes",
        fake_set_security_span_attributes,
    )
    monkeypatch.setenv("SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT", "true")

    result = filter_sections_for_opa_retrieval_acl_context(
        sections=[
            _section(
                [
                    _chunk(
                        document_id="doc-traced",
                        chunk_id=7,
                        content="raw secret chunk text must not be traced",
                    )
                ]
            )
        ],
        subject_user_id="user-a",
        subject_tenant_id="tenant-a",
        subject_groups=None,
        correlation_id="trace-test",
        opa_client=RecordingOPAClient(),
    )

    assert len(result.decisions) == 1
    decision_span = next(
        attributes
        for name, attributes in spans
        if name == "security.opa.retrieval_acl.decision"
    )
    assert decision_span["correlation_id"] == "trace-test:doc-traced:7"
    assert decision_span["subject_user_id"] == "user-a"
    assert decision_span["subject_tenant_id"] == "tenant-a"
    assert decision_span["resource_document_id"] == "doc-traced"
    assert decision_span["resource_chunk_id"] == "7"
    assert decision_span["resource_tenant_id"] == "tenant-a"
    assert decision_span["policy_package"] == "onyx.security.retrieval_acl"
    assert decision_span["decision"] == "allow"
    assert decision_span["reason"] == "same tenant allowed user"
    assert decision_span["fallback_used"] is False
    assert decision_span["enforcement_enabled"] is True
    serialized_attributes = str(spans)
    assert "raw secret chunk text must not be traced" not in serialized_attributes
