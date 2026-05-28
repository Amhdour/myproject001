from backend.security_layer.cache.key_contract import REQUIRED_CACHE_KEY_FIELDS
from backend.security_layer.cache.models import CacheACLContext
from backend.security_layer.cache.models import CacheEntryMetadata
from backend.security_layer.cache.models import CacheKey
from backend.security_layer.cache.models import CacheOperationType
from backend.security_layer.cache.models import CacheProvenance
from backend.security_layer.cache.models import CacheSecurityContext
from backend.security_layer.cache.models import CacheSecurityStage
from backend.security_layer.cache.models import CacheSourceType
from backend.security_layer.monitor_only.cache_adapter import monitor_only_cache_dry_run
from backend.security_layer.monitor_only.cache_adapter import preserve_cache_result_with_monitor_only_dry_run
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyFeatureFlags
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyRuntimeMode
from backend.security_layer.monitor_only.models import MonitorOnlyDecision
from backend.security_layer.runtime.audit import clear_audit_events
from backend.security_layer.runtime.audit import get_audit_events
from backend.security_layer.runtime.findings import clear_findings
from backend.security_layer.runtime.findings import get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics
from backend.security_layer.runtime.metrics import get_security_metrics


def _enabled_flags() -> MonitorOnlyFeatureFlags:
    return MonitorOnlyFeatureFlags(
        runtime_mode=MonitorOnlyRuntimeMode.MONITOR_ONLY,
        shared_sink_enabled=True,
        cache_adapter_enabled=True,
    )


def _ctx(subject: str | None = "subject-safe") -> CacheSecurityContext:
    return CacheSecurityContext(
        stage=CacheSecurityStage.CACHE_READ_REQUESTED,
        operation=CacheOperationType.READ,
        request_id="req-1",
        tenant_id_hash_or_safe_id="tenant-safe",
        workspace_id_hash_or_safe_id="workspace-safe",
        subject_id_hash_or_safe_id=subject,
        acl_context=CacheACLContext("acl-id", "v1", "2099-01-01T00:00:00Z"),
        provenance=CacheProvenance("prov-1", CacheSourceType.SYSTEM),
    )


def _metadata(ttl: int = 60) -> CacheEntryMetadata:
    key = {k: "safe" for k in REQUIRED_CACHE_KEY_FIELDS}
    key["cache_key_schema_version"] = "v1"
    key["cache_ttl_seconds"] = ttl
    return CacheEntryMetadata(cache_key=CacheKey(key), cache_ttl_seconds=ttl)


def test_cache_adapter_skips_when_disabled() -> None:
    observation = monitor_only_cache_dry_run(MonitorOnlyFeatureFlags(), context=_ctx(), metadata=_metadata())

    assert observation.decision is MonitorOnlyDecision.SKIPPED_DISABLED


def test_cache_adapter_emits_monitor_only_observation_without_blocking() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()

    observation = monitor_only_cache_dry_run(_enabled_flags(), context=_ctx(), metadata=_metadata())

    assert observation.decision is MonitorOnlyDecision.OBSERVED
    assert "no blocking" in observation.notes
    assert "no filtering" in observation.notes
    assert "original return value preserved" in observation.notes
    assert get_audit_events()
    assert not get_findings()
    assert get_security_metrics()


def test_cache_adapter_records_finding_for_invalid_context_but_preserves_result() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()
    original_result = {"cache": "hit"}

    returned_result = preserve_cache_result_with_monitor_only_dry_run(
        original_result,
        _enabled_flags(),
        context=_ctx(subject=None),
        metadata=_metadata(ttl=-1),
    )

    assert returned_result is original_result
    assert get_audit_events()
    assert get_findings()[0].reason_code == "monitor_only_invalid_cache_context"
    assert get_security_metrics()
