from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "scenario",
    [
        "future shadow-deny records denial and does not block",
        "future enforce blocks cross-tenant document",
        "future enforce blocks unauthorized chunk",
        "future enforce removes unauthorized citation",
        "future enforce excludes unauthorized context chunk",
        "future enforce prevents cache ACL bypass",
        "future enforce returns generic safe denial",
        "feature flag cannot default to enforce",
    ],
)
@pytest.mark.xfail(reason="future mode not enabled yet", strict=False)
def test_future_mode_skeletons(scenario: str) -> None:
    pytest.skip("future mode not enabled yet")
