from __future__ import annotations


def build_retrieval_security_fixtures() -> dict[str, dict[str, object]]:
    tenant_a = {"id": "fake_tenant_alpha", "label": "synthetic_tenant_alpha"}
    tenant_b = {"id": "fake_tenant_beta", "label": "synthetic_tenant_beta"}
    user_allowed = {"id": "fake_user_allowed", "email": "synthetic_user_allowed@fake.invalid"}
    user_denied = {"id": "fake_user_denied", "email": "synthetic_user_denied@fake.invalid"}
    group_allowed = {"id": "fake_group_allowed", "name": "synthetic_group_allowed"}
    group_denied = {"id": "fake_group_denied", "name": "synthetic_group_denied"}
    role_allowed = {"id": "fake_role_allowed", "name": "synthetic_role_allowed"}
    role_denied = {"id": "fake_role_denied", "name": "synthetic_role_denied"}

    document_allowed = {"id": "fake_doc_allowed", "tenant_id": tenant_a["id"], "deleted": False, "placeholder": "SYNTHETIC_DOC_PLACEHOLDER"}
    document_cross_tenant = {"id": "fake_doc_cross_tenant", "tenant_id": tenant_b["id"], "deleted": False, "synthetic_cross_tenant": True}
    document_deleted = {"id": "fake_doc_deleted", "tenant_id": tenant_a["id"], "deleted": True}

    chunk_allowed = {"id": "fake_chunk_allowed", "document_id": document_allowed["id"], "tenant_id": tenant_a["id"], "chunk_placeholder": "SYNTHETIC_CHUNK_PLACEHOLDER"}
    chunk_cross_tenant = {"id": "fake_chunk_cross_tenant", "document_id": document_cross_tenant["id"], "tenant_id": tenant_b["id"], "synthetic_cross_tenant": True}
    chunk_denied_group = {"id": "fake_chunk_denied_group", "document_id": document_allowed["id"], "tenant_id": tenant_a["id"], "denied_group_id": group_denied["id"], "unauthorized": True}
    chunk_denied_role = {"id": "fake_chunk_denied_role", "document_id": document_allowed["id"], "tenant_id": tenant_a["id"], "denied_role_id": role_denied["id"], "unauthorized": True}

    stale_acl_snapshot = {"id": "fake_acl_stale", "tenant_id": tenant_a["id"], "stale": True, "fresh": False}
    fresh_acl_snapshot = {"id": "fake_acl_fresh", "tenant_id": tenant_a["id"], "stale": False, "fresh": True}

    vector_namespace_allowed = {"id": "fake_vector_ns_allowed", "namespace": "tenant:fake_tenant_alpha"}
    vector_namespace_denied = {"id": "fake_vector_ns_denied", "namespace": "tenant:fake_tenant_beta", "unauthorized": True}
    vector_metadata_allowed = {"id": "fake_vector_meta_allowed", "tenant_id": tenant_a["id"], "security_scope": "synthetic_scope_allowed"}
    vector_metadata_denied = {"id": "fake_vector_meta_denied", "tenant_id": tenant_b["id"], "security_scope": "synthetic_scope_denied", "unauthorized": True}

    cache_entry_allowed = {"id": "fake_cache_allowed", "tenant_id": tenant_a["id"], "cache_key": "synthetic_cache_key_allowed"}
    cache_entry_cross_tenant = {"id": "fake_cache_cross_tenant", "tenant_id": tenant_b["id"], "cache_key": "synthetic_cache_key_cross_tenant", "synthetic_cross_tenant": True}

    citation_allowed = {"id": "fake_citation_allowed", "document_id": document_allowed["id"], "unauthorized": False}
    citation_denied = {"id": "fake_citation_denied", "document_id": document_cross_tenant["id"], "unauthorized": True}

    rerank_candidate_allowed = {"id": "fake_rerank_allowed", "candidate_id": "fake_doc_allowed__fake_chunk_allowed", "unauthorized": False}
    rerank_candidate_denied = {"id": "fake_rerank_denied", "candidate_id": "fake_doc_cross_tenant__fake_chunk_cross_tenant", "unauthorized": True}

    return locals()
