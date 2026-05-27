from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from backend.security_layer.policies.exceptions import PolicyLoadError
from backend.security_layer.policies.models import EnforcementMode
from backend.security_layer.policies.models import Policy
from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.policies.models import PolicyRule
from backend.security_layer.policies.models import PolicyScope
from backend.security_layer.policies.models import RiskLevel

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


SUPPORTED_EXTENSIONS = {".json", ".yaml", ".yml"}


def compute_policy_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _load_raw(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PolicyLoadError(f"missing policy file: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise PolicyLoadError(f"unsupported extension: {path.suffix}")

    raw = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()
    if ext == ".json":
        return json.loads(raw)
    if yaml is None:
        raise PolicyLoadError("YAML loading unavailable; install PyYAML or use JSON")
    return yaml.safe_load(raw)


def _to_policy(data: dict[str, Any]) -> Policy:
    rules = []
    for rule in data.get("rules", []):
        rules.append(
            PolicyRule(
                rule_id=rule.get("rule_id", ""),
                effect=PolicyEffect(rule.get("effect")),
                actions=rule.get("actions", []),
                required_context=rule.get("required_context", []),
                reason=rule.get("reason", ""),
                risk_level=RiskLevel(rule.get("risk_level", "low")),
            )
        )

    return Policy(
        policy_id=data.get("policy_id", ""),
        version=data.get("version", ""),
        scope=PolicyScope(data.get("scope")),
        default_effect=PolicyEffect(data.get("default_effect", "deny")),
        enforcement_mode=EnforcementMode(data.get("enforcement_mode", "disabled")),
        rules=rules,
    )


def load_policy_file(path: str | Path) -> Policy:
    path_obj = Path(path)
    data = _load_raw(path_obj)
    if not isinstance(data, dict):
        raise PolicyLoadError("policy file must parse to an object")
    return _to_policy(data)


def load_policy_directory(path: str | Path) -> list[Policy]:
    path_obj = Path(path)
    if not path_obj.exists() or not path_obj.is_dir():
        raise PolicyLoadError(f"missing policy directory: {path}")

    policies: list[Policy] = []
    for policy_file in sorted(path_obj.iterdir()):
        if policy_file.suffix.lower() in SUPPORTED_EXTENSIONS:
            policies.append(load_policy_file(policy_file))
    return policies
