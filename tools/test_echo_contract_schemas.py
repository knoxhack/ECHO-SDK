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
        "id": "fixture-addon",
        "kind": "addon",
        "version": "1.0.0",
        "channel": "alpha",
        "publisher": "knoxhack",
        "sourceRepo": "knoxhack/ECHO-Fixture",
        "releaseTag": "v1.0.0",
        "commitSha": "abc1234",
        "artifacts": {"native": {"file": "fixture-addon.echo-addon", "sha256": SHA}},
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
        "artifacts": {"updater": {"file": "latest.yml", "sha256": SHA, "size": 42}},
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
        "schemaVersion": 1,
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
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "sourceRepo", "not-a-repo"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "commitSha", "not-a-sha"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "commitSha", "0000000"),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", []),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "fixture-addon.echo-addon"}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "artifacts", {"native": {"file": "fixture-addon.echo-addon", "sha256": "not-a-sha"}}),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "dependencies", [{"kind": "runtime"}]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "dependencies", [{"id": "fixture-runtime", "kind": "unknown"}]),
        with_value(VALID_FIXTURES["release-index-entry.schema.json"], "validation", "unknown"),
    ],
    "product-update-entry.schema.json": [
        without(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "kind", "module"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "commitSha", "0000000"),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "dependencies", [{"id": "echo-runtime", "kind": "unknown"}]),
        with_value(VALID_FIXTURES["product-update-entry.schema.json"], "artifacts", {"updater": {"file": "latest.yml", "sha256": "not-a-sha"}}),
    ],
    "channel.schema.json": [
        without(VALID_FIXTURES["channel.schema.json"], "stability"),
        with_value(VALID_FIXTURES["channel.schema.json"], "stability", "nightly"),
    ],
    "module-release-manifest.schema.json": [
        without(VALID_FIXTURES["module-release-manifest.schema.json"], "provenance"),
        without(VALID_FIXTURES["module-release-manifest.schema.json"], "modules"),
        with_value(VALID_FIXTURES["module-release-manifest.schema.json"], "schemaVersion", 2),
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
}


def run_tests() -> dict[str, Any]:
    failures: list[str] = []
    tested = 0
    for schema_name, fixture in VALID_FIXTURES.items():
        tested += 1
        errors = validate_schema_fixture(schema_name, fixture)
        if errors:
            failures.append(f"{schema_name} valid fixture failed: {errors}")
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
