import pytest

from backend.security_layer.monitor_only.feature_flags import IMPLEMENTED_MONITOR_ONLY_FEATURE_FLAG_COUNT
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyFeatureFlags
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyRuntimeMode
from backend.security_layer.monitor_only.feature_flags import default_monitor_only_feature_flags
from backend.security_layer.monitor_only.feature_flags import is_cache_adapter_enabled
from backend.security_layer.monitor_only.feature_flags import is_monitor_only_runtime_enabled
from backend.security_layer.monitor_only.feature_flags import is_shared_sink_enabled
from backend.security_layer.monitor_only.feature_flags import monitor_only_feature_flags_from_env
from backend.security_layer.monitor_only.feature_flags import validate_monitor_only_feature_flags


def test_monitor_only_flags_default_disabled() -> None:
    flags = default_monitor_only_feature_flags()

    assert IMPLEMENTED_MONITOR_ONLY_FEATURE_FLAG_COUNT == 3
    assert not is_monitor_only_runtime_enabled(flags)
    assert not is_shared_sink_enabled(flags)
    assert not is_cache_adapter_enabled(flags)


def test_monitor_only_flags_enable_helpers_only_in_monitor_only_mode() -> None:
    flags = MonitorOnlyFeatureFlags(
        runtime_mode=MonitorOnlyRuntimeMode.MONITOR_ONLY,
        shared_sink_enabled=True,
        cache_adapter_enabled=True,
    )

    assert is_monitor_only_runtime_enabled(flags)
    assert is_shared_sink_enabled(flags)
    assert is_cache_adapter_enabled(flags)


def test_monitor_only_flags_reject_helper_enabled_when_runtime_disabled() -> None:
    flags = MonitorOnlyFeatureFlags(shared_sink_enabled=True)

    with pytest.raises(ValueError, match="disabled"):
        validate_monitor_only_feature_flags(flags)


def test_monitor_only_flags_from_env_are_default_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECURITY_LAYER_MONITOR_ONLY_ENABLED", raising=False)
    monkeypatch.setenv("SECURITY_LAYER_MONITOR_ONLY_SHARED_SINK_ENABLED", "true")
    monkeypatch.setenv("SECURITY_LAYER_MONITOR_ONLY_CACHE_ADAPTER_ENABLED", "true")

    flags = monitor_only_feature_flags_from_env()

    assert flags == default_monitor_only_feature_flags()
