from __future__ import annotations

import re
from urllib.parse import urlparse

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import raise_security_denial


FORBIDDEN_ARGUMENT_NAMES = {"password", "token", "api_key", "secret", "private_key"}


def detect_path_traversal(value: str) -> bool:
    return "../" in value or "..\\" in value


def detect_ssrf_url(value: str) -> bool:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    return host in {"localhost", "127.0.0.1", "0.0.0.0"} or host.startswith("169.254.")


def detect_command_injection(value: str) -> bool:
    return any(tok in value for tok in [";", "&&", "||", "`", "$("])


def detect_secret_pattern(value: str) -> bool:
    patterns = [r"sk-[A-Za-z0-9]{10,}", r"-----BEGIN PRIVATE KEY-----", r"password\s*=", r"token\s*=", r"api[_-]?key"]
    return any(re.search(p, value, flags=re.IGNORECASE) for p in patterns)


def validate_tool_argument_schema(argument_schema) -> dict[str, object]:
    if not argument_schema or not argument_schema.schema_id:
        raise_security_denial(DenialCategory.VALIDATION_FAILED, "missing argument schema")
    return {"ok": True}


def validate_argument_types(arguments, schema) -> dict[str, object]:
    for arg in arguments:
        expected = schema.argument_types.get(arg.name)
        if expected == "str" and not isinstance(arg.value, str):
            raise_security_denial(DenialCategory.VALIDATION_FAILED, "invalid argument type")
    return {"ok": True}


def validate_argument_lengths(arguments, schema) -> dict[str, object]:
    for arg in arguments:
        limit = schema.max_lengths.get(arg.name)
        if limit is not None and len(str(arg.value)) > limit:
            raise_security_denial(DenialCategory.VALIDATION_FAILED, "argument length violation")
    return {"ok": True}


def validate_forbidden_argument_names(arguments) -> dict[str, object]:
    for arg in arguments:
        if arg.name.lower() in FORBIDDEN_ARGUMENT_NAMES:
            raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "forbidden argument name")
    return {"ok": True}


def validate_no_secret_argument_values(arguments) -> dict[str, object]:
    for arg in arguments:
        if detect_secret_pattern(str(arg.value)):
            raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "secret-like value")
    return {"ok": True}


def validate_file_path_argument(value: str) -> dict[str, object]:
    if detect_path_traversal(value):
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "path traversal")
    return {"ok": True}


def validate_url_argument(value: str) -> dict[str, object]:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise_security_denial(DenialCategory.VALIDATION_FAILED, "invalid URL scheme")
    if detect_ssrf_url(value):
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "ssrf url")
    return {"ok": True}


def validate_domain_argument(value: str, allowed_domains=None, denied_domains=None) -> dict[str, object]:
    allowed_domains = allowed_domains or []
    denied_domains = denied_domains or []
    domain = value.lower()
    if denied_domains and domain in denied_domains:
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "denied domain")
    if allowed_domains and domain not in allowed_domains:
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "domain not allowed")
    return {"ok": True}


def validate_command_argument(value: str) -> dict[str, object]:
    if detect_command_injection(value):
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "command injection")
    return {"ok": True}


def validate_sql_like_argument(value: str) -> dict[str, object]:
    if re.search(r"\b(drop|truncate|delete)\b", value, flags=re.IGNORECASE):
        raise_security_denial(DenialCategory.UNSAFE_TOOL_BLOCKED, "unsafe sql-like argument")
    return {"ok": True}


def validate_prompt_derived_argument(value: str) -> dict[str, object]:
    if re.search(r"ignore previous|system prompt|jailbreak", value, flags=re.IGNORECASE):
        return {"ok": True, "flagged_prompt_injection": True}
    return {"ok": True, "flagged_prompt_injection": False}


def sanitize_tool_arguments(arguments):
    return [{"name": arg.name, "value": "[redacted]" if detect_secret_pattern(str(arg.value)) else str(arg.value)} for arg in arguments]


def validate_tool_arguments(arguments, schema):
    validate_tool_argument_schema(schema)
    validate_forbidden_argument_names(arguments)
    validate_no_secret_argument_values(arguments)
    validate_argument_types(arguments, schema)
    validate_argument_lengths(arguments, schema)
    for arg in arguments:
        if "path" in arg.name:
            validate_file_path_argument(str(arg.value))
        if "url" in arg.name:
            validate_url_argument(str(arg.value))
        if "command" in arg.name:
            validate_command_argument(str(arg.value))
    return {"ok": True, "sanitized_arguments": sanitize_tool_arguments(arguments)}
