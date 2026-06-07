from __future__ import annotations

import re
from collections.abc import Iterable

from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentChunkLike,
)

_PROMPT_INJECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "instruction_override",
        re.compile(
            r"(?:ignore|disregard|forget).{0,60}(?:prior|previous|above).{0,60}(?:instructions?|prompts?|system prompt)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "role_override",
        re.compile(
            r"(?:you are now|pretend to be|act as|system:|developer:|assistant:)",
            re.IGNORECASE,
        ),
    ),
    (
        "exfiltration_request",
        re.compile(
            r"(?:exfiltrat|leak|send|upload|post|email|transmit).{0,60}(?:context|prompt|secret|secrets|token|api key|credentials|conversation)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "tool_abuse_request",
        re.compile(
            r"(?:call|invoke|execute|run).{0,60}(?:tool|function|shell|terminal|mcp).{0,60}(?:without|ignore).{0,60}(?:approval|permission|policy)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "override_marker",
        re.compile(
            r"(?:prompt injection|hidden instruction|malicious instruction|override all|bypass guardrails)",
            re.IGNORECASE,
        ),
    ),
)


def _metadata_values(metadata: dict[str, str | list[str]]) -> Iterable[str]:
    for value in metadata.values():
        if isinstance(value, list):
            for item in value:
                yield str(item)
            continue
        yield str(value)


def _chunk_text(chunk: RetrievedContentChunkLike) -> str:
    text_parts = [
        getattr(chunk, "blurb", None),
        getattr(chunk, "doc_summary", None),
        getattr(chunk, "chunk_context", None),
        *getattr(chunk, "match_highlights", []),
        *list(_metadata_values(getattr(chunk, "metadata", {}))),
    ]
    return "\n".join(part for part in text_parts if part)


def detect_retrieved_content_prompt_injection_signals(
    chunk: RetrievedContentChunkLike,
) -> tuple[str, ...]:
    text = _chunk_text(chunk)
    if not text:
        return ()

    matched_patterns: list[str] = []
    for pattern_name, pattern in _PROMPT_INJECTION_PATTERNS:
        if pattern.search(text):
            matched_patterns.append(pattern_name)
    return tuple(matched_patterns)


def has_prompt_injection_signals(chunk: RetrievedContentChunkLike) -> bool:
    return bool(detect_retrieved_content_prompt_injection_signals(chunk))


def prompt_injection_pattern_names() -> tuple[str, ...]:
    return tuple(pattern_name for pattern_name, _ in _PROMPT_INJECTION_PATTERNS)
