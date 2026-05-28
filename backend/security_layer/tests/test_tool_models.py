from backend.security_layer.tools.models import ToolAuthorizationContext, ToolCallerContext, ToolOperationType

def test_tool_authorization_context_creation(sample_context):
    assert isinstance(sample_context, ToolAuthorizationContext)
    assert sample_context.caller == ToolCallerContext(caller_id="u1", caller_type="user")
    assert sample_context.operation == ToolOperationType.EXECUTE
