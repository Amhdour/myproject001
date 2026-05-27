class PolicyLoadError(Exception):
    """Raised when policy files cannot be loaded."""


class PolicyValidationError(Exception):
    """Raised when policy definitions are invalid."""


class PolicyEvaluationError(Exception):
    """Raised when policy evaluation fails."""


class PolicyDeniedError(PolicyEvaluationError):
    """Raised when an operation is denied by policy."""
