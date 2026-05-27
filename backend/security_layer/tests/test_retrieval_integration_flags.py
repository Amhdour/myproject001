import pytest

from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig, RetrievalIntegrationMode, default_retrieval_integration_config, validate_retrieval_integration_config


def test_default_config_is_not_enforce() -> None:
    cfg = default_retrieval_integration_config()
    assert cfg.mode in {RetrievalIntegrationMode.DISABLED, RetrievalIntegrationMode.MONITOR_ONLY}
    assert cfg.mode != RetrievalIntegrationMode.ENFORCE


def test_invalid_mode_rejected() -> None:
    with pytest.raises(ValueError):
        validate_retrieval_integration_config(RetrievalIntegrationConfig(mode="bad"))  # type: ignore[arg-type]
