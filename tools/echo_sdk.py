#!/usr/bin/env python3
"""Local-only ECHO SDK template renderer and validator."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_TEMPLATE_IDS = [
    "echo-addon-platform-contract",
    "echo-addon-content",
    "echo-addon-ui-surface",
    "echo-addon-pack-root",
    "echo-addon-ai-tool",
    "echo-addon-bridge-tool",
    "echo-schema",
    "echo-pack-profile",
    "echo-metadata",
    "echo-report",
]

REQUIRED_MANIFEST_FIELDS = [
    "schema",
    "id",
    "name",
    "kind",
    "description",
    "tokens",
    "requiredFiles",
    "defaultFeatures",
    "safeEditZones",
    "protectedFiles",
    "recommendedAgentLanes",
    "validationCommands",
]

REQUIRED_TOKEN_NAMES = {
    "module_id",
    "package_path",
    "class_name",
    "role",
    "kind",
    "feature_id",
}

MODULE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
TOKEN_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
AGENT_LANES = {
    "architect_agent",
    "loader_agent",
    "runtime_agent",
    "ui_agent",
    "asset_agent",
    "mission_agent",
    "world_agent",
    "packaging_agent",
    "diagnostics_agent",
    "test_agent",
    "release_agent",
}


@dataclass(frozen=True)
class RenderedFile:
    source: Path
    target: Path


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, text: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise ValueError(f"Refusing to overwrite existing file without --force: {path}")
    path.write_text(text, encoding="utf-8")


def safe_relative_path(path: str) -> bool:
    candidate = Path(path)
    return not candidate.is_absolute() and ".." not in candidate.parts


def template_root(root: Path) -> Path:
    return root / "templates"


def template_manifest(root: Path, template_id: str) -> dict[str, Any]:
    path = template_root(root) / template_id / "template.json"
    if not path.is_file():
        raise ValueError(f"Template manifest not found: {path.as_posix()}")
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Template manifest must be a JSON object: {path.as_posix()}")
    return payload


def class_name_from_module(module_id: str) -> str:
    parts = [part for part in re.split(r"[_\W]+", module_id) if part]
    return "".join(part[:1].upper() + part[1:] for part in parts) or "EchoGeneratedModule"


def display_name_from_module(module_id: str) -> str:
    parts = [part for part in module_id.replace("_", " ").split() if part]
    if module_id.startswith("echo") and len(module_id) > 4:
        parts = ["ECHO"] + [module_id[4:].replace("_", " ")]
    return " ".join(part[:1].upper() + part[1:] for part in parts) or module_id


def pack_dir_from_id(pack_id: str) -> str:
    return pack_id.replace("_", "-")


def build_tokens(manifest: dict[str, Any], args: argparse.Namespace, command_kind: str) -> dict[str, str]:
    default_values = manifest.get("defaultValues") if isinstance(manifest.get("defaultValues"), dict) else {}
    module_id = getattr(args, "module_id", None) or getattr(args, "pack_id", None) or default_values.get("module_id") or manifest["id"].replace("-", "_")
    module_id = str(module_id).strip().lower().replace("-", "_")
    if not MODULE_ID_PATTERN.match(module_id):
        raise ValueError(f"Invalid module or pack id '{module_id}'. Use lowercase letters, numbers, and underscores.")
    class_name = getattr(args, "class_name", None) or default_values.get("class_name") or class_name_from_module(module_id)
    role = getattr(args, "role", None) or default_values.get("role") or "module"
    kind = getattr(args, "kind_value", None) or default_values.get("kind") or manifest.get("kind", "addon")
    feature_id = getattr(args, "feature_id", None) or default_values.get("feature_id") or f"{module_id}.feature"
    pack_id = getattr(args, "pack_id", None) or module_id
    pack_id = str(pack_id).strip().lower().replace("-", "_")
    package_name = default_values.get("package_name") or f"com.knoxhack.echo.sdk.{module_id}"
    package_path = str(package_name).replace(".", "/")
    display_name = getattr(args, "display_name", None) or default_values.get("display_name") or display_name_from_module(module_id)
    mod_name = default_values.get("mod_name") or display_name
    return {
        "module_id": module_id,
        "pack_id": pack_id,
        "pack_dir": pack_dir_from_id(pack_id),
        "package_name": str(package_name),
        "package_path": package_path,
        "class_name": str(class_name),
        "role": str(role),
        "kind": str(kind),
        "feature_id": str(feature_id),
        "display_name": str(display_name),
        "mod_name": str(mod_name),
        "template_id": str(manifest["id"]),
        "template_name": str(manifest["name"]),
        "command_kind": command_kind,
    }


def render_tokens(text: str, tokens: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in tokens:
            raise ValueError(f"Unknown template token: {key}")
        return tokens[key]

    return TOKEN_PATTERN.sub(replace, text)


def source_roots(root: Path, manifest: dict[str, Any]) -> list[Path]:
    roots: list[Path] = []
    for file_set in manifest.get("fileSets", []):
        if not isinstance(file_set, str) or not safe_relative_path(file_set):
            raise ValueError(f"Invalid file set in {manifest['id']}: {file_set}")
        roots.append(template_root(root) / "_shared" / file_set)
    local_files = template_root(root) / manifest["id"] / "files"
    if local_files.is_dir():
        roots.append(local_files)
    if not roots:
        raise ValueError(f"Template {manifest['id']} does not declare file sets or local files.")
    return roots


def rendered_target(source_root: Path, source: Path, output_root: Path, tokens: dict[str, str]) -> Path:
    relative = source.relative_to(source_root).as_posix()
    if relative.endswith(".tpl"):
        relative = relative[:-4]
    relative = render_tokens(relative, tokens)
    if not safe_relative_path(relative):
        raise ValueError(f"Template rendered an unsafe path: {relative}")
    return output_root / relative


def render_template(root: Path, template_id: str, output_root: Path, args: argparse.Namespace, command_kind: str, force: bool = False, dry_run: bool = False) -> list[RenderedFile]:
    manifest = template_manifest(root, template_id)
    tokens = build_tokens(manifest, args, command_kind)
    rendered: list[RenderedFile] = []
    for source_root in source_roots(root, manifest):
        if not source_root.is_dir():
            raise ValueError(f"Template source root is missing: {source_root.as_posix()}")
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            target = rendered_target(source_root, source, output_root, tokens)
            rendered.append(RenderedFile(source=source, target=target))
            if dry_run:
                continue
            content = source.read_text(encoding="utf-8")
            write_text(target, render_tokens(content, tokens), force=force)
    return rendered


def validate_manifest(root: Path, template_id: str) -> list[str]:
    errors: list[str] = []
    try:
        manifest = template_manifest(root, template_id)
    except Exception as exc:  # noqa: BLE001 - validation reports every template error.
        return [str(exc)]
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest:
            errors.append(f"{template_id}: missing manifest field {field}")
    if manifest.get("schema") != "echo.sdk.template.v1":
        errors.append(f"{template_id}: schema must be echo.sdk.template.v1")
    if manifest.get("id") != template_id:
        errors.append(f"{template_id}: manifest id must match folder name")
    tokens = manifest.get("tokens")
    if not isinstance(tokens, dict):
        errors.append(f"{template_id}: tokens must be an object")
    else:
        missing_tokens = sorted(REQUIRED_TOKEN_NAMES - set(tokens))
        for token in missing_tokens:
            errors.append(f"{template_id}: missing required token {token}")
    for list_field in ("requiredFiles", "defaultFeatures", "safeEditZones", "protectedFiles", "recommendedAgentLanes", "validationCommands"):
        if list_field in manifest and not isinstance(manifest[list_field], list):
            errors.append(f"{template_id}: {list_field} must be an array")
    for lane in manifest.get("recommendedAgentLanes", []):
        if lane not in AGENT_LANES:
            errors.append(f"{template_id}: unknown recommended agent lane {lane}")
    for required_file in manifest.get("requiredFiles", []):
        if not isinstance(required_file, str) or not safe_relative_path(required_file):
            errors.append(f"{template_id}: unsafe required file path {required_file}")
    try:
        roots = source_roots(root, manifest)
        for source_root in roots:
            if not source_root.is_dir():
                errors.append(f"{template_id}: missing file set {source_root.as_posix()}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{template_id}: {exc}")
    readme = template_root(root) / template_id / "README.md"
    if not readme.is_file():
        errors.append(f"{template_id}: missing README.md")
    return errors


def validate_templates(root: Path) -> dict[str, Any]:
    template_dir = template_root(root)
    errors: list[str] = []
    if not template_dir.is_dir():
        return {
            "status": "failed",
            "templateCount": 0,
            "validatedTemplates": [],
            "errors": [f"Missing templates directory: {template_dir.as_posix()}"],
        }
    observed = sorted(path.name for path in template_dir.iterdir() if path.is_dir() and not path.name.startswith("_"))
    for required in REQUIRED_TEMPLATE_IDS:
        if required not in observed:
            errors.append(f"Missing required template folder: {required}")
    for template_id in observed:
        errors.extend(validate_manifest(root, template_id))
    return {
        "status": "passed" if not errors else "failed",
        "templateCount": len(observed),
        "validatedTemplates": observed,
        "requiredTemplates": REQUIRED_TEMPLATE_IDS,
        "errors": errors,
    }


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    payload = validate_templates(root)
    if args.json_output:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
    elif payload["errors"]:
        print("ECHO SDK template validation failed:")
        for error in payload["errors"]:
            print(f"- {error}")
    else:
        print(f"ECHO SDK template validation passed for {payload['templateCount']} templates.")
    return 0 if not payload["errors"] else 1


def command_create_addon(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    output_root = Path(args.output_root).resolve()
    rendered = render_template(root, args.template_id, output_root, args, "addon", force=args.force, dry_run=args.dry_run)
    payload = {
        "status": "dry_run" if args.dry_run else "created",
        "template": args.template_id,
        "moduleId": args.module_id,
        "outputRoot": str(output_root),
        "fileCount": len(rendered),
        "files": [str(item.target.relative_to(output_root)).replace("\\", "/") for item in rendered],
        "settingsGradleModified": False,
        "localOnly": True,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True) if args.json_output else f"Rendered {len(rendered)} files for {args.module_id} under {output_root}.")
    return 0


def command_create_pack(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    output_root = Path(args.output_root).resolve()
    rendered = render_template(root, args.template_id, output_root, args, "pack", force=args.force, dry_run=args.dry_run)
    payload = {
        "status": "dry_run" if args.dry_run else "created",
        "template": args.template_id,
        "packId": args.pack_id,
        "outputRoot": str(output_root),
        "fileCount": len(rendered),
        "files": [str(item.target.relative_to(output_root)).replace("\\", "/") for item in rendered],
        "settingsGradleModified": False,
        "localOnly": True,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True) if args.json_output else f"Rendered {len(rendered)} files for {args.pack_id} under {output_root}.")
    return 0


def relative_or_local(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def registration_plan(root: Path, module_id: str, output_root: Path) -> dict[str, Any]:
    normalized_id = str(module_id).strip().lower().replace("-", "_")
    if not MODULE_ID_PATTERN.match(normalized_id):
        raise ValueError(f"Invalid module id '{module_id}'. Use lowercase letters, numbers, and underscores.")
    target_addon_path = output_root.resolve() / "addons" / normalized_id
    target_addon_relative = relative_or_local(root, target_addon_path)
    settings_lines = [
        f"include '{normalized_id}'",
        f"project(':{normalized_id}').projectDir = file('{target_addon_relative}')",
    ]
    return {
        "schema": "echo.sdk.registration_plan.v1",
        "status": "planned",
        "action": "register_addon_dry_run",
        "moduleId": normalized_id,
        "outputRoot": relative_or_local(root, output_root),
        "targetAddonPath": target_addon_relative,
        "proposedSettingsGradleLines": settings_lines,
        "requiredValidationCommands": [
            f".\\gradlew :{normalized_id}:compileJava -PechoAddonSet=beta",
            ".\\gradlew scanEchoWorkspace -PechoAddonSet=beta",
            ".\\gradlew generateEchoModuleGraph -PechoAddonSet=beta",
            ".\\gradlew build -PechoAddonSet=beta",
        ],
        "safetyNotes": [
            "Dry-run only; real settings.gradle is not modified.",
            "Review generated metadata before manually registering the addon.",
            "Do not register build/ fixtures into release packs.",
            "Regenerate PackOS reports and lockfiles only after human review.",
        ],
        "mutatesSettingsGradle": False,
        "writesFiles": False,
        "localOnly": True,
    }


def command_plan_register_addon(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    output_root = Path(args.output_root).resolve()
    payload = registration_plan(root, args.module_id, output_root)
    if args.json_output:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
    else:
        print(f"Registration dry-run for {payload['moduleId']}:")
        for line in payload["proposedSettingsGradleLines"]:
            print(line)
    return 0


def clean_output_root(root: Path, output_root: Path) -> None:
    resolved_root = root.resolve()
    resolved_output = output_root.resolve()
    try:
        resolved_output.relative_to(resolved_root / "build")
    except ValueError as exc:
        raise ValueError(f"Refusing to clean output outside build/: {resolved_output}") from exc
    if resolved_output.exists():
        shutil.rmtree(resolved_output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render and validate local ECHO SDK templates.")
    parser.add_argument("--root", default=".", help="Repository root.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate SDK inputs.")
    validate_sub = validate.add_subparsers(dest="validate_target", required=True)
    validate_templates_parser = validate_sub.add_parser("templates", help="Validate templates.")
    validate_templates_parser.add_argument("--root", default=argparse.SUPPRESS, help="Repository root.")
    validate_templates_parser.add_argument("--json", action="store_true", dest="json_output")
    validate_templates_parser.set_defaults(func=command_validate)

    create = subparsers.add_parser("create", help="Create local SDK output.")
    create_sub = create.add_subparsers(dest="create_target", required=True)

    addon = create_sub.add_parser("addon", help="Render an addon template under the requested output root.")
    addon.add_argument("--template", default="echo-addon-content", dest="template_id")
    addon.add_argument("--root", default=argparse.SUPPRESS, help="Repository root.")
    addon.add_argument("--id", required=True, dest="module_id")
    addon.add_argument("--role", required=True)
    addon.add_argument("--kind", default=None, dest="kind_value")
    addon.add_argument("--feature-id", default=None)
    addon.add_argument("--class-name", default=None)
    addon.add_argument("--display-name", default=None)
    addon.add_argument("--output-root", required=True)
    addon.add_argument("--force", action="store_true")
    addon.add_argument("--dry-run", action="store_true")
    addon.add_argument("--json", action="store_true", dest="json_output")
    addon.set_defaults(func=command_create_addon)

    pack = create_sub.add_parser("pack", help="Render a pack profile template under the requested output root.")
    pack.add_argument("--template", default="echo-pack-profile", dest="template_id")
    pack.add_argument("--root", default=argparse.SUPPRESS, help="Repository root.")
    pack.add_argument("--id", required=True, dest="pack_id")
    pack.add_argument("--role", default="pack_root")
    pack.add_argument("--kind", default="official_pack", dest="kind_value")
    pack.add_argument("--feature-id", default=None)
    pack.add_argument("--class-name", default=None)
    pack.add_argument("--display-name", default=None)
    pack.add_argument("--output-root", required=True)
    pack.add_argument("--force", action="store_true")
    pack.add_argument("--dry-run", action="store_true")
    pack.add_argument("--json", action="store_true", dest="json_output")
    pack.set_defaults(func=command_create_pack)

    plan = subparsers.add_parser("plan", help="Produce local-only SDK plans without mutating files.")
    plan_sub = plan.add_subparsers(dest="plan_target", required=True)
    register = plan_sub.add_parser("register", help="Plan a workspace registration.")
    register_sub = register.add_subparsers(dest="register_target", required=True)
    register_addon = register_sub.add_parser("addon", help="Plan settings.gradle registration for a generated addon.")
    register_addon.add_argument("--root", default=argparse.SUPPRESS, help="Repository root.")
    register_addon.add_argument("--id", required=True, dest="module_id")
    register_addon.add_argument("--output-root", required=True)
    register_addon.add_argument("--json", action="store_true", dest="json_output")
    register_addon.set_defaults(func=command_plan_register_addon)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001 - CLI should produce a concise failure.
        print(f"ECHO SDK error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
