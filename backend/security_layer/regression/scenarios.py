"""Scenario catalog for the isolated regression/demo attack bundle."""

from __future__ import annotations

from backend.security_layer.regression.models import RegressionDemoExpectedResult
from backend.security_layer.regression.models import RegressionDemoFamily
from backend.security_layer.regression.models import RegressionDemoFixtureType
from backend.security_layer.regression.models import RegressionDemoScenario
from backend.security_layer.regression.models import RegressionDemoScenarioStatus
from backend.security_layer.regression.models import RegressionDemoSeverity

RDA_EVIDENCE_DIR = "docs/security/evidence/regression_demo_attack_bundle"


def _scenario(
    scenario_id: str,
    title: str,
    family: RegressionDemoFamily,
    expected: RegressionDemoExpectedResult,
    fixture_type: RegressionDemoFixtureType,
    controls: tuple[str, ...],
    risks: tuple[str, ...],
    severity: RegressionDemoSeverity = RegressionDemoSeverity.MEDIUM,
) -> RegressionDemoScenario:
    return RegressionDemoScenario(
        scenario_id=scenario_id,
        title=title,
        family=family,
        status=RegressionDemoScenarioStatus.IMPLEMENTED,
        expected_result=expected,
        severity=severity,
        fixture_type=fixture_type,
        mapped_controls=controls,
        mapped_risks=risks,
        evidence_ref=f"{RDA_EVIDENCE_DIR}/scenario_coverage.md#{scenario_id.lower()}",
    )


REGRESSION_DEMO_SCENARIOS: tuple[RegressionDemoScenario, ...] = (
    _scenario(
        "RDA-001",
        "same-tenant retrieval allowed",
        RegressionDemoFamily.UNAUTHORIZED_RETRIEVAL,
        RegressionDemoExpectedResult.ALLOWED,
        RegressionDemoFixtureType.SYNTHETIC_RETRIEVAL,
        ("retrieval_acl", "monitor_only"),
        ("R-RET-001",),
        RegressionDemoSeverity.INFO,
    ),
    _scenario(
        "RDA-002",
        "cross-tenant retrieval denied/simulated-denied",
        RegressionDemoFamily.CROSS_TENANT_RETRIEVAL,
        RegressionDemoExpectedResult.SIMULATED_DENY_NO_BLOCK,
        RegressionDemoFixtureType.SYNTHETIC_RETRIEVAL,
        ("retrieval_acl", "shadow_deny"),
        ("R-RET-002", "R-SD-001"),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-003",
        "stale ACL retrieval flagged",
        RegressionDemoFamily.STALE_DELETED_ACL_RETRIEVAL,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_RETRIEVAL,
        ("retrieval_acl", "audit_finding_metric"),
        ("R-RET-003",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-004",
        "deleted document retrieval flagged",
        RegressionDemoFamily.STALE_DELETED_ACL_RETRIEVAL,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_RETRIEVAL,
        ("retrieval_acl", "safe_denial"),
        ("R-RET-004",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-005",
        "vector namespace mismatch flagged",
        RegressionDemoFamily.VECTOR_METADATA_MISMATCH,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_VECTOR,
        ("vector_security", "audit_finding_metric"),
        ("R-VEC-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-006",
        "vector ACL metadata mismatch flagged",
        RegressionDemoFamily.VECTOR_METADATA_MISMATCH,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_VECTOR,
        ("vector_security", "retrieval_acl"),
        ("R-VEC-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-007",
        "cache tenant mismatch flagged",
        RegressionDemoFamily.CACHE_TENANT_ACL_COLLISION,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_CACHE,
        ("cache_security", "monitor_only"),
        ("R-CACHE-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-008",
        "cache ACL version mismatch flagged",
        RegressionDemoFamily.CACHE_TENANT_ACL_COLLISION,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_CACHE,
        ("cache_security", "retrieval_acl"),
        ("R-CACHE-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-009",
        "unauthorized tool call flagged/denied in isolated control",
        RegressionDemoFamily.UNAUTHORIZED_TOOL_CALL,
        RegressionDemoExpectedResult.BLOCKED_ISOLATED_CONTROL,
        RegressionDemoFixtureType.SYNTHETIC_TOOL,
        ("tool_authorization", "safe_denial"),
        ("R-TOOL-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-010",
        "high-risk tool requires approval",
        RegressionDemoFamily.UNAUTHORIZED_TOOL_CALL,
        RegressionDemoExpectedResult.APPROVAL_REQUIRED,
        RegressionDemoFixtureType.SYNTHETIC_TOOL,
        ("tool_authorization", "approval_workflow"),
        ("R-TOOL-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-011",
        "prompt-to-tool injection marker flagged",
        RegressionDemoFamily.PROMPT_TO_TOOL_ABUSE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_TOOL,
        ("tool_authorization", "prompt_safety"),
        ("R-TOOL-003",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-012",
        "unknown MCP server flagged/denied in isolated control",
        RegressionDemoFamily.MCP_CONFUSED_DEPUTY,
        RegressionDemoExpectedResult.BLOCKED_ISOLATED_CONTROL,
        RegressionDemoFixtureType.SYNTHETIC_MCP,
        ("mcp_hardening", "registry_contract"),
        ("R-MCP-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-013",
        "MCP confused-deputy marker flagged",
        RegressionDemoFamily.MCP_CONFUSED_DEPUTY,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_MCP,
        ("mcp_hardening", "request_validation"),
        ("R-MCP-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-014",
        "MCP credential boundary violation flagged",
        RegressionDemoFamily.MCP_CREDENTIAL_MISUSE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_MCP,
        ("mcp_hardening", "credential_isolation"),
        ("R-MCP-003",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-015",
        "artifact raw secret flagged",
        RegressionDemoFamily.ARTIFACT_SECRET_LEAKAGE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_ARTIFACT,
        ("artifact_safety", "content_scanning"),
        ("R-ART-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-016",
        "artifact unauthorized document marker flagged",
        RegressionDemoFamily.ARTIFACT_DOCUMENT_LEAKAGE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_ARTIFACT,
        ("artifact_safety", "retrieval_acl"),
        ("R-ART-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-017",
        "artifact prompt-injection marker flagged",
        RegressionDemoFamily.ARTIFACT_SECRET_LEAKAGE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_ARTIFACT,
        ("artifact_safety", "prompt_safety"),
        ("R-ART-003",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-018",
        "monitor-only cache adapter does not block",
        RegressionDemoFamily.MONITOR_ONLY_NO_BLOCK,
        RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        RegressionDemoFixtureType.SYNTHETIC_MONITOR_ONLY,
        ("monitor_only", "cache_security"),
        ("R-MON-001",),
        RegressionDemoSeverity.MEDIUM,
    ),
    _scenario(
        "RDA-019",
        "monitor-only shared sink fails open",
        RegressionDemoFamily.MONITOR_ONLY_NO_BLOCK,
        RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        RegressionDemoFixtureType.SYNTHETIC_MONITOR_ONLY,
        ("monitor_only", "audit_finding_metric"),
        ("R-MON-002",),
        RegressionDemoSeverity.MEDIUM,
    ),
    _scenario(
        "RDA-020",
        "shadow-deny simulated deny does not block",
        RegressionDemoFamily.SHADOW_DENY_SAFETY,
        RegressionDemoExpectedResult.SIMULATED_DENY_NO_BLOCK,
        RegressionDemoFixtureType.SYNTHETIC_SHADOW_DENY,
        ("shadow_deny", "safe_denial"),
        ("R-SD-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-021",
        "enforce-mode activation blocked by missing gates",
        RegressionDemoFamily.ENFORCE_MODE_GATE_BLOCK,
        RegressionDemoExpectedResult.ENFORCE_ACTIVATION_BLOCKED,
        RegressionDemoFixtureType.SYNTHETIC_ENFORCE_MODE,
        ("enforce_mode_readiness", "activation_gates"),
        ("R-ENF-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-022",
        "enforce-mode kill switch keeps live effect no_change",
        RegressionDemoFamily.ENFORCE_MODE_GATE_BLOCK,
        RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        RegressionDemoFixtureType.SYNTHETIC_ENFORCE_MODE,
        ("enforce_mode_readiness", "kill_switch"),
        ("R-ENF-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-023",
        "safe denial does not leak raw internals",
        RegressionDemoFamily.SAFE_DENIAL_NON_LEAKAGE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_SAFE_DENIAL,
        ("safe_denial", "non_leakage"),
        ("R-SAFE-001",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-024",
        "audit/finding/metric evidence emitted",
        RegressionDemoFamily.AUDIT_FINDING_METRIC,
        RegressionDemoExpectedResult.EVIDENCE_EMITTED,
        RegressionDemoFixtureType.SYNTHETIC_SAFE_DENIAL,
        ("audit_finding_metric", "runtime_evidence"),
        ("R-AUD-001",),
        RegressionDemoSeverity.MEDIUM,
    ),
    _scenario(
        "RDA-025",
        "non-leakage across all decision summaries",
        RegressionDemoFamily.SAFE_DENIAL_NON_LEAKAGE,
        RegressionDemoExpectedResult.FLAGGED,
        RegressionDemoFixtureType.SYNTHETIC_SAFE_DENIAL,
        ("non_leakage", "safe_denial"),
        ("R-SAFE-002",),
        RegressionDemoSeverity.HIGH,
    ),
    _scenario(
        "RDA-026",
        "production behavior unchanged",
        RegressionDemoFamily.MONITOR_ONLY_NO_BLOCK,
        RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        RegressionDemoFixtureType.SYNTHETIC_MONITOR_ONLY,
        ("monitor_only", "no_live_blocking", "no_live_filtering"),
        ("R-RDA-006",),
        RegressionDemoSeverity.HIGH,
    ),
)


def get_regression_demo_scenarios() -> tuple[RegressionDemoScenario, ...]:
    return REGRESSION_DEMO_SCENARIOS


def validate_regression_demo_scenario(scenario: RegressionDemoScenario) -> bool:
    if not scenario.scenario_id.startswith("RDA-"):
        raise ValueError("invalid regression demo scenario ID")
    if not scenario.mapped_controls:
        raise ValueError("scenario must map explicit controls")
    if not scenario.mapped_risks:
        raise ValueError("scenario must map explicit risks")
    if not scenario.evidence_ref:
        raise ValueError("scenario must include evidence reference")
    if scenario.status is not RegressionDemoScenarioStatus.IMPLEMENTED:
        raise ValueError("scenario must be implemented for this bundle")
    return True


def validate_all_regression_demo_scenarios() -> bool:
    seen: set[str] = set()
    for scenario in REGRESSION_DEMO_SCENARIOS:
        validate_regression_demo_scenario(scenario)
        if scenario.scenario_id in seen:
            raise ValueError("duplicate regression demo scenario ID")
        seen.add(scenario.scenario_id)
    if len(REGRESSION_DEMO_SCENARIOS) < 26:
        raise ValueError("at least 26 regression demo scenarios are required")
    return True


def _scenario_by_id(scenario_id: str) -> RegressionDemoScenario:
    for scenario in REGRESSION_DEMO_SCENARIOS:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise ValueError("unknown regression demo scenario ID")


def map_scenario_to_controls(scenario_id: str) -> tuple[str, ...]:
    return _scenario_by_id(scenario_id).mapped_controls


def map_scenario_to_expected_result(
    scenario_id: str,
) -> RegressionDemoExpectedResult:
    return _scenario_by_id(scenario_id).expected_result
