from datetime import datetime

from backend.security_layer.ingestion.models import ACLSnapshot
from backend.security_layer.ingestion.models import IngestionSecurityContext
from backend.security_layer.ingestion.models import IngestionSourceType
from backend.security_layer.ingestion.models import IngestionStage
from backend.security_layer.ingestion.models import ProvenanceRecord


def test_ingestion_context_creation() -> None:
    context = IngestionSecurityContext(
        tenant_id="t1",
        subject_id="u1",
        stage=IngestionStage.UPLOAD_RECEIVED,
        source_type=IngestionSourceType.USER_UPLOAD,
        source_id="doc-1",
        source_metadata={"filename": "a.txt"},
        acl_snapshot=ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=1),
        provenance=ProvenanceRecord(source_id="doc-1", source_type=IngestionSourceType.USER_UPLOAD, ingested_at=datetime.utcnow(), checksum="abc"),
    )
    assert context.tenant_id == "t1"
    assert context.source_metadata["filename"] == "a.txt"
