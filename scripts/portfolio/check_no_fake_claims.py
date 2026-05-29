#!/usr/bin/env python3
"""Fail on fake or unsupported security/compliance evidence claims."""

from __future__ import annotations

from pathlib import Path
import string
import sys

ROOT = Path(__file__).resolve().parents[2]
SCAN_TARGETS = [ROOT / "README.md", ROOT / "portfolio", ROOT / "docs/security"]
TEXT_SUFFIXES = {".md", ".txt", ".yml", ".yaml"}
UNSAFE_PHRASES = [
    "guaranteed secure",
    "fully secure",
    "certified secure",
    "production protected",
    "enterprise protected",
    "verified by external auditor",
    "soc 2 certified",
    "iso 27001 certified",
    "gdpr compliant",
    "hipaa compliant",
]
SAFE_MARKERS = [
    "not certified",
    "not claimed",
    "compliance certification: not claimed",
    "external validation: pending",
    "production readiness: no-go",
    "enterprise readiness: no-go",
    "does not prove",
    "do not claim",
    "must not claim",
    "do not say",
    "before making",
    "no-go",
    ": no",
    "pending",
    "not prove",
    "not compliant",
    "not a claim",
    "forbidden claim",
    "forbidden claims",
    "unsupported",
    "unsafe wording",
    "unsafe phrase",
    "non-claim",
    "non-claims",
]
NEGATION_WORDS = {"not", "no", "never", "without"}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for target in SCAN_TARGETS:
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(
                path
                for path in target.rglob("*")
                if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
            )
    return sorted(files)


def tokenize(value: str) -> list[str]:
    table = str.maketrans({char: " " for char in string.punctuation})
    return value.translate(table).split()


def has_near_negation(line: str, phrase: str) -> bool:
    words = tokenize(line)
    phrase_words = tokenize(phrase)
    if not phrase_words:
        return False
    for index in range(0, len(words) - len(phrase_words) + 1):
        if words[index : index + len(phrase_words)] == phrase_words:
            window = words[max(0, index - 4) : index]
            return any(word in NEGATION_WORDS for word in window)
    return False


def is_safe_boundary_line(line: str, phrase: str, context: list[str] | None = None) -> bool:
    normalized = " ".join(line.lower().split())
    context_text = " ".join(context or [])
    return (
        any(marker in normalized for marker in SAFE_MARKERS)
        or any(marker in context_text for marker in SAFE_MARKERS)
        or has_near_negation(normalized, phrase)
    )


def main() -> int:
    violations: list[tuple[Path, int, str, str]] = []
    checked_files = iter_files()

    for path in checked_files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        normalized_lines = [" ".join(line.lower().split()) for line in lines]
        for line_number, line in enumerate(lines, start=1):
            normalized = normalized_lines[line_number - 1]
            prior_context = normalized_lines[max(0, line_number - 12) : line_number - 1]
            for phrase in UNSAFE_PHRASES:
                if phrase in normalized and not is_safe_boundary_line(line, phrase, prior_context):
                    violations.append((path.relative_to(ROOT), line_number, phrase, line.strip()))

    if violations:
        print("FAIL: fake or unsupported security/compliance claims found.")
        for path, line_number, phrase, line in violations:
            print(f"- {path}:{line_number}: matched {phrase!r}: {line}")
        return 1

    print(
        "PASS: fake-claim check found no unsupported positive evidence claims "
        f"across {len(checked_files)} reviewer-facing files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
