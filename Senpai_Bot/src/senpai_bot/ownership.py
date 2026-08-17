from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ComponentRecord:
    component_id: str
    kind: str
    version: str = ""
    source: str = ""
    install_method: str = ""
    installed_by_senpai: bool = False
    previously_present: bool = False
    path: str = ""
    installed_at_utc: str = ""
    verification: str = ""
    removal_policy: str = "confirmation-required"
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> "ComponentRecord":
        allowed = cls.__dataclass_fields__
        filtered = {key: value for key, value in values.items() if key in allowed}
        if not isinstance(filtered.get("metadata", {}), dict):
            filtered["metadata"] = {}
        return cls(**filtered)


@dataclass
class OwnershipManifest:
    path: Path
    app_version: str
    components: dict[str, ComponentRecord] = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION
    updated_at_utc: str = ""

    @classmethod
    def load(cls, path: Path, app_version: str) -> "OwnershipManifest":
        temporary = path.with_name(f".{path.name}.tmp")
        backup = path.with_suffix(path.suffix + ".bak")
        candidates: list[tuple[int, int, Path]] = []
        for priority, candidate in enumerate((path, temporary, backup), start=1):
            try:
                if candidate.is_file():
                    candidates.append(
                        (candidate.stat().st_mtime_ns, -priority, candidate)
                    )
            except OSError:
                continue
        for _modified, _priority, candidate in sorted(candidates, reverse=True):
            try:
                values = json.loads(candidate.read_text(encoding="utf-8"))
                if values.get("schema_version") != SCHEMA_VERSION:
                    continue
                raw_components = values.get("components", {})
                if not isinstance(raw_components, dict):
                    continue
                components = {
                    component_id: ComponentRecord.from_dict(record)
                    for component_id, record in raw_components.items()
                    if isinstance(component_id, str) and isinstance(record, dict)
                }
                return cls(
                    path=path,
                    app_version=app_version,
                    components=components,
                    updated_at_utc=str(values.get("updated_at_utc", "")),
                )
            except (OSError, TypeError, ValueError):
                continue
        return cls(path=path, app_version=app_version)

    def get(self, component_id: str) -> ComponentRecord | None:
        return self.components.get(component_id)

    def record(self, record: ComponentRecord) -> None:
        if not record.component_id:
            raise ValueError("An ownership record requires a component ID.")
        if not record.installed_at_utc:
            values = asdict(record)
            values["installed_at_utc"] = _utc_now()
            record = ComponentRecord.from_dict(values)
        self.components[record.component_id] = record
        self.save()

    def remove(self, component_id: str) -> None:
        if self.components.pop(component_id, None) is not None:
            self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.updated_at_utc = _utc_now()
        payload = {
            "schema_version": self.schema_version,
            "app_version": self.app_version,
            "updated_at_utc": self.updated_at_utc,
            "components": {
                component_id: asdict(record)
                for component_id, record in sorted(self.components.items())
            },
        }
        temporary = self.path.with_name(f".{self.path.name}.tmp")
        backup = self.path.with_suffix(self.path.suffix + ".bak")
        with temporary.open("w", encoding="utf-8", newline="\n") as output:
            json.dump(payload, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        if self.path.is_file():
            shutil.copy2(self.path, backup)
        os.replace(temporary, self.path)
