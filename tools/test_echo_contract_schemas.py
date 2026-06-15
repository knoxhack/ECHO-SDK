#!/usr/bin/env python3
"""Dependency-free fixture tests for the public ECHO contract schemas."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_FIXTURES: dict[str, Path] = {
    "content-graph-evidence.schema.json": REPO_ROOT / "fixtures" / "content-graph-evidence.generated.json",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def type_matches(expected: str | list[str], value: Any) -> bool:
    expected_types = expected if isinstance(expected, list) else [expected]
    for expected_type in expected_types:
        if expected_type == "object" and isinstance(value, dict):
            return True
        if expected_type == "array" and isinstance(value, list):
            return True
        if expected_type == "string" and isinstance(value, str):
            return True
        if expected_type == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if expected_type == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if expected_type == "boolean" and isinstance(value, bool):
            return True
        if expected_type == "null" and value is None:
            return True
    return False


def validate_value(schema: dict[str, Any], value: Any, pointer: str = "$") -> list[str]:
    errors: list[str] = []
    if "type" in schema and not type_matches(schema["type"], value):
        errors.append(f"{pointer} expected type {schema['type']}")
        return errors
    if "const" in schema and value != schema["const"]:
        errors.append(f"{pointer} expected const {schema['const']}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{pointer} expected one of {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            errors.append(f"{pointer} expected minLength {schema['minLength']}")
        if "pattern" in schema and not re.match(str(schema["pattern"]), value):
            errors.append(f"{pointer} did not match pattern {schema['pattern']}")
    if isinstance(value, int) and "minimum" in schema and value < int(schema["minimum"]):
        errors.append(f"{pointer} expected minimum {schema['minimum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            errors.append(f"{pointer} expected minItems {schema['minItems']}")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{pointer} expected uniqueItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_value(item_schema, item, f"{pointer}[{index}]"))
    if isinstance(value, dict):
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"{pointer}.{field} is required")
        properties = schema.get("properties", {})
        for field, child_schema in properties.items():
            if field in value:
                errors.extend(validate_value(child_schema, value[field], f"{pointer}.{field}"))
        additional = schema.get("additionalProperties")
        if isinstance(additional, dict):
            for field, child_value in value.items():
                if field not in properties:
                    errors.extend(validate_value(additional, child_value, f"{pointer}.{field}"))
        elif additional is False:
            for field in value:
                if field not in properties:
                    errors.append(f"{pointer}.{field} is not allowed")
    return errors


def validate_schema_fixture(schema_name: str, payload: dict[str, Any]) -> list[str]:
    schema = load_json(REPO_ROOT / "schemas" / schema_name)
    return validate_value(schema, payload)


def without(payload: dict[str, Any], field: str) -> dict[str, Any]:
    cloned = copy.deepcopy(payload)
    cloned.pop(field, None)
    return cloned


def with_value(payload: dict[str, Any], field: str, value: Any) -> dict[str, Any]:
    cloned = copy.deepcopy(payload)
    cloned[field] = value
    return cloned


SHA = "a" * 64

VALID_FIXTURES: dict[str, dict[str, Any]] = {
    "echo-addon-package.schema.json": {
        "schemaVersion": "echo.addon.package.v1",
        "id": "fixture-addon",
        "version": "1.0.0",
        "publisher": {"githubOwner": "knoxhack", "githubRepo": "ECHO-Fixture"},
        "targets": ["native"],
        "dependencies": [{"id": "fixture-runtime", "kind": "runtime", "version": "1.0.0"}],
        "artifacts": {"native": "fixture-addon-1.0.0.echo-addon"},
    },
    "echo-pack.schema.json": {
        "schemaVersion": "echo.pack.v1",
        "id": "fixture-pack",
        "version": "1.0.0",
        "target": "native",
        "requiredArtifacts": [{"id": "fixture-runtime", "kind": "runtime", "version": "1.0.0"}],
    },
    "release-index-entry.schema.json": {
        "schemaVersion": "echo.release.index.entry.v1",
        "id": "fixture-addon",
        "kind": "addon",
        "version": "1.0.0",
        "channel": "alpha",
        "publisher": "knoxhack",
        "sourceRepo": "knoxhack/ECHO-Fixture",
        "releaseTag": "v1.0.0",
        "commitSha": "abc1234",
        "artifacts": {
            "native": {
                "file": "fixture-addon.echo-addon",
                "sha256": SHA,
                "url": "https://github.com/knoxhack/ECHO-Fixture/releases/download/v1.0.0/fixture-addon.echo-addon",
            }
        },
        "dependencies": [{"id": "fixture-runtime", "kind": "runtime", "version": "1.0.0"}],
        "compatibility": ["ashfall-native-edition"],
        "trust": "community",
        "validation": "approved",
    },
    "product-update-entry.schema.json": {
        "id": "echo-launcher",
        "kind": "product",
        "version": "1.0.0",
        "channel": "alpha",
        "publisher": "knoxhack",
        "sourceRepo": "knoxhack/ECHO-Launcher",
        "releaseTag": "v1.0.0",
        "commitSha": "abc1234",
        "artifacts": {
            "updater": {
                "file": "latest.yml",
                "sha256": SHA,
                "url": "https://github.com/knoxhack/ECHO-Launcher/releases/download/v1.0.0/latest.yml",
                "size": 42,
            }
        },
        "dependencies": [{"id": "echo-runtime", "kind": "runtime", "version": "1.0.0"}],
        "compatibility": ["windows-x64"],
        "trust": "official",
        "validation": "approved",
    },
    "channel.schema.json": {
        "id": "alpha",
        "name": "Alpha",
        "stability": "alpha",
    },
    "module-release-manifest.schema.json": {
        "schemaVersion": "echo.module.release.v1",
        "releaseId": "modules-fixture",
        "generatedAt": "2026-06-09T00:00:00Z",
        "sourceRepo": "https://github.com/knoxhack/ECHO-Modules",
        "provenance": {
            "sourceRepo": "knoxhack/ECHO-Modules",
            "commitSha": "abc1234",
            "workflow": ".github/workflows/release-modules.yml",
            "workflowRef": "knoxhack/ECHO-Modules/.github/workflows/release-modules.yml@refs/tags/modules-fixture",
            "runId": "123",
            "runAttempt": "1",
            "refName": "modules-fixture",
            "eventName": "workflow_dispatch",
            "generatedBy": "scripts/generate-module-release.mjs",
            "attestation": {
                "action": "actions/attest@v4",
                "subjectChecksums": "checksums.sha256",
            },
        },
        "contentGraphEvidence": {
            "kind": "content-graph-evidence",
            "filename": "content-graph-evidence.json",
            "sha256": SHA,
            "size": 420,
            "downloadUrl": "https://github.com/knoxhack/ECHO-Modules/releases/download/modules-fixture/content-graph-evidence.json",
            "runtimeTarget": "content-graph",
            "buildMode": "generated",
            "schemaVersion": "echo.content_graph.evidence.v1",
        },
        "modules": [
            {
                "moduleId": "fixture-addon",
                "version": "1.0.0",
                "descriptor": {"path": "META-INF/echo.mod.json", "sha256": SHA},
                "requires": [],
                "optional": [],
                "artifacts": [
                    {
                        "kind": "echo-addon",
                        "filename": "fixture-addon-1.0.0.echo-addon",
                        "sha256": SHA,
                        "size": 42,
                        "buildMode": "compiled-runtime",
                    },
                    {
                        "kind": "content-graph",
                        "filename": "fixture-addon-1.0.0-content-graph.json",
                        "sha256": SHA,
                        "size": 84,
                        "runtimeTarget": "content-graph",
                        "buildMode": "generated",
                    }
                ],
            }
        ],
    },
    "publisher.schema.json": {
        "id": "knoxhack",
        "name": "Knoxhack",
        "githubOwner": "knoxhack",
        "trust": "official",
    },
    "trust.schema.json": {
        "id": "community",
        "rank": 40,
        "description": "Community published fixture.",
        "playable": True,
    },
    "block.schema.json": {
        "id": "block-fixture",
        "scope": "addon",
        "target": "fixture-addon",
        "reason": "Fixture block.",
        "createdAt": "2026-06-09T00:00:00Z",
    },
    "content-graph-node.schema.json": {
        "schemaVersion": "echo.content_graph.node.v1",
        "kind": "echo:block",
        "id": "fixture:old_waystone",
        "moduleId": "fixturemodule",
        "addonId": "fixtureaddon",
        "displayName": "Old Waystone",
        "tags": ["interactable"],
        "source": {"repo": "ECHO-Modules", "path": "addons/fixturemodule/...", "format": "json"},
        "aliases": [],
        "capabilities": ["stateful", "interactable"],
        "runtimeHints": {
            "neoforge": {},
            "echo_native": {},
            "echo_runtime_standalone": {},
            "hytale": {},
        },
        "data": {"hardness": 2.5},
        "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
    },
    "content-graph-edge.schema.json": {
        "schemaVersion": "echo.content_graph.edge.v1",
        "id": "fixture:core_requires_material",
        "kind": "module_requires_module",
        "from": "echocore",
        "to": "echomaterialcore",
        "moduleId": "echocore",
        "tags": [],
        "data": {},
        "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
    },
    "content-graph.schema.json": {
        "schemaVersion": "echo.content_graph.v1",
        "id": "fixture:fixturemodule_graph",
        "generatedAt": "2026-06-09T00:00:00Z",
        "modules": ["fixturemodule"],
        "nodes": [
            {
                "schemaVersion": "echo.content_graph.node.v1",
                "kind": "echo:module",
                "id": "fixturemodule",
                "moduleId": "fixturemodule",
                "displayName": "Fixture Module",
                "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
            }
        ],
        "edges": [],
        "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
    },
    "content-graph-export-plan.schema.json": {
        "schemaVersion": "echo.content_graph.export_plan.v1",
        "target": "hytale",
        "sourceGraphId": "fixture:fixturemodule_graph",
        "plannedAt": "2026-06-09T00:00:00Z",
        "nodes": [
            {"nodeId": "fixture:old_waystone", "status": "direct", "rationale": "Stateful block maps to server state object."}
        ],
        "summary": {"direct": 1, "adapter_required": 0, "fallback": 0, "blocked": 0, "not_applicable": 0},
        "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
    },
    "content-feature-list.schema.json": {
        "schemaVersion": "echo.content_feature_list.v1",
        "moduleId": "fixturemodule",
        "generatedAt": "2026-06-09T00:00:00Z",
        "features": [
            {
                "id": "fixture:waystone_travel",
                "title": "Waystone Travel",
                "nodes": ["fixture:old_waystone"],
                "runtimes": {
                    "neoforge": "supported",
                    "echo_native": "supported",
                    "echo_runtime_standalone": "supported",
                    "hytale": "planned_with_fallback",
                },
            }
        ],
        "provenance": {"generatedBy": "fixture", "generatedAt": "2026-06-09T00:00:00Z"},
    },
    "content-graph-evidence.schema.json": {
        "schemaVersion": "echo.content_graph.evidence.v1",
        "generatedAt": "2026-06-09T00:00:00Z",
        "source": "ECHO-Modules/dist/echo-module-release",
        "graphCount": 1,
        "moduleCount": 1,
        "nodeCount": 2,
        "edgeCount": 1,
        "featureCount": 1,
        "exportPlanCount": 4,
        "unresolvedReferenceCount": 0,
        "hytaleBlockerCount": 1,
        "validationState": "warning",
        "hytaleSummary": {"direct": 1, "adapter_required": 0, "fallback": 0, "blocked": 1, "not_applicable": 0},
        "modules": [
            {
                "moduleId": "fixturemodule",
                "version": "1.0.0",
                "graphPath": ".echo/content-graph/content-graph.json",
                "schemaVersion": "echo.content_graph.v1",
                "nodeCount": 2,
                "edgeCount": 1,
                "featureCount": 1,
                "exportPlanCount": 4,
                "unresolvedReferenceCount": 0,
                "hytaleBlockerCount": 1,
                "validationState": "warning",
                "hytaleBlockers": ["fixture:old_waystone: needs runtime hint"],
                "validationIssues": [],
            }
        ],
        "diagnostics": [{"severity": "warning", "code": "HYTALE_BLOCKED", "message": "One Hytale node is blocked."}],
    },
}


INVALID_FIXTURES: dict[str, list[dict[str, Any]]] = {
    "echo-addon-package.schema.json": [
        without(VALID_FIXTURES["echo-addon-package.schema.json"], "schemaVersion"),
        with_value(VALID_FIXTURES["echo-addon-package.schema.json"], "schemaVersion", "echo.addon.package.v0"),
        with_value(VALID_FIXTURES["echo-addon-package.schema.json"], "dependencies", {}),
        with_value(
            VALID_FIXTURES["echo-addon-package.schema.json"],
            "dependencies",
            [{"id": "fixture-runtime", "kind": "unknown", "version": "1.0.0"}],
        ),
    ],
    "echo-pack.schema.json": [
        without(VALID_FIXTURES["echo-pack.schema.json"], "requiredArtifacts"),
        with_value(VALID_FIXTURES["echo-pack.schema.json"], "schemaVersion", "echo.pack.v0"),
    ],
    "release-index-entry.schema.json": [
        without(VALID_FIXTURES["release-index-entry.schema.json"], "sourceRepo"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "schemaVersion", 1),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "sourceRepo", "not-a-repo"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "commitSha", "not-a-sha"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "commitSha", "0000000"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", []),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "fixture-addon.echo-addon"}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "../fixture-addon.echo-addon", "sha256": SHA}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "fixture-addon.echo-addon", "sha256": "not-a-sha"}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "fixture-addon.echo-addon", "sha256": SHA, "url": "http://example.com/fixture-addon.echo-addon"}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "dependencies", [{"kind": "runtime"}]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "dependencies", [{"id": "fixture-runtime", "kind": "unknown"}]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "compatibility", [123]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "compatibility", ["ashfall-native-edition", "ashfall-native-edition"]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "trust", "unknown"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "validation", "unknown"),
    ],
    "product-update-entry.schema.json": [
        without(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "kind", "module"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "commitSha", "0000000"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "dependencies", [{"id": "echo-runtime", "kind": "unknown"}]),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "compatibility", [123]),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "compatibility", ["windows-x64", "windows-x64"]),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "trust", "unknown"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts", {"updater": {"file": "C:/latest.yml", "sha256": SHA}}),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts", {"updater": {"file": "latest.yml", "sha256": "not-a-sha"}}),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts", {"updater": {"file": "latest.yml", "sha256": SHA, "url": "http://example.com/latest.yml"}}),
    ],
    "channel.schema.json": [
        without(VALID_FIXTURES["channel.schema.json"], "stability"),
        with_value(VALID_FIXTURES["channel.schema.json"], "stability", "nightly"),
    ],
    "module-release-manifest.schema.json": [
        without(VALID_FIXTURES["module-release-manifest.schema.json"], "provenance"),
        without(VALID_FIXTURES["module-release-manifest.schema.json"], "contentGraphEvidence"),
        without(VALID_FIXTURES["module-release-manifest.schema.json"], "modules"),
        with_value(VALID_FIXTURES["module-release-manifest.schema.json"], "schemaVersion", 1),
        with_value(
            VALID_FIXTURES["module-release-manifest.schema.json"],
            "provenance",
            {
                "sourceRepo": "knoxhack/ECHO-Modules",
                "generatedBy": "scripts/generate-module-release.mjs",
                "attestation": {
                    "action": "actions/attest@v3",
                    "subjectChecksums": "checksums.sha256",
                },
            },
        ),
        with_value(VALID_FIXTURES["module-release-manifest.schema.json"], "modules", []),
        with_value(
            VALID_FIXTURES["module-release-manifest.schema.json"],
            "modules",
            [
                {
                    "moduleId": "fixture-addon",
                    "version": "1.0.0",
                    "descriptor": {"path": "wrong/path.json", "sha256": SHA},
                    "requires": [],
                    "optional": [],
                    "artifacts": [{"kind": "zip", "filename": "fixture.zip", "sha256": SHA, "size": 42}],
                }
            ],
        ),
    ],
    "publisher.schema.json": [
        without(VALID_FIXTURES["publisher.schema.json"], "githubOwner"),
        with_value(VALID_FIXTURES["publisher.schema.json"], "name", ""),
    ],
    "trust.schema.json": [
        with_value(VALID_FIXTURES["trust.schema.json"], "id", "unknown-tier"),
        with_value(VALID_FIXTURES["trust.schema.json"], "rank", -1),
        with_value(VALID_FIXTURES["trust.schema.json"], "playable", "yes"),
    ],
    "block.schema.json": [
        without(VALID_FIXTURES["block.schema.json"], "reason"),
        with_value(VALID_FIXTURES["block.schema.json"], "scope", "unknown"),
    ],
    "content-graph-node.schema.json": [
        without(VALID_FIXTURES["content-graph-node.schema.json"], "schemaVersion"),
        with_value(VALID_FIXTURES["content-graph-node.schema.json"], "kind", "echo:unknown_kind"),
        with_value(VALID_FIXTURES["content-graph-node.schema.json"], "id", "bad id"),
        without(VALID_FIXTURES["content-graph-node.schema.json"], "moduleId"),
        with_value(VALID_FIXTURES["content-graph-node.schema.json"], "source", {"repo": "ECHO-Modules"}),
        with_value(VALID_FIXTURES["content-graph-node.schema.json"], "neoforgeScreenClass", "com.example.FancyScreen"),
        with_value(
            VALID_FIXTURES["content-graph-node.schema.json"],
            "provenance",
            {"generatedAt": "2026-06-09T00:00:00Z"},
        ),
    ],
    "content-graph-edge.schema.json": [
        without(VALID_FIXTURES["content-graph-edge.schema.json"], "from"),
        with_value(VALID_FIXTURES["content-graph-edge.schema.json"], "kind", "echo:bad_edge"),
        with_value(VALID_FIXTURES["content-graph-edge.schema.json"], "id", "no-colon-here"),
    ],
    "content-graph.schema.json": [
        without(VALID_FIXTURES["content-graph.schema.json"], "nodes"),
        with_value(VALID_FIXTURES["content-graph.schema.json"], "schemaVersion", "echo.content_graph.v0"),
        with_value(VALID_FIXTURES["content-graph.schema.json"], "modules", []),
    ],
    "content-graph-export-plan.schema.json": [
        without(VALID_FIXTURES["content-graph-export-plan.schema.json"], "target"),
        with_value(VALID_FIXTURES["content-graph-export-plan.schema.json"], "target", "fabric"),
        with_value(
            VALID_FIXTURES["content-graph-export-plan.schema.json"],
            "nodes",
            [{"nodeId": "fixture:old_waystone", "status": "maybe"}],
        ),
    ],
    "content-feature-list.schema.json": [
        without(VALID_FIXTURES["content-feature-list.schema.json"], "features"),
        with_value(VALID_FIXTURES["content-feature-list.schema.json"], "moduleId", "BAD ID"),
        with_value(
            VALID_FIXTURES["content-feature-list.schema.json"],
            "features",
            [{"id": "fixture:empty", "title": "Empty", "nodes": [], "runtimes": {}}],
        ),
    ],
    "content-graph-evidence.schema.json": [
        without(VALID_FIXTURES["content-graph-evidence.schema.json"], "schemaVersion"),
        without(VALID_FIXTURES["content-graph-evidence.schema.json"], "hytaleBlockerCount"),
        with_value(VALID_FIXTURES["content-graph-evidence.schema.json"], "schemaVersion", "echo.content_graph.evidence.v0"),
        with_value(VALID_FIXTURES["content-graph-evidence.schema.json"], "nodeCount", -1),
        with_value(VALID_FIXTURES["content-graph-evidence.schema.json"], "validationState", "unknown"),
        with_value(
            VALID_FIXTURES["content-graph-evidence.schema.json"],
            "modules",
            [{"moduleId": "BAD ID", "nodeCount": 0, "edgeCount": 0, "featureCount": 0, "exportPlanCount": 0, "hytaleBlockerCount": 0, "validationState": "valid"}],
        ),
        with_value(
            VALID_FIXTURES["content-graph-evidence.schema.json"],
            "diagnostics",
            [{"severity": "bad", "message": "Invalid severity"}],
        ),
    ],
}


def run_tests() -> dict[str, Any]:
    failures: list[str] = []
    tested = 0
    for schema_name, fixture in VALID_FIXTURES.items():
        tested += 1
        errors = validate_schema_fixture(schema_name, fixture)
        if errors:
            failures.append(f"{schema_name} valid fixture failed: {errors}")
        generated_fixture = GENERATED_FIXTURES.get(schema_name)
        if generated_fixture is not None:
            tested += 1
            if not generated_fixture.exists():
                failures.append(f"{schema_name} generated fixture missing: {generated_fixture}")
            else:
                errors = validate_schema_fixture(schema_name, load_json(generated_fixture))
                if errors:
                    failures.append(f"{schema_name} generated fixture failed: {errors}")
        for index, invalid in enumerate(INVALID_FIXTURES[schema_name], start=1):
            tested += 1
            errors = validate_schema_fixture(schema_name, invalid)
            if not errors:
                failures.append(f"{schema_name} invalid fixture {index} unexpectedly passed")
    return {
        "status": "failed" if failures else "passed",
        "testedFixtures": tested,
        "schemaFamilies": sorted(VALID_FIXTURES),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ECHO SDK schema contract fixture tests.")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    result = run_tests()
    if args.json_output:
        print(json.dumps(result, indent=2))
    elif result["failures"]:
        print("ECHO SDK schema fixture tests failed:")
        for failure in result["failures"]:
            print(f"- {failure}")
    else:
        print(f"ECHO SDK schema fixture tests passed for {result['testedFixtures']} fixtures.")
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
