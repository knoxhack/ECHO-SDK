#!/usr/bin/env python3
"""Validate ECHO SDK contract fixtures without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ADDON_SCHEMA = "echo.addon.package.v1"
PACK_SCHEMA = "echo.pack.v1"
SHA256 = re.compile(r"^[a-f0-9]{64}$", re.IGNORECASE)
RUNTIME_CONTRACT_SCHEMA_VERSIONS = {
    "echo-native-host.schema.json": "echo.native.host.v1",
    "echo-ui-surface.schema.json": "echo.ui.surface.v1",
    "echo-input-binding.schema.json": "echo.input.binding.v1",
    "echo-inventory-surface.schema.json": "echo.inventory.surface.v1",
    "echo-gameplay-action.schema.json": "echo.gameplay.action.v1",
    "echo-save-session.schema.json": "echo.save.session.v1",
    "echo-runtime-conformance.schema.json": "echo.runtime.conformance.v1",
    "echo-player-surface-manifest.schema.json": "echo.native.player_surface_manifest.v1",
    "echo-theme-tokens.schema.json": "echo.theme.tokens.v1",
    "echo-playtest-scenario.schema.json": "echo.playtest.scenario.v1",
}
RUNTIME_CONTRACT_FIXTURES = {
    schema_name: Path("fixtures") / "unified-native" / schema_name.replace(".schema.json", ".fixture.json")
    for schema_name in RUNTIME_CONTRACT_SCHEMA_VERSIONS
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(errors: list[str], path: Path, payload: dict[str, Any], field: str) -> None:
    if payload.get(field) in (None, "", []):
        errors.append(f"{path.as_posix()} missing {field}")


def validate_addon_package(path: Path, errors: list[str]) -> None:
    payload = load_json(path)
    if not isinstance(payload, dict):
        errors.append(f"{path.as_posix()} must be an object")
        return
    for field in ["schemaVersion", "id", "version", "publisher", "targets", "artifacts"]:
        require(errors, path, payload, field)
    if not isinstance(payload.get("dependencies"), list):
        errors.append(f"{path.as_posix()} dependencies must be an array")
    if payload.get("schemaVersion") != ADDON_SCHEMA:
        errors.append(f"{path.as_posix()} schemaVersion must be {ADDON_SCHEMA}")
    if "moduleId" in payload or "schema" in payload:
        errors.append(f"{path.as_posix()} must use id/schemaVersion instead of legacy moduleId/schema")
    publisher = payload.get("publisher")
    if not isinstance(publisher, dict) or not publisher.get("githubOwner") or not publisher.get("githubRepo"):
        errors.append(f"{path.as_posix()} publisher must include githubOwner and githubRepo")
    targets = payload.get("targets")
    if not isinstance(targets, list) or not targets:
        errors.append(f"{path.as_posix()} targets must be a non-empty array")
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append(f"{path.as_posix()} artifacts must be an object")
        return
    expected_suffixes = {
        "native": ".echo-addon",
        "neoforge": "-neoforge.jar",
        "standalone": "-standalone.jar",
        "sources": "-sources.jar",
    }
    for key, suffix in expected_suffixes.items():
        value = artifacts.get(key)
        if value is not None and ("/" in value or "\\" in value or not str(value).endswith(suffix)):
            errors.append(f"{path.as_posix()} artifacts.{key} must be a filename ending with {suffix}")


def validate_pack_contract(path: Path, errors: list[str]) -> None:
    payload = load_json(path)
    if not isinstance(payload, dict):
        errors.append(f"{path.as_posix()} must be an object")
        return
    if payload.get("schemaVersion") != PACK_SCHEMA:
        errors.append(f"{path.as_posix()} schemaVersion must be {PACK_SCHEMA}")
    for field in ["id", "version", "target", "requiredArtifacts"]:
        require(errors, path, payload, field)


def validate_schema_files(root: Path, errors: list[str]) -> None:
    schemas = root / "schemas"
    if not schemas.is_dir():
        errors.append(f"Missing schemas directory: {schemas.as_posix()}")
        return
    for schema in sorted(schemas.glob("*.schema.json")):
        payload = load_json(schema)
        if not isinstance(payload, dict):
            errors.append(f"{schema.as_posix()} must be an object")
            continue
        for field in ["$schema", "$id", "title", "type"]:
            require(errors, schema, payload, field)
        expected_schema_version = RUNTIME_CONTRACT_SCHEMA_VERSIONS.get(schema.name)
        if expected_schema_version:
            actual_schema_version = payload.get("properties", {}).get("schemaVersion", {}).get("const")
            if actual_schema_version != expected_schema_version:
                errors.append(f"{schema.as_posix()} properties.schemaVersion.const must be {expected_schema_version}")


def validate_unified_native_fixtures(root: Path, errors: list[str]) -> None:
    from test_echo_contract_schemas import validate_value

    for schema_name, fixture_path in sorted(RUNTIME_CONTRACT_FIXTURES.items()):
        absolute_fixture = root / fixture_path
        absolute_schema = root / "schemas" / schema_name
        if not absolute_schema.is_file():
            errors.append(f"Missing runtime contract schema: {absolute_schema.as_posix()}")
            continue
        if not absolute_fixture.is_file():
            errors.append(f"Missing runtime contract fixture: {absolute_fixture.as_posix()}")
            continue
        schema_payload = load_json(absolute_schema)
        fixture_payload = load_json(absolute_fixture)
        for error in validate_value(schema_payload, fixture_payload):
            errors.append(f"{absolute_fixture.as_posix()} failed {schema_name}: {error}")


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    errors: list[str] = []
    validate_schema_files(root, errors)
    validate_unified_native_fixtures(root, errors)
    sample = root / "samples" / "hello-content-addon" / "src" / "main" / "resources" / "META-INF" / "echo-addon-package.json"
    if sample.is_file():
        validate_addon_package(sample, errors)
    else:
        errors.append(f"Missing sample addon package: {sample.as_posix()}")
    for pack_path in sorted((root / "templates").glob("**/echo.pack.json")):
        validate_pack_contract(pack_path, errors)
    if args.json_output:
        print(json.dumps({"status": "failed" if errors else "passed", "errors": errors}, indent=2))
    elif errors:
        print("ECHO SDK contract validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("ECHO SDK contract validation passed.")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ECHO SDK contract fixtures.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return command_validate(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
