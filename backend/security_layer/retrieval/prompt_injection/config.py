from __future__ import annotations

import os
from dataclasses import dataclass

from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionMode,
)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionConfig:
    mode: RetrievedContentPromptInjectionMode = RetrievedContentPromptInjectionMode.DISABLED


def parse_retrieved_content_prompt_injection_mode(raw_mode: str | None) -> RetrievedContentPromptInjectionMode:
    if raw_mode is None or raw_mode == "":
        return RetrievedContentPromptInjectionMode.DISABLED
    normalized = raw_mode.strip().lower()
    try:
        return RetrievedContentPromptInjectionMode(normalized)
    except ValueError as exc:
        valid_modes = ", ".join(mode.value for mode in RetrievedContentPromptInjectionMode)
        raise ValueError(
            "Invalid retrieved-content prompt-injection mode: "
            f"{normalized}. Expected one of: {valid_modes}"
        ) from exc


def get_retrieved_content_prompt_injection_config() -> RetrievedContentPromptInjectionConfig:
    return RetrievedContentPromptInjectionConfig(
        mode=parse_retrieved_content_prompt_injection_mode(
            os.getenv("RETRIEVED_CONTENT_PROMPT_INJECTION_MODE")
        )
    )
