from __future__ import annotations

from typing import TypeVar

from backend.security_layer.cache.models import CacheEntryMetadata
from backend.security_layer.cache.models import CacheSecurityContext
from backend.security_layer.cache.validators import validate_cache_context
from backend.security_layer.cache.validators import validate_cache_entry_metadata
from backend.security_layer.cache.validators import validate_cache_entry_ttl
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyFeatureFlags
from backend.security_layer.monitor_only.feature_flags import is_cache_adapter_enabled
from backend.security_layer.monitor_only.models import MonitorOnlyCandidate
from backend.security_layer.monitor_only.models import MonitorOnlyDecision
from backend.security_layer.monitor_only.models import MonitorOnlyObservation
from backend.security_layer.monitor_only.shared_sink import write_monitor_only_signals

T = TypeVar("T")


def monitor_only_cache_dry_run(
    flags: MonitorOnlyFeatureFlags,
    *,
    context: CacheSecurityContext,
    metadata: CacheEntryMetadata | None = None,
) -> MonitorOnlyObservation:
    try:
        enabled = is_cache_adapter_enabled(flags)
    except ValueError:
        enabled = False
    if not enabled:
        return MonitorOnlyObservation(
            candidate=MonitorOnlyCandidate.CACHE_DRY_RUN_ADAPTER,
            decision=MonitorOnlyDecision.SKIPPED_DISABLED,
            request_id=context.request_id,
            notes=("cache adapter disabled or invalid",),
        )

    notes: list[str] = []
    reason_code: str | None = None
    if not validate_cache_context(context):
        notes.append("invalid cache context observed")
        reason_code = "monitor_only_invalid_cache_context"
    if metadata is not None and not validate_cache_entry_metadata(metadata):
        notes.append("invalid cache metadata observed")
        reason_code = reason_code or "monitor_only_invalid_cache_metadata"
    if metadata is not None and not validate_cache_entry_ttl(metadata):
        notes.append("invalid cache ttl observed")
        reason_code = reason_code or "monitor_only_invalid_cache_ttl"
    if not notes:
        notes.append("cache dry-run observed without behavior change")

    sink_observation = write_monitor_only_signals(
        flags,
        request_id=context.request_id,
        action=context.stage.value,
        decision="observed",
        reason_code=reason_code,
        details={"operation": context.operation.value, "cache_purpose": context.cache_purpose.value},
    )

    return MonitorOnlyObservation(
        candidate=MonitorOnlyCandidate.CACHE_DRY_RUN_ADAPTER,
        decision=MonitorOnlyDecision.OBSERVED,
        request_id=context.request_id,
        signals=sink_observation.signals,
        notes=tuple(notes) + ("no blocking", "no filtering", "original return value preserved"),
    )


def preserve_cache_result_with_monitor_only_dry_run(
    original_result: T,
    flags: MonitorOnlyFeatureFlags,
    *,
    context: CacheSecurityContext,
    metadata: CacheEntryMetadata | None = None,
) -> T:
    monitor_only_cache_dry_run(flags, context=context, metadata=metadata)
    return original_result
