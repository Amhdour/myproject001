from datetime import UTC, datetime, timedelta
import pytest
from backend.security_layer.tools.models import *

@pytest.fixture
def sample_registry():
    return ToolRegistryEntry(
        tool_id='tool1',tool_name='Tool 1',tool_version='v1',tool_owner='sec',tool_category=ToolCategory.INTERNAL,
        tool_risk_tier=ToolRiskTier.HIGH,tool_status=ToolStatus.ACTIVE,allowed_tenant_scope=['t1'],allowed_workspace_scope=['w1'],
        required_user_permissions=['perm1'],required_group_permissions=['grp1'],required_role_permissions=['role1'],
        service_account_allowed=False,delegated_credential_required=True,delegated_credential_scope='scope',approval_required=True,
        approval_risk_level='high',argument_schema_id='schema1',result_safety_policy_id='policy1',audit_required=True,
        finding_required_on_violation=True,metric_required=True,default_effect=ToolDefaultEffect.DENY,metadata_schema_version='1.0',
        tool_description_placeholder='placeholder',
    )

@pytest.fixture
def sample_context():
    return ToolAuthorizationContext(
        request_id='r1',tool_id='tool1',operation=ToolOperationType.EXECUTE,
        caller=ToolCallerContext(caller_id='u1',caller_type='user'),tenant_scope=ToolTenantScope('t1'),workspace_scope=ToolWorkspaceScope('w1'),
        permission_context=ToolPermissionContext(subject_id='u1',user_permissions=['perm1'],group_permissions=['grp1'],role_permissions=['role1']),
        delegated_credential=ToolDelegatedCredential('c1','t1','scope',datetime.now(UTC)+timedelta(days=1)),
        approval_requirement=ToolApprovalRequirement(required=True,approved=False,risk_level='high'),
        argument_schema=ToolArgumentSchema(schema_id='schema1',metadata_schema_version='1.0',argument_types={'prompt':'str'},max_lengths={'prompt':100}),
        arguments=[ToolArgument(name='prompt', value='hello')],
    )
