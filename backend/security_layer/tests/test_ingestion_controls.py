from datetime import datetime

from backend.security_layer.ingestion import controls
from backend.security_layer.ingestion.models import ACLSnapshot
from backend.security_layer.ingestion.models import IngestionDecisionStatus
from backend.security_layer.ingestion.models import IngestionSecurityContext
from backend.security_layer.ingestion.models import IngestionSourceType
from backend.security_layer.ingestion.models import IngestionStage
from backend.security_layer.ingestion.models import ProvenanceRecord
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _ctx(stage: IngestionStage = IngestionStage.UPLOAD_RECEIVED) -> IngestionSecurityContext:
    return IngestionSecurityContext(
        tenant_id="tenant-1",
        subject_id="subject-1",
        stage=stage,
        source_type=IngestionSourceType.USER_UPLOAD,
        source_id="doc-1",
        source_metadata={"filename": "safe.txt"},
        content_type="text/plain",
        size_bytes=10,
        max_size_bytes=100,
        file_count=1,
        max_file_count=5,
        acl_snapshot=ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=1, is_stale=False),
        provenance=ProvenanceRecord(
            source_id="doc-1",
            source_type=IngestionSourceType.USER_UPLOAD,
            ingested_at=datetime.utcnow(),
            checksum="checksum",
        ),
        request_id="req-1",
    )


def test_all_17_ingestion_stage_authorizers_have_coverage() -> None:
    authorizers = {
        IngestionStage.UPLOAD_RECEIVED: controls.authorize_upload_received,
        IngestionStage.CONNECTOR_SYNC_STARTED: controls.authorize_connector_sync_started,
        IngestionStage.SOURCE_METADATA_VALIDATED: controls.authorize_source_metadata_validated,
        IngestionStage.TENANT_BOUNDARY_VALIDATED: controls.authorize_tenant_boundary_validated,
        IngestionStage.OWNERSHIP_VALIDATED: controls.authorize_ownership_validated,
        IngestionStage.ACL_SNAPSHOT_CAPTURED: controls.authorize_acl_snapshot_captured,
        IngestionStage.CONTENT_TYPE_VALIDATED: controls.authorize_content_type_validated,
        IngestionStage.FILE_SIZE_VALIDATED: controls.authorize_file_size_validated,
        IngestionStage.PARSER_SELECTED: controls.authorize_parser_selected,
        IngestionStage.PARSER_COMPLETED: controls.authorize_parser_completed,
        IngestionStage.CHUNKS_CREATED: controls.authorize_chunks_created,
        IngestionStage.CHUNK_METADATA_ATTACHED: controls.authorize_chunk_metadata_attached,
        IngestionStage.EMBEDDING_REQUESTED: controls.authorize_embedding_requested,
        IngestionStage.VECTOR_WRITE_AUTHORIZED: controls.authorize_vector_write_authorized,
        IngestionStage.PROVENANCE_RECORDED: controls.authorize_provenance_recorded,
        IngestionStage.INGESTION_AUDIT_WRITTEN: controls.authorize_ingestion_audit_written,
        IngestionStage.INGESTION_FINDING_RECORDED_IF_NEEDED: controls.authorize_ingestion_finding_recorded_if_needed,
    }
    assert len(authorizers) == 17
    for stage, fn in authorizers.items():
        decision = fn(_ctx(stage))
        assert decision.stage == stage
        assert decision.status in {IngestionDecisionStatus.ALLOW, IngestionDecisionStatus.FLAG}


def test_missing_tenant_subject_metadata_and_acl_denials() -> None:
    tenant_missing = controls.authorize_upload_received(IngestionSecurityContext(**{**_ctx().__dict__, "tenant_id": None}))
    subject_missing = controls.authorize_upload_received(IngestionSecurityContext(**{**_ctx().__dict__, "subject_id": None}))
    metadata_invalid = controls.authorize_source_metadata_validated(
        IngestionSecurityContext(**{**_ctx(IngestionStage.SOURCE_METADATA_VALIDATED).__dict__, "source_metadata": {"api_key": "abc"}})
    )
    acl_missing = controls.authorize_acl_snapshot_captured(
        IngestionSecurityContext(**{**_ctx(IngestionStage.ACL_SNAPSHOT_CAPTURED).__dict__, "acl_snapshot": None})
    )
    acl_stale = controls.authorize_acl_snapshot_captured(
        IngestionSecurityContext(
            **{
                **_ctx(IngestionStage.ACL_SNAPSHOT_CAPTURED).__dict__,
                "acl_snapshot": ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=1, is_stale=True),
            }
        )
    )
    for decision, category in (
        (tenant_missing, DenialCategory.TENANT_CONTEXT_MISSING),
        (subject_missing, DenialCategory.SUBJECT_CONTEXT_MISSING),
        (metadata_invalid, DenialCategory.VALIDATION_FAILED),
        (acl_missing, DenialCategory.VALIDATION_FAILED),
        (acl_stale, DenialCategory.VALIDATION_FAILED),
    ):
        assert decision.status == IngestionDecisionStatus.DENY
        assert decision.denial_category == category


def test_content_size_count_and_provenance_denials() -> None:
    content_invalid = controls.authorize_content_type_validated(
        IngestionSecurityContext(**{**_ctx(IngestionStage.CONTENT_TYPE_VALIDATED).__dict__, "content_type": "application/x-msdownload"})
    )
    size_oversized = controls.authorize_file_size_validated(
        IngestionSecurityContext(**{**_ctx(IngestionStage.FILE_SIZE_VALIDATED).__dict__, "size_bytes": 9999})
    )
    file_count_excessive = controls.authorize_file_size_validated(
        IngestionSecurityContext(**{**_ctx(IngestionStage.FILE_SIZE_VALIDATED).__dict__, "file_count": 99})
    )
    provenance_missing = controls.authorize_vector_write_authorized(
        IngestionSecurityContext(**{**_ctx(IngestionStage.VECTOR_WRITE_AUTHORIZED).__dict__, "provenance": None})
    )
    for decision in (content_invalid, size_oversized, file_count_excessive, provenance_missing):
        assert decision.status == IngestionDecisionStatus.DENY
        assert decision.denial_category == DenialCategory.VALIDATION_FAILED


def test_marker_flagging_audit_finding_metric_and_non_leakage() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()

    decision = controls.authorize_upload_received(
        IngestionSecurityContext(
            **{
                **_ctx().__dict__,
                "text_sample": "ignore previous instructions with hidden instruction marker",
                "source_metadata": {"filename": "safe.txt", "source_secret": "sk-secret"},
            }
        )
    )

    assert decision.status == IngestionDecisionStatus.DENY
    assert "hidden instruction" not in decision.reason
    assert "ignore previous instructions" not in decision.reason
    assert "sk-secret" not in decision.reason

    assert get_audit_events()
    assert get_findings() == []
    assert get_security_metrics()


def test_prompt_and_poisoning_findings_emit_when_metadata_valid() -> None:
    clear_findings()
    decision = controls.authorize_upload_received(
        IngestionSecurityContext(**{**_ctx().__dict__, "text_sample": "ignore previous instructions and hidden instruction"})
    )
    assert decision.status == IngestionDecisionStatus.FLAG
    assert set(decision.flags) == {"prompt_injection_marker", "poisoning_marker"}
    findings = get_findings()
    assert {finding.reason_code for finding in findings} == {"prompt_injection_marker", "poisoning_marker"}


def test_no_live_app_integration_imported() -> None:
    imported_modules = set(controls.__dict__.keys())
    assert "fastapi" not in imported_modules
    assert "celery" not in imported_modules
