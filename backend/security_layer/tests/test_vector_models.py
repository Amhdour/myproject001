from datetime import UTC, datetime, timedelta

from backend.security_layer.vector.models import VectorNamespace, VectorOperationType, VectorSecurityContext, VectorSecurityStage


def test_vector_security_context_creation() -> None:
    ctx = VectorSecurityContext(
        request_id="r1",
        operation_type=VectorOperationType.WRITE,
        stage=VectorSecurityStage.WRITE_REQUESTED,
        tenant_id_hash_or_safe_id="tenant_a",
        workspace_id_hash_or_safe_id="ws_a",
        subject_id_hash_or_safe_id="subj_a",
        namespace=VectorNamespace(name="tenant_a/ws_a"),
        authorized_namespaces=("tenant_a/ws_a",),
    )
    assert ctx.tenant_id_hash_or_safe_id == "tenant_a"
    assert ctx.namespace.name == "tenant_a/ws_a"
    assert datetime.now(UTC) + timedelta(seconds=0)
