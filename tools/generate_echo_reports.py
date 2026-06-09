#!/usr/bin/env python3
"""Small report generator used by SDK template validation fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReportContext:
    root: Path
    channel: str
    run_id: str
    status: str
    pack_id: str
    notes: str


def collect_context(
    root: Path | str,
    channel: str,
    run_id: str,
    status: str,
    pack_id: str,
    notes: str,
) -> ReportContext:
    return ReportContext(Path(root), channel, run_id, status, pack_id, notes)


def create_reports(context: ReportContext) -> dict[str, dict[str, Any]]:
    modules = _scan_modules(context.root)
    graph_nodes = [
        {
            "id": module["moduleId"],
            "label": module["name"],
            "version": module["version"],
            "path": module["path"],
        }
        for module in modules
    ]
    return {
        "scanned-modules.json": {
            "schema": "echo.reports.scanned_modules.v1",
            "channel": context.channel,
            "runId": context.run_id,
            "status": context.status,
            "packId": context.pack_id,
            "notes": context.notes,
            "data": {
                "scannedModules": {
                    "moduleCount": len(modules),
                    "modules": modules,
                }
            },
        },
        "module-graph.json": {
            "schema": "echo.reports.module_graph.v1",
            "channel": context.channel,
            "runId": context.run_id,
            "status": context.status,
            "packId": context.pack_id,
            "notes": context.notes,
            "data": {
                "moduleGraph": {
                    "nodeCount": len(graph_nodes),
                    "nodes": graph_nodes,
                    "edges": [],
                }
            },
        },
    }


def write_reports(root: Path | str, reports: dict[str, dict[str, Any]], context: ReportContext) -> None:
    del context
    report_root = Path(root) / "reports" / "echo"
    report_root.mkdir(parents=True, exist_ok=True)
    for name, payload in reports.items():
        (report_root / name).write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_json(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _scan_modules(root: Path) -> list[dict[str, Any]]:
    modules_root = root / "addons"
    modules: list[dict[str, Any]] = []
    if not modules_root.is_dir():
        return modules
    for descriptor in sorted(modules_root.glob("*/src/main/resources/META-INF/echo.mod.json")):
        payload = load_json(descriptor)
        module_root = descriptor.parents[4]
        module_id = str(payload.get("id") or module_root.name)
        modules.append(
            {
                "moduleId": module_id,
                "name": str(payload.get("name") or module_id),
                "version": str(payload.get("version") or ""),
                "path": module_root.relative_to(root).as_posix(),
                "role": str(payload.get("role") or ""),
                "provides": list(payload.get("provides") or []),
                "requires": list(payload.get("requires") or []),
                "optional": list(payload.get("optional") or []),
            }
        )
    return modules
