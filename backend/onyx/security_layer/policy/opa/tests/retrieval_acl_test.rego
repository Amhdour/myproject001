package onyx.security.retrieval_acl

import rego.v1

default_input := {
	"subject": {
		"user_id": "user-a",
		"tenant_id": "tenant-a",
		"groups": ["group-a"],
	},
	"resource": {
		"document_id": "doc-a",
		"chunk_id": "chunk-a",
		"tenant_id": "tenant-a",
		"allowed_users": ["user-a"],
		"allowed_groups": [],
		"connector_id": "connector-a",
		"deleted": false,
		"permission_version": "pv-1",
	},
	"action": "rag.context.include",
	"correlation_id": "corr-test",
}

test_same_tenant_allowed_user_allow if {
	result := decision with input as default_input
	result.decision == "allow"
	result.reason == "same tenant allowed user"
}

test_same_tenant_allowed_group_allow if {
	test_input := object.union(default_input, {
		"resource": object.union(default_input.resource, {
			"allowed_users": [],
			"allowed_groups": ["group-a"],
		}),
	})
	result := decision with input as test_input
	result.decision == "allow"
	result.reason == "same tenant allowed group"
}

test_cross_tenant_deny if {
	test_input := object.union(default_input, {
		"resource": object.union(default_input.resource, {"tenant_id": "tenant-b"}),
	})
	result := decision with input as test_input
	result.decision == "deny"
	result.reason == "cross-tenant resource"
}

test_deleted_document_deny if {
	test_input := object.union(default_input, {
		"resource": object.union(default_input.resource, {"deleted": true}),
	})
	result := decision with input as test_input
	result.decision == "deny"
	result.reason == "deleted document"
}

test_missing_tenant_metadata_deny if {
	test_input := object.union(default_input, {
		"resource": object.union(default_input.resource, {"tenant_id": null}),
	})
	result := decision with input as test_input
	result.decision == "deny"
	result.reason == "missing tenant metadata"
}

test_missing_permission_metadata_deny if {
	test_input := object.union(default_input, {
		"resource": object.union(default_input.resource, {"permission_version": null}),
	})
	result := decision with input as test_input
	result.decision == "deny"
	result.reason == "missing permission metadata"
}
