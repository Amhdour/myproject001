from __future__ import annotations

import pytest

from backend.security_layer.retrieval.integration_flags import (
    RetrievalIntegrationMode,
    default_retrieval_integration_config,
    is_enforce_mode,
    is_shadow_deny,
)


FUTURE_SCENARIOS = (
    "future shadow-deny records denial and does not block",
    "future enforce blocks cross-tenant document",
    "future enforce blocks unauthorized chunk",
    "future enforce removes unauthorized citation",
    "future enforce excludes unauthorized context chunk",
    "future enforce prevents cache ACL bypass",
    "future enforce returns generic safe denial",
    "feature flag cannot default to enforce",
)


@pytest.mark.parametrize("scenario", FUTURE_SCENARIOS)
@pytest.mark.xfail(reason="future mode not enabled yet", strict=False)
def test_future_mode_skeletons(scenario: str) -> None:
    pytest.skip("future mode not enabled yet")


def test_future_modes_not_enabled_by_default() -> None:
    default_config = default_retrieval_integration_config()
    assert default_config.mode is RetrievalIntegrationMode.DISABLED
    assert not is_shadow_deny(default_config)
    assert not is_enforce_mode(default_config)
