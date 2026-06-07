package onyx.security.retrieval_acl

import rego.v1

policy_package := "onyx.security.retrieval_acl"
policy_version := "v1"
retrieval_action := "rag.context.include"

decision := {
	"decision": "deny",
	"reason": "missing tenant metadata",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	missing_tenant_metadata
} else := {
	"decision": "deny",
	"reason": "cross-tenant resource",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	cross_tenant_resource
} else := {
	"decision": "deny",
	"reason": "deleted document",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	input.resource.deleted == true
} else := {
	"decision": "deny",
	"reason": "missing permission metadata",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	missing_permission_metadata
} else := {
	"decision": "allow",
	"reason": "same tenant allowed user",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	valid_action
	same_tenant
	input.subject.user_id in input.resource.allowed_users
} else := {
	"decision": "allow",
	"reason": "same tenant allowed group",
	"policy_package": policy_package,
	"policy_version": policy_version,
} if {
	valid_action
	same_tenant
	some group in input.subject.groups
	group in input.resource.allowed_groups
} else := {
	"decision": "deny",
	"reason": "subject is not permitted for resource",
	"policy_package": policy_package,
	"policy_version": policy_version,
}

valid_action if {
	input.action == retrieval_action
}

same_tenant if {
	input.subject.tenant_id == input.resource.tenant_id
}

missing_tenant_metadata if {
	object.get(input.subject, "tenant_id", null) == null
} else if {
	object.get(input.resource, "tenant_id", null) == null
}

cross_tenant_resource if {
	input.subject.tenant_id
	input.resource.tenant_id
	input.subject.tenant_id != input.resource.tenant_id
}

missing_permission_metadata if {
	object.get(input.resource, "permission_version", null) == null
} else if {
	count(object.get(input.resource, "allowed_users", [])) == 0
	count(object.get(input.resource, "allowed_groups", [])) == 0
}
