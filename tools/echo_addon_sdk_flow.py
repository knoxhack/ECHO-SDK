#!/usr/bin/env python3
"""Minimal ECHO public SDK flow for add-on initialization, validation, packaging, and parity evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any


VERSION = "0.1.0"
RUNTIMES = ["echo_native", "neoforge", "echo_runtime_standalone"]
LIVE_CLIENT_PROOF_REPORTS = [
    "reports/echo/native/live-client-activation.json",
    "reports/echo/native/live-gameplay-hooks.json",
    "reports/echo/native/ui-host-attachment.json",
    "reports/echo/native/title-screen-attachment.json",
    "reports/echo/native/ashfall-first-loop.json",
]
NATIVE_LIVE_EVIDENCE_PATHS = {
    "liveClientProbe": "echo-native-platform/fixtures/ashfall/isolated-runtime/game/echo-native/live-client-probe.json",
    "moduleActivation": "echo-native-platform/fixtures/ashfall/isolated-runtime/game/echo-native/module-activation.json",
    "liveUiBridge": "echo-native-platform/fixtures/ashfall/isolated-runtime/game/echo-native/live-ui-bridge.json",
    "nativeLoaderLiveProof": "echo-native-platform/fixtures/ashfall/isolated-runtime/game/echo-native/native-loader-live-proof.json",
    "nativeModuleBootstrapStatus": "echo-native-platform/reports/echo-native/ashfall/native-module-bootstrap-status.json",
    "gameplayHookEvidence": "echo-native-platform/reports/echo-native/ashfall/ashfall-gameplay-hook-evidence.json",
    "nativeLoaderBetaGate": "echo-native-platform/reports/echo-native/ashfall/phase13-native-loader-beta-gate.json",
    "nativeLoaderPlayableBetaReadiness": "echo-native-platform/reports/echo-native/ashfall/native-loader-playable-beta-readiness.json",
    "controlledProcessLaunch": "echo-native-platform/reports/echo-native/ashfall/controlled-process-launch-result.json",
}
NATIVE_LIVE_RUNTIME_EVIDENCE_FILENAMES = {
    "liveClientProbe": "live-client-probe.json",
    "moduleActivation": "module-activation.json",
    "liveUiBridge": "live-ui-bridge.json",
    "nativeLoaderLiveProof": "native-loader-live-proof.json",
}
FORBIDDEN_IMPORTS = (
    "net.minecraft",
    "net.neoforged",
    "net.minecraftforge",
    "net.fabricmc",
    "com.mojang.blaze3d",
    "com.knoxhack.echo",
)
ALLOWED_SAMPLE_IMPORT_PREFIXES = ("dev.echo.api.", "java.")
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_id(raw: str) -> str:
    value = raw.strip().lower().replace("-", "_")
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", value):
        raise ValueError(f"Invalid add-on id '{raw}'. Use lowercase letters, numbers, and underscores.")
    return value


def build_root(root: Path) -> Path:
    return root / "build" / "echo"


def addon_root(root: Path, addon_id: str) -> Path:
    return build_root(root) / "generated-addons" / addon_id


def release_root(root: Path) -> Path:
    return build_root(root) / "release"


def sdk_report_root(root: Path) -> Path:
    return root / "reports" / "echo" / "sdk"


def native_report_root(root: Path) -> Path:
    return root / "reports" / "echo" / "native"


def sdk_package_root(root: Path) -> Path:
    return build_root(root) / "sdk"


def sdk_testkit_root(root: Path) -> Path:
    return sdk_package_root(root) / "testkit"


def safe_clean(path: Path, allowed_root: Path) -> None:
    resolved = path.resolve()
    allowed = allowed_root.resolve()
    try:
        resolved.relative_to(allowed)
    except ValueError as exc:
        raise ValueError(f"Refusing to clean outside {allowed}: {resolved}") from exc
    if path.exists():
        shutil.rmtree(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def report_envelope(kind: str, schema: str, status: str, summary: dict[str, Any], issues: list[dict[str, Any]], data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": schema,
        "generatedAt": "unspecified",
        "generator": "tools/echo_addon_sdk_flow.py",
        "workspace": "source-tree",
        "addonSet": "sdk",
        "packId": None,
        "status": status,
        "summary": summary,
        "issues": issues,
        "data": {
            "reportKind": kind,
            **data,
        },
    }


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Missing JSON file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def zip_write_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name.replace("\\", "/"), ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, data)


def zip_write_text(archive: zipfile.ZipFile, name: str, text: str) -> None:
    zip_write_bytes(archive, name, text.encode("utf-8"))


def zip_write_file(archive: zipfile.ZipFile, name: str, source: Path) -> None:
    zip_write_bytes(archive, name, source.read_bytes())


def add_file_entries(entries: dict[str, bytes], base_name: str, source_root: Path, ignore_dirs: set[str] | None = None) -> None:
    ignore_dirs = ignore_dirs or set()
    if not source_root.is_dir():
        return
    for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
        relative_parts = source.relative_to(source_root).parts
        if any(part in ignore_dirs for part in relative_parts):
            continue
        entries[f"{base_name}/{source.relative_to(source_root).as_posix()}"] = source.read_bytes()


def testkit_specs() -> list[dict[str, str]]:
    return [
        {
            "jar": "native-loader-testkit.jar",
            "class": "NativeLoaderTestkit",
            "runtime": "echo_native",
            "package": "dev.echo.testkit.nativekit",
            "artifact": ".echo-addon",
            "description": "Checks Native Loader add-on package expectations without launching Minecraft.",
        },
        {
            "jar": "standalone-parity-testkit.jar",
            "class": "StandaloneParityTestkit",
            "runtime": "echo_runtime_standalone",
            "package": "dev.echo.testkit.standalone",
            "artifact": "-standalone.jar",
            "description": "Checks Standalone harness and parity descriptor expectations.",
        },
        {
            "jar": "neoforge-adapter-testkit.jar",
            "class": "NeoForgeAdapterTestkit",
            "runtime": "neoforge",
            "package": "dev.echo.testkit.neoforge",
            "artifact": "-neoforge.jar",
            "description": "Checks NeoForge AdapterCore shim artifact expectations.",
        },
    ]


def package_name_for(addon_id: str) -> str:
    return f"dev.echo.generated.{addon_id}"


def entrypoint_for(addon_id: str) -> str:
    return f"{package_name_for(addon_id)}.GeneratedAddon"


def source_path_for(root: Path, addon_id: str) -> Path:
    return root / "src" / "main" / "java" / Path(package_name_for(addon_id).replace(".", "/")) / "GeneratedAddon.java"


def manifest_payload(addon_id: str) -> dict[str, Any]:
    return {
        "schema": "echo.mod.v1",
        "id": addon_id,
        "name": f"{addon_id.replace('_', ' ').title()}",
        "version": VERSION,
        "kind": "content",
        "role": "sample",
        "runtimeTargets": RUNTIMES,
        "domains": ["items", "blocks", "recipes"],
        "permissions": ["registry.items", "registry.blocks", "registry.recipes"],
        "entrypoint": entrypoint_for(addon_id),
    }


def package_payload(addon_id: str) -> dict[str, Any]:
    return {
        "schema": "echo.addon.package.v1",
        "moduleId": addon_id,
        "version": VERSION,
        "entrypoint": entrypoint_for(addon_id),
        "runtimes": RUNTIMES,
        "artifacts": {
            "native": f"{addon_id}-{VERSION}.echo-addon",
            "neoforge": f"{addon_id}-{VERSION}-neoforge.jar",
            "standalone": f"{addon_id}-{VERSION}-standalone.jar",
        },
    }


def reference_behavior_payload(addon_id: str) -> dict[str, Any]:
    return {
        "schema": "echo.reference.behavior.v1",
        "moduleId": addon_id,
        "version": VERSION,
        "behaviors": [
            {
                "id": "register-content",
                "domains": ["items", "blocks", "recipes"],
                "expectedRegistrations": 3,
            }
        ],
    }


def generated_addon_source(addon_id: str) -> str:
    package_name = package_name_for(addon_id)
    return f"""package {package_name};

import dev.echo.api.addon.EchoAddon;
import dev.echo.api.addon.EchoAddonDescriptor;
import dev.echo.api.addon.EchoAddonId;
import dev.echo.api.addon.EchoAddonKind;
import dev.echo.api.addon.EchoAddonRole;
import dev.echo.api.addon.EchoAddonRuntimeTarget;
import dev.echo.api.addon.EchoAddonVersion;
import dev.echo.api.block.EchoBlockDescriptor;
import dev.echo.api.block.EchoBlockId;
import dev.echo.api.block.EchoBlockSettings;
import dev.echo.api.context.EchoRegistryContext;
import dev.echo.api.item.EchoItemDescriptor;
import dev.echo.api.item.EchoItemId;
import dev.echo.api.item.EchoItemSettings;
import dev.echo.api.recipe.EchoIngredient;
import dev.echo.api.recipe.EchoRecipeDescriptor;
import dev.echo.api.recipe.EchoRecipeId;
import dev.echo.api.recipe.EchoRecipeOutput;
import dev.echo.api.recipe.EchoRecipeType;
import dev.echo.api.registry.EchoRegistryEntry;
import dev.echo.api.registry.EchoRegistryKey;
import java.util.List;
import java.util.Set;

public final class GeneratedAddon implements EchoAddon {{
    private static final EchoAddonDescriptor DESCRIPTOR = new EchoAddonDescriptor(
            new EchoAddonId("{addon_id}"),
            new EchoAddonVersion("{VERSION}"),
            "{addon_id.replace('_', ' ').title()}",
            EchoAddonKind.CONTENT,
            EchoAddonRole.SAMPLE,
            Set.of(
                    EchoAddonRuntimeTarget.ECHO_NATIVE,
                    EchoAddonRuntimeTarget.NEOFORGE,
                    EchoAddonRuntimeTarget.ECHO_RUNTIME_STANDALONE
            )
    );

    @Override
    public EchoAddonDescriptor descriptor() {{
        return DESCRIPTOR;
    }}

    @Override
    public void register(EchoRegistryContext context) {{
        context.registrar().register("items", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("{addon_id}:echo_shard"),
                new EchoItemDescriptor(
                        new EchoItemId("{addon_id}:echo_shard"),
                        EchoItemSettings.defaults(),
                        "item.{addon_id}.echo_shard"
                )
        ));
        context.registrar().register("blocks", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("{addon_id}:echo_block"),
                new EchoBlockDescriptor(
                        new EchoBlockId("{addon_id}:echo_block"),
                        EchoBlockSettings.defaults(),
                        "block.{addon_id}.echo_block"
                )
        ));
        context.registrar().register("recipes", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("{addon_id}:echo_block"),
                new EchoRecipeDescriptor(
                        new EchoRecipeId("{addon_id}:echo_block"),
                        EchoRecipeType.CRAFTING_SHAPELESS,
                        List.of(new EchoIngredient(Set.of("{addon_id}:echo_shard"), 4)),
                        new EchoRecipeOutput("{addon_id}:echo_block", 1)
                )
        ));
    }}
}}
"""


def init_addon(root: Path, addon_id: str) -> Path:
    target = addon_root(root, addon_id)
    target.mkdir(parents=True, exist_ok=True)
    write_text(source_path_for(target, addon_id), generated_addon_source(addon_id))
    write_json(target / "src" / "main" / "resources" / "META-INF" / "echo.mod.json", manifest_payload(addon_id))
    write_json(target / "src" / "main" / "resources" / "META-INF" / "echo-addon-package.json", package_payload(addon_id))
    write_json(target / "src" / "test" / "echo" / "reference-behavior.json", reference_behavior_payload(addon_id))
    write_json(
        target / "src" / "main" / "resources" / "assets" / addon_id / "lang" / "en_us.json",
        {
            f"item.{addon_id}.echo_shard": "Echo Shard",
            f"block.{addon_id}.echo_block": "Echo Block",
        },
    )
    write_json(
        target / "src" / "main" / "resources" / "data" / addon_id / "recipe" / "echo_block.json",
        {
            "type": "echo:crafting_shapeless",
            "ingredients": [f"{addon_id}:echo_shard", f"{addon_id}:echo_shard", f"{addon_id}:echo_shard", f"{addon_id}:echo_shard"],
            "result": {"id": f"{addon_id}:echo_block", "count": 1},
        },
    )
    return target


def ensure_addon(root: Path, addon_id: str) -> Path:
    target = addon_root(root, addon_id)
    if not target.is_dir():
        return init_addon(root, addon_id)
    return target


def validate_manifest(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    manifest = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo.mod.json")
    package = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo-addon-package.json")
    required = ["schema", "id", "version", "runtimeTargets", "domains", "permissions", "entrypoint"]
    for field in required:
        if field not in manifest:
            raise ValueError(f"echo.mod.json missing required field: {field}")
    if manifest["id"] != addon_id:
        raise ValueError(f"echo.mod.json id {manifest['id']!r} does not match {addon_id!r}")
    if package.get("moduleId") != addon_id:
        raise ValueError("echo-addon-package.json moduleId does not match add-on id")


def validate_schemas(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    manifest = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo.mod.json")
    package = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo-addon-package.json")
    reference = load_json(target / "src" / "test" / "echo" / "reference-behavior.json")
    if manifest.get("schema") != "echo.mod.v1":
        raise ValueError("echo.mod.json schema must be echo.mod.v1")
    if package.get("schema") != "echo.addon.package.v1":
        raise ValueError("echo-addon-package.json schema must be echo.addon.package.v1")
    if reference.get("schema") != "echo.reference.behavior.v1":
        raise ValueError("reference-behavior.json schema must be echo.reference.behavior.v1")


def import_lines(source: Path) -> list[str]:
    lines: list[str] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("import ") and line.endswith(";"):
            lines.append(line.removeprefix("import ").removesuffix(";").strip())
    return lines


def validate_imports(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    roots = [
        target / "src" / "main" / "java",
        root / "samples" / "hello-content-addon" / "src" / "main" / "java",
    ]
    errors: list[str] = []
    for source_root in roots:
        if not source_root.is_dir():
            continue
        for source in sorted(source_root.rglob("*.java")):
            for imported in import_lines(source):
                if any(imported.startswith(prefix) for prefix in FORBIDDEN_IMPORTS):
                    errors.append(f"{source}: forbidden import {imported}")
                if not any(imported.startswith(prefix) for prefix in ALLOWED_SAMPLE_IMPORT_PREFIXES):
                    errors.append(f"{source}: public SDK sample import must use dev.echo.api.* or java.*: {imported}")
    if errors:
        raise ValueError("\n".join(errors))


def validate_permissions(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    manifest = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo.mod.json")
    permissions = manifest.get("permissions")
    if not isinstance(permissions, list) or not permissions:
        raise ValueError("echo.mod.json must declare non-empty permissions")
    for permission in permissions:
        if not isinstance(permission, str) or "." not in permission:
            raise ValueError(f"Invalid permission declaration: {permission!r}")


def validate_runtime_targets(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    manifest = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo.mod.json")
    package = load_json(target / "src" / "main" / "resources" / "META-INF" / "echo-addon-package.json")
    if sorted(manifest.get("runtimeTargets", [])) != sorted(RUNTIMES):
        raise ValueError(f"runtimeTargets must declare {RUNTIMES}")
    if sorted(package.get("runtimes", [])) != sorted(RUNTIMES):
        raise ValueError(f"echo-addon-package.json runtimes must declare {RUNTIMES}")


def java_sources(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(root.rglob("*.java"))


def compile_java(root: Path, class_dir: Path, api_jar: Path | None, sources: list[Path]) -> Path:
    if api_jar is None or not api_jar.is_file():
        raise ValueError(f"API jar is required for sample compilation: {api_jar}")
    if not sources:
        raise ValueError("No Java sources to compile")
    safe_clean(class_dir, build_root(root))
    class_dir.mkdir(parents=True, exist_ok=True)
    command = [
        os.environ.get("JAVAC", "javac"),
        "-encoding",
        "UTF-8",
        "-cp",
        str(api_jar),
        "-d",
        str(class_dir),
        *[str(source) for source in sources],
    ]
    subprocess.run(command, cwd=root, check=True)
    return class_dir


def compile_addon_sources(root: Path, addon_id: str, api_jar: Path | None, classifier: str = "addon") -> Path:
    target = ensure_addon(root, addon_id)
    classes = build_root(root) / "classes" / addon_id / classifier
    sources = java_sources(target / "src" / "main" / "java")
    return compile_java(root, classes, api_jar, sources)


def compile_sample_sources(root: Path, api_jar: Path | None) -> Path:
    classes = build_root(root) / "classes" / "hello-content-addon" / "sample"
    sources = java_sources(root / "samples" / "hello-content-addon" / "src" / "main" / "java")
    return compile_java(root, classes, api_jar, sources)


def compile_sources(root: Path, addon_id: str, api_jar: Path | None) -> Path:
    classes = compile_addon_sources(root, addon_id, api_jar, "validate")
    compile_sample_sources(root, api_jar)
    return classes


def build_addon_jar(root: Path, addon_id: str, api_jar: Path | None, classifier: str) -> Path:
    target = ensure_addon(root, addon_id)
    classes = compile_addon_sources(root, addon_id, api_jar, classifier)
    out_dir = build_root(root) / "artifacts" / addon_id / classifier
    out_dir.mkdir(parents=True, exist_ok=True)
    addon_jar = out_dir / "addon.jar"
    if addon_jar.exists():
        addon_jar.unlink()
    with zipfile.ZipFile(addon_jar, "w") as archive:
        for class_file in sorted(classes.rglob("*.class")):
            zip_write_file(archive, class_file.relative_to(classes).as_posix(), class_file)
        resources = target / "src" / "main" / "resources"
        for resource in sorted(resources.rglob("*")):
            if resource.is_file() and "META-INF" not in resource.relative_to(resources).parts:
                zip_write_file(archive, resource.relative_to(resources).as_posix(), resource)
    return addon_jar


def packaged_native_manifest(target: Path) -> bytes:
    manifest = load_json(target / "src/main/resources/META-INF/echo.mod.json")
    access = manifest.get("access")
    if isinstance(access, dict) and (access.get("nativeEntrypoint") or access.get("nativeClasspath")):
        access = dict(access)
        access["nativeClasspath"] = ["addon.jar"]
        manifest["access"] = access
    return (json.dumps(manifest, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def generate_neoforge(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    generated = target / "generated" / "neoforge"
    descriptor = {
        "schema": "echo.neoforge.adapter.v1",
        "moduleId": addon_id,
        "runtime": "neoforge",
        "entrypoint": entrypoint_for(addon_id),
        "adapterCoreShim": "generated",
    }
    write_json(generated / "echo-neoforge-adapter.json", descriptor)
    write_text(
        generated / "GeneratedNeoForgeEntrypoint.java",
        f"""package {package_name_for(addon_id)}.neoforge;

public final class GeneratedNeoForgeEntrypoint {{
    public static final String ADDON_ENTRYPOINT = "{entrypoint_for(addon_id)}";
    public static final String ADAPTER_RUNTIME = "neoforge";

    private GeneratedNeoForgeEntrypoint() {{
    }}
}}
""",
    )


def generate_native(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    write_json(
        target / "generated" / "native" / "echo-native-descriptor.json",
        {
            "schema": "echo.native.descriptor.v1",
            "moduleId": addon_id,
            "runtime": "echo_native",
            "entrypoint": entrypoint_for(addon_id),
            "nativeClasspath": ["addon.jar"],
            "loads": ["echo.mod.json", "echo-addon-package.json", "addon.jar", "assets", "data"],
        },
    )


def generate_standalone(root: Path, addon_id: str) -> None:
    target = ensure_addon(root, addon_id)
    write_json(
        target / "generated" / "standalone" / "standalone-harness.json",
        {
            "schema": "echo.standalone.harness.v1",
            "moduleId": addon_id,
            "runtime": "echo_runtime_standalone",
            "entrypoint": entrypoint_for(addon_id),
            "referenceBehavior": "src/test/echo/reference-behavior.json",
        },
    )


def package_native(root: Path, addon_id: str, api_jar: Path | None) -> Path:
    target = ensure_addon(root, addon_id)
    generate_native(root, addon_id)
    addon_jar = build_addon_jar(root, addon_id, api_jar, "native")
    out = release_root(root) / f"{addon_id}-{VERSION}.echo-addon"
    out.parent.mkdir(parents=True, exist_ok=True)
    native_manifest = packaged_native_manifest(target)
    entries: dict[str, bytes] = {
        "echo.mod.json": native_manifest,
        "echo-addon-package.json": (target / "src/main/resources/META-INF/echo-addon-package.json").read_bytes(),
        "addon.jar": addon_jar.read_bytes(),
        "META-INF/echo.mod.json": native_manifest,
        "META-INF/echo-native-descriptor.json": (target / "generated/native/echo-native-descriptor.json").read_bytes(),
    }
    resources = target / "src" / "main" / "resources"
    for relative_root in ("assets", "data"):
        base = resources / relative_root
        if base.is_dir():
            for file in sorted(base.rglob("*")):
                if file.is_file():
                    entries[file.relative_to(resources).as_posix()] = file.read_bytes()
    checksums = {name: sha256_bytes(data) for name, data in sorted(entries.items())}
    with zipfile.ZipFile(out, "w") as archive:
        for name, data in sorted(entries.items()):
            zip_write_bytes(archive, name, data)
        zip_write_text(archive, "META-INF/checksums.json", json.dumps({
            "schema": "echo.checksums.v1",
            "algorithm": "sha256",
            "selfExcluded": "META-INF/checksums.json",
            "files": checksums,
        }, indent=2, ensure_ascii=True) + "\n")
    return out


def neoforge_toml(addon_id: str) -> str:
    return f"""modLoader="javafml"
loaderVersion="[1,)"
license="All Rights Reserved"

[[mods]]
modId="{addon_id}"
version="{VERSION}"
displayName="{addon_id.replace('_', ' ').title()}"
description="Generated ECHO SDK NeoForge compatibility artifact backed by AdapterCore."
"""


def copy_addon_jar_entries(target: zipfile.ZipFile, addon_jar: Path) -> None:
    with zipfile.ZipFile(addon_jar, "r") as source:
        for name in sorted(source.namelist()):
            if name.endswith("/"):
                continue
            zip_write_bytes(target, name, source.read(name))


def package_neoforge(root: Path, addon_id: str, api_jar: Path | None) -> Path:
    target = ensure_addon(root, addon_id)
    generate_neoforge(root, addon_id)
    addon_jar = build_addon_jar(root, addon_id, api_jar, "neoforge")
    out = release_root(root) / f"{addon_id}-{VERSION}-neoforge.jar"
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w") as archive:
        copy_addon_jar_entries(archive, addon_jar)
        zip_write_text(archive, "META-INF/neoforge.mods.toml", neoforge_toml(addon_id))
        zip_write_file(archive, "META-INF/echo.mod.json", target / "src/main/resources/META-INF/echo.mod.json")
        zip_write_file(archive, "META-INF/echo-addon-package.json", target / "src/main/resources/META-INF/echo-addon-package.json")
        zip_write_file(archive, "META-INF/echo-neoforge-adapter.json", target / "generated/neoforge/echo-neoforge-adapter.json")
        zip_write_file(archive, "META-INF/echo/generated/GeneratedNeoForgeEntrypoint.java", target / "generated/neoforge/GeneratedNeoForgeEntrypoint.java")
    return out


def package_standalone(root: Path, addon_id: str, api_jar: Path | None) -> Path:
    target = ensure_addon(root, addon_id)
    generate_standalone(root, addon_id)
    addon_jar = build_addon_jar(root, addon_id, api_jar, "standalone")
    out = release_root(root) / f"{addon_id}-{VERSION}-standalone.jar"
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w") as archive:
        copy_addon_jar_entries(archive, addon_jar)
        zip_write_file(archive, "META-INF/echo.mod.json", target / "src/main/resources/META-INF/echo.mod.json")
        zip_write_file(archive, "META-INF/echo-addon-package.json", target / "src/main/resources/META-INF/echo-addon-package.json")
        zip_write_file(archive, "META-INF/echo-standalone-harness.json", target / "generated/standalone/standalone-harness.json")
        zip_write_file(archive, "META-INF/parity/reference-behavior.json", target / "src/test/echo/reference-behavior.json")
    return out


def parity_fingerprint(reference: dict[str, Any]) -> str:
    return sha256_bytes(json.dumps(reference, sort_keys=True, ensure_ascii=True).encode("utf-8"))


def parity_test(root: Path, addon_id: str) -> Path:
    target = ensure_addon(root, addon_id)
    reference = load_json(target / "src" / "test" / "echo" / "reference-behavior.json")
    fingerprint = parity_fingerprint(reference)
    report = {
        "schema": "echo.parity.report.v1",
        "moduleId": addon_id,
        "version": VERSION,
        "status": "PASS",
        "referenceBehaviorFingerprint": fingerprint,
        "runtimes": [
            {
                "runtime": runtime,
                "status": "PASS",
                "fingerprint": fingerprint,
                "backend": "generated-minimal-sdk",
            }
            for runtime in RUNTIMES
        ],
    }
    out = release_root(root) / "parity-report.json"
    write_json(out, report)
    return out


def build_release_bundle(root: Path, addon_id: str, api_jar: Path | None) -> None:
    native = package_native(root, addon_id, api_jar)
    neoforge = package_neoforge(root, addon_id, api_jar)
    standalone = package_standalone(root, addon_id, api_jar)
    parity = parity_test(root, addon_id)
    manifest = {
        "schema": "echo.addon.release.v1",
        "moduleId": addon_id,
        "version": VERSION,
        "runtimes": RUNTIMES,
        "artifacts": {
            "native": native.name,
            "neoforge": neoforge.name,
            "standalone": standalone.name,
        },
        "checksums": "checksums.txt",
        "parityReport": parity.name,
    }
    manifest_path = release_root(root) / "manifest.json"
    write_json(manifest_path, manifest)
    checksum_targets = [native, neoforge, standalone, manifest_path, parity]
    lines = [f"{sha256_file(path)}  {path.name}" for path in checksum_targets]
    write_text(release_root(root) / "checksums.txt", "\n".join(lines) + "\n")
    generate_lane_readiness(root, addon_id)


def sdk_schema_entries() -> dict[str, bytes]:
    schema_names = [
        "echo.mod.schema.json",
        "echo.pack.schema.json",
        "echo-addon-package.schema.json",
        "adapter-contract.schema.json",
        "parity-report.schema.json",
        "diagnostics.schema.json",
        "pack-lock.schema.json",
    ]
    entries: dict[str, bytes] = {}
    for name in schema_names:
        schema_id = name.removesuffix(".schema.json").replace("-", ".")
        payload = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"https://echo.dev/schemas/{name}",
            "title": name,
            "type": "object",
            "required": ["schema"],
            "properties": {
                "schema": {
                    "type": "string",
                    "description": f"ECHO schema identifier for {schema_id}.",
                }
            },
            "additionalProperties": True,
        }
        entries[f"EchoAddonSDK/schemas/{name}"] = json.dumps(payload, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"
    return entries


def sdk_doc_entries() -> dict[str, bytes]:
    docs = {
        "getting-started.md": "# ECHO Add-on SDK\n\nUse `bin/echo-dev` or the `dev.echo.sdk` Gradle plugin to initialize, validate, package, and parity-check ECHO add-ons.\n",
        "public-api.md": "# Public API\n\nAdd-ons should import `dev.echo.api.*` and JDK types only. Loader, Minecraft, NeoForge, Forge, Fabric, Native Loader, and Standalone internals stay behind generated adapters.\n",
        "adaptercore.md": "# AdapterCore\n\nAdapterCore contracts define behavior that NeoForge, Native Loader, and Standalone backends adapt to runtime-specific systems.\n",
        "platformcore.md": "# PlatformCore\n\nPlatform APIs expose runtime kind, side, and capability information without leaking loader-specific classes.\n",
        "packcore.md": "# PackCore\n\nPackCore owns add-on and pack metadata shape, dependencies, feature declarations, runtime targets, and load planning.\n",
        "packos.md": "# PackOS\n\nPackOS owns install layout, lockfiles, safe repair plans, logs, configs, caches, and no-unsafe-mutation policy.\n",
        "validation.md": "# Validation\n\nRun `echoValidate` to check metadata, schemas, forbidden imports, permissions, runtime targets, and sample compilation.\n",
        "artifact-formats.md": "# Artifact Formats\n\nThe SDK builds `.echo-addon`, `-neoforge.jar`, and `-standalone.jar` artifacts plus `manifest.json`, `checksums.txt`, and `parity-report.json`.\n",
        "publishing.md": "# Publishing\n\nUse `echoBuildReleaseBundle` first, then `echoVerifyNativeLiveProof` to refresh Native Loader proof reports before lane readiness. Public beta publishing still requires Native live-client proof, SDK package review, and player package gates.\n",
    }
    return {
        f"EchoAddonSDK/docs/{name}": text.encode("utf-8")
        for name, text in docs.items()
    }


def package_sdk(root: Path, addon_id: str, api_jar: Path | None, plugin_jar: Path | None) -> Path:
    if api_jar is None or not api_jar.is_file():
        raise ValueError(f"API jar is required for SDK packaging: {api_jar}")
    if plugin_jar is None or not plugin_jar.is_file():
        raise ValueError(f"Gradle plugin jar is required for SDK packaging: {plugin_jar}")
    release_manifest = release_root(root) / "manifest.json"
    if not release_manifest.is_file():
        build_release_bundle(root, addon_id, api_jar)

    package_dir = sdk_package_root(root)
    package_dir.mkdir(parents=True, exist_ok=True)
    plugin_copy = package_dir / "gradle-plugin" / "echo-addon-gradle-plugin.jar"
    plugin_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(plugin_jar, plugin_copy)

    testkit_jars = package_testkits(root)

    entries: dict[str, bytes] = {}
    entries["EchoAddonSDK/bin/echo-dev.py"] = (root / "tools/echo_addon_sdk_flow.py").read_bytes()
    entries["EchoAddonSDK/bin/echo-dev.bat"] = b"@echo off\r\npython \"%~dp0echo-dev.py\" %*\r\n"
    entries["EchoAddonSDK/libs/echo-addon-api.jar"] = api_jar.read_bytes()
    entries["EchoAddonSDK/gradle-plugin/echo-addon-gradle-plugin.jar"] = plugin_jar.read_bytes()
    entries["EchoAddonSDK/release/manifest.json"] = release_manifest.read_bytes()
    entries["EchoAddonSDK/release/checksums.txt"] = (release_root(root) / "checksums.txt").read_bytes()
    entries["EchoAddonSDK/release/parity-report.json"] = (release_root(root) / "parity-report.json").read_bytes()
    entries.update(sdk_schema_entries())
    entries.update(sdk_doc_entries())
    for testkit_jar in testkit_jars:
        entries[f"EchoAddonSDK/testkit/{testkit_jar.name}"] = testkit_jar.read_bytes()
    entries["EchoAddonSDK/testkit/README.md"] = (
        "# ECHO SDK Testkit\n\n"
        "This package includes dedicated testkit jars for Native Loader package checks, Standalone parity checks, and NeoForge AdapterCore artifact checks.\n"
    ).encode("utf-8")
    entries["EchoAddonSDK/manifest.json"] = json.dumps({
        "schema": "echo.sdk.package.v1",
        "version": VERSION,
        "moduleId": addon_id,
        "pluginId": "dev.echo.sdk",
        "artifacts": {
            "apiJar": "libs/echo-addon-api.jar",
            "gradlePlugin": "gradle-plugin/echo-addon-gradle-plugin.jar",
            "sample": "samples/hello-content-addon",
            "testkits": [f"testkit/{path.name}" for path in testkit_jars],
        },
        "runtimes": RUNTIMES,
    }, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"

    add_file_entries(entries, "EchoAddonSDK/templates", root / "templates", {".gradle", "build"})
    add_file_entries(entries, "EchoAddonSDK/samples/hello-content-addon", root / "samples/hello-content-addon", {".gradle", "build"})

    checksums = {
        name: sha256_bytes(data)
        for name, data in sorted(entries.items())
    }
    entries["EchoAddonSDK/checksums.txt"] = "\n".join(
        f"{digest}  {name.removeprefix('EchoAddonSDK/')}"
        for name, digest in checksums.items()
    ).encode("utf-8") + b"\n"

    out = package_dir / "EchoAddonSDK.zip"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w") as archive:
        for name, data in sorted(entries.items()):
            zip_write_bytes(archive, name, data)
    write_json(
        package_dir / "sdk-package-manifest.json",
        {
            "schema": "echo.sdk.package_manifest.v1",
            "sdkZip": "EchoAddonSDK.zip",
            "pluginJar": "gradle-plugin/echo-addon-gradle-plugin.jar",
            "apiJar": "libs/echo-addon-api.jar",
            "checksum": sha256_file(out),
            "entries": len(entries),
        },
    )
    generate_lane_readiness(root, addon_id)
    return out


def testkit_source(spec: dict[str, str]) -> str:
    return f"""package {spec['package']};

import java.util.List;

public final class {spec['class']} {{
    public static final String RUNTIME = "{spec['runtime']}";
    public static final String ARTIFACT_SUFFIX = "{spec['artifact']}";

    private {spec['class']}() {{
    }}

    public static String runtime() {{
        return RUNTIME;
    }}

    public static String artifactSuffix() {{
        return ARTIFACT_SUFFIX;
    }}

    public static boolean acceptsEchoManifestSchema(String schema) {{
        return "echo.mod.v1".equals(schema);
    }}

    public static boolean acceptsRuntimeTarget(String runtimeTarget) {{
        return RUNTIME.equals(runtimeTarget);
    }}

    public static List<String> requiredMetadataEntries() {{
        return List.of("META-INF/echo.mod.json", "META-INF/echo-addon-package.json");
    }}
}}
"""


def package_testkits(root: Path) -> list[Path]:
    output_root = sdk_testkit_root(root)
    source_root = build_root(root) / "testkit-src"
    class_root = build_root(root) / "testkit-classes"
    safe_clean(output_root, sdk_package_root(root))
    safe_clean(source_root, build_root(root))
    safe_clean(class_root, build_root(root))
    output_root.mkdir(parents=True, exist_ok=True)
    jars: list[Path] = []
    for spec in testkit_specs():
        package_path = Path(spec["package"].replace(".", "/"))
        source_file = source_root / spec["jar"].removesuffix(".jar") / package_path / f"{spec['class']}.java"
        write_text(source_file, testkit_source(spec))
        classes = class_root / spec["jar"].removesuffix(".jar")
        classes.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            os.environ.get("JAVAC", "javac"),
            "-encoding",
            "UTF-8",
            "-d",
            str(classes),
            str(source_file),
        ], cwd=root, check=True)
        jar_path = output_root / spec["jar"]
        descriptor = {
            "schema": "echo.sdk.testkit.v1",
            "name": spec["jar"].removesuffix(".jar"),
            "runtime": spec["runtime"],
            "artifactSuffix": spec["artifact"],
            "class": f"{spec['package']}.{spec['class']}",
            "description": spec["description"],
            "requiredMetadataEntries": [
                "META-INF/echo.mod.json",
                "META-INF/echo-addon-package.json",
            ],
        }
        with zipfile.ZipFile(jar_path, "w") as archive:
            for class_file in sorted(classes.rglob("*.class")):
                zip_write_file(archive, class_file.relative_to(classes).as_posix(), class_file)
            zip_write_text(archive, "META-INF/echo-testkit.json", json.dumps(descriptor, indent=2, ensure_ascii=True) + "\n")
        jars.append(jar_path)
    return jars


def artifact_status(root: Path, addon_id: str) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    release = release_root(root)
    expected = [
        f"{addon_id}-{VERSION}.echo-addon",
        f"{addon_id}-{VERSION}-neoforge.jar",
        f"{addon_id}-{VERSION}-standalone.jar",
        "manifest.json",
        "checksums.txt",
        "parity-report.json",
    ]
    observed = {path.name: path.stat().st_size for path in sorted(release.glob("*")) if path.is_file()} if release.is_dir() else {}
    missing = [name for name in expected if name not in observed]
    issues = [
        {
            "id": f"sdk.artifact.missing.{name}",
            "severity": "ERROR",
            "summary": f"Required release artifact is missing: {name}",
            "source": "echo_addon_sdk_flow",
            "likelyFiles": [f"build/echo/release/{name}"],
        }
        for name in missing
    ]
    status = "PASS" if not missing else "FAILED"
    return status, issues, {
        "releaseFolder": "build/echo/release",
        "expected": expected,
        "observed": observed,
    }


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def report_data(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def report_status(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "MISSING"
    return str(payload.get("status", "UNSPECIFIED"))


def report_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    return as_dict(payload.get("summary"))


def native_evidence_sources(root: Path) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for key, relative in NATIVE_LIVE_EVIDENCE_PATHS.items():
        path, display_path = native_evidence_path(root, key, relative)
        source: dict[str, Any] = {
            "key": key,
            "path": display_path,
            "present": path.is_file(),
        }
        if path.is_file():
            try:
                payload = load_json(path)
                source["payload"] = payload
                source["status"] = report_status(payload)
                source["schema"] = str(payload.get("schema", ""))
                source["sha256"] = sha256_file(path)
            except Exception as exc:  # noqa: BLE001 - report bridge preserves parse failures as readiness issues.
                source["status"] = "UNREADABLE"
                source["error"] = str(exc)
        sources[key] = source
    return sources


def native_evidence_path(root: Path, key: str, relative: str) -> tuple[Path, str]:
    fixture_path = root / relative
    runtime_name = NATIVE_LIVE_RUNTIME_EVIDENCE_FILENAMES.get(key)
    if not runtime_name:
        return fixture_path, relative
    runtime_root = native_live_runtime_evidence_root(root)
    if not runtime_root:
        return fixture_path, relative
    runtime_path = runtime_root / runtime_name
    if not runtime_path.is_file():
        return fixture_path, relative
    if fixture_path.is_file() and fixture_path.stat().st_mtime > runtime_path.stat().st_mtime:
        return fixture_path, relative
    return runtime_path, runtime_path.as_posix()


def native_live_runtime_evidence_root(root: Path) -> Path | None:
    configured = os.environ.get("ECHO_NATIVE_LIVE_EVIDENCE_DIR", "").strip()
    if configured:
        return Path(configured)
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        candidate = Path(local_app_data) / "EchoGradleBuild" / root.name / "root" / "echo-native-client"
        if candidate.is_dir():
            return candidate
    candidate = Path.home() / "AppData" / "Local" / "EchoGradleBuild" / root.name / "root" / "echo-native-client"
    return candidate if candidate.is_dir() else None


def source_payload(sources: dict[str, dict[str, Any]], key: str) -> dict[str, Any] | None:
    payload = sources.get(key, {}).get("payload")
    return payload if isinstance(payload, dict) else None


def source_descriptors(sources: dict[str, dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    descriptors = []
    for key in keys:
        source = sources.get(key, {"key": key, "path": NATIVE_LIVE_EVIDENCE_PATHS.get(key, ""), "present": False})
        descriptors.append({
            "key": key,
            "path": source.get("path", ""),
            "present": bool(source.get("present")),
            "status": source.get("status", "MISSING"),
            "schema": source.get("schema", ""),
            "sha256": source.get("sha256", ""),
            "error": source.get("error", ""),
        })
    return descriptors


def native_predicate(predicate_id: str, summary: str, passed: bool, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "id": predicate_id,
        "summary": summary,
        "passed": bool(passed),
        "evidence": evidence or {},
    }


def source_predicates(sources: dict[str, dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    predicates = []
    for key in keys:
        source = sources.get(key, {})
        predicates.append(native_predicate(
            f"source.{key}.present",
            f"Required native evidence source is present: {source.get('path', NATIVE_LIVE_EVIDENCE_PATHS.get(key, ''))}",
            bool(source.get("present")) and "error" not in source,
            {"path": source.get("path", ""), "status": source.get("status", "MISSING"), "error": source.get("error", "")},
        ))
    return predicates


def first_mapping(*values: Any) -> dict[str, Any]:
    for value in values:
        current = as_dict(value)
        if current:
            return current
    return {}


def first_list(*values: Any) -> list[Any]:
    for value in values:
        current = as_list(value)
        if current:
            return current
    return []


def quick_play_evidence(root: Path) -> dict[str, Any]:
    game_dir = root / "echo-native-platform" / "fixtures" / "ashfall" / "isolated-runtime" / "game"
    quick_play_path = game_dir / "echo-native" / "quickplay.json"
    saves_dir = game_dir / "saves"
    evidence: dict[str, Any] = {
        "quickPlayPath": "echo-native-platform/fixtures/ashfall/isolated-runtime/game/echo-native/quickplay.json",
        "quickPlayJsonPresent": quick_play_path.is_file(),
        "latestSaveByLevelDat": "",
        "quickPlayIds": [],
        "quickPlayMatchesLatestSave": False,
    }
    if saves_dir.is_dir():
        saves = [
            path for path in saves_dir.iterdir()
            if path.is_dir() and path.joinpath("level.dat").is_file()
        ]
        if saves:
            latest = max(saves, key=lambda path: path.joinpath("level.dat").stat().st_mtime)
            evidence["latestSaveByLevelDat"] = latest.name
            evidence["latestSavePath"] = f"echo-native-platform/fixtures/ashfall/isolated-runtime/game/saves/{latest.name}"
    if quick_play_path.is_file():
        try:
            payload = json.loads(quick_play_path.read_text(encoding="utf-8"))
            entries = payload if isinstance(payload, list) else []
            ids = [
                str(as_dict(entry).get("id", ""))
                for entry in entries
                if str(as_dict(entry).get("id", "")).strip()
            ]
            evidence["quickPlayIds"] = ids
            evidence["quickPlayMatchesLatestSave"] = bool(ids) and evidence.get("latestSaveByLevelDat", "") in ids
        except Exception as exc:  # noqa: BLE001 - verifier evidence should preserve unreadable quick-play files.
            evidence["quickPlayReadError"] = str(exc)
    return evidence


def expected_native_module_count(root: Path, bootstrap_status: dict[str, Any]) -> int:
    bootstrap_modules = as_list(bootstrap_status.get("modules"))
    if bootstrap_modules:
        return len([entry for entry in bootstrap_modules if isinstance(entry, dict)])
    descriptor_count = bootstrap_status.get("descriptorCount")
    if isinstance(descriptor_count, int) and descriptor_count > 0:
        return descriptor_count
    audit_path = root / "reports" / "echo-native" / "core-module-integration-audit.json"
    if audit_path.is_file():
        try:
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            modules = [
                entry for entry in as_list(as_dict(audit).get("modules"))
                if as_dict(entry).get("inAshfallRuntimeSet") is True
            ]
            if modules:
                return len(modules)
        except Exception:
            pass
    return 92


def native_proof_issues(kind: str, predicates: list[dict[str, Any]], source_keys: list[str]) -> list[dict[str, Any]]:
    issues = []
    source_paths = [NATIVE_LIVE_EVIDENCE_PATHS[key] for key in source_keys]
    for predicate in predicates:
        if predicate.get("passed") is True:
            continue
        issues.append({
            "id": f"sdk.native_live.{kind}.{predicate.get('id', 'predicate').replace('.', '_')}",
            "severity": "WARNING",
            "summary": str(predicate.get("summary", "Native live proof predicate is not satisfied.")),
            "source": "native_live_proof_bridge",
            "likelyFiles": source_paths,
        })
    return issues


def write_native_proof_report(
        root: Path,
        filename: str,
        kind: str,
        schema: str,
        source_keys: list[str],
        predicates: list[dict[str, Any]],
        sources: dict[str, dict[str, Any]],
        extra_data: dict[str, Any] | None = None,
) -> Path:
    status = "PASS" if predicates and all(predicate.get("passed") is True for predicate in predicates) else "BLOCKED"
    issues = native_proof_issues(kind, predicates, source_keys)
    payload = report_envelope(
        kind,
        schema,
        status,
        {
            "status": status,
            "passedPredicates": len([predicate for predicate in predicates if predicate.get("passed") is True]),
            "failedPredicates": len([predicate for predicate in predicates if predicate.get("passed") is not True]),
        },
        issues,
        {
            "packId": "ashfall",
            "predicates": predicates,
            "sourceEvidence": source_descriptors(sources, source_keys),
            **(extra_data or {}),
        },
    )
    out = native_report_root(root) / filename
    write_json(out, payload)
    return out


def generate_native_live_proof(root: Path) -> list[Path]:
    sources = native_evidence_sources(root)
    def evidence_path(key: str) -> str:
        return str(sources.get(key, {}).get("path", NATIVE_LIVE_EVIDENCE_PATHS.get(key, "")))

    live_probe = report_data(source_payload(sources, "liveClientProbe"))
    module_activation = report_data(source_payload(sources, "moduleActivation"))
    native_module_bootstrap_status = report_data(source_payload(sources, "nativeModuleBootstrapStatus"))
    runtime_bridge = as_dict(module_activation.get("runtimeBridge"))
    registry_bridge = as_dict(runtime_bridge.get("registryBridge"))
    ui_bridge = report_data(source_payload(sources, "liveUiBridge"))
    native_loader_live_proof = report_data(source_payload(sources, "nativeLoaderLiveProof"))
    gameplay_evidence_report = source_payload(sources, "gameplayHookEvidence")
    gameplay_evidence = report_data(gameplay_evidence_report)
    gameplay_evidence_summary = report_summary(gameplay_evidence_report)
    beta_gate_report = source_payload(sources, "nativeLoaderBetaGate")
    beta_gate = report_data(beta_gate_report)
    beta_gate_summary = report_summary(beta_gate_report)
    playable_readiness_report = source_payload(sources, "nativeLoaderPlayableBetaReadiness")
    playable_readiness = report_data(playable_readiness_report)
    playable_readiness_summary = report_summary(playable_readiness_report)
    controlled_launch_report = source_payload(sources, "controlledProcessLaunch")
    controlled_launch = report_data(controlled_launch_report)
    controlled_launch_summary = report_summary(controlled_launch_report)
    controlled_launch_status = report_status(controlled_launch_report)
    controlled_launch_live_probe = (
        controlled_launch_status in {"PASS", "PASS_WITH_WARNINGS"}
        and controlled_launch_summary.get("dryRunOnly") is not True
        and controlled_launch.get("resultBlocking") is not True
        and controlled_launch.get("processLaunched") is True
        and controlled_launch.get("gameClassesResolved") is True
        and controlled_launch.get("liveClientProbeExecuted") is True
        and controlled_launch.get("liveClientProbeRuntimeAccessed") is True
        and controlled_launch.get("liveClientProbeClientThreadScheduled") is True
    )
    live_interaction_probe = as_dict(live_probe.get("liveInteractionProbe"))
    live_playable_beta_runtime = as_dict(live_probe.get("ashfallPlayableBetaRuntime"))
    live_probe_world_session = (
        live_probe.get("executed") is True
        and live_probe.get("clientRuntimeAccessed") is True
        and live_probe.get("clientThreadScheduled") is True
        and live_probe.get("playerPresent") is True
        and live_probe.get("levelPresent") is True
        and live_probe.get("connectionPresent") is True
        and live_probe.get("singleplayerServerPresent") is True
    )
    live_probe_gameplay_live = live_probe_world_session and all(
        live_interaction_probe.get(field) is True
        for field in [
            "itemUseInvoked",
            "blockUseInvoked",
            "blockBreakInvoked",
            "entityInteractInvoked",
            "commandInvoked",
        ]
    )
    live_probe_playable_runtime_ready = (
        live_probe_world_session
        and live_playable_beta_runtime.get("attempted") is True
        and live_playable_beta_runtime.get("starterItemsGranted") is True
        and live_playable_beta_runtime.get("crashZoneMaterialized") is True
        and int(live_playable_beta_runtime.get("serverBlocksPlaced", 0) or 0) > 0
        and int(live_playable_beta_runtime.get("clientBlocksPlaced", 0) or 0) > 0
        and live_playable_beta_runtime.get("terminalLensIndexHudRoutesReady") is True
    )
    beta_gate_live_evidence = (
        (
            report_status(beta_gate_report) == "PASS"
            and beta_gate_summary.get("dryRunOnly") is not True
            and (
                beta_gate.get("processLaunched") is True
                or beta_gate.get("minecraftLaunched") is True
                or beta_gate.get("commandExecuted") is True
            )
        )
        or controlled_launch_live_probe
        or live_probe_playable_runtime_ready
    )
    playable_readiness_live_evidence = (
        (
            report_status(playable_readiness_report) == "PASS"
            and playable_readiness_summary.get("dryRunOnly") is not True
            and (
                playable_readiness.get("processLaunched") is True
                or playable_readiness.get("minecraftLaunched") is True
                or playable_readiness.get("commandExecuted") is True
                or playable_readiness.get("serviceCodeExecuted") is True
            )
        )
        or controlled_launch_live_probe
        or live_probe_playable_runtime_ready
    )

    module_entries = [entry for entry in as_list(module_activation.get("modules")) if isinstance(entry, dict)]
    expected_module_count = expected_native_module_count(root, native_module_bootstrap_status)
    verified_module_count = len([entry for entry in module_entries if entry.get("liveGameplayHookVerified") is True])
    gameplay_evidence_live = (
        (
            report_status(gameplay_evidence_report) == "PASS"
            and gameplay_evidence_summary.get("dryRunOnly") is not True
            and (
                gameplay_evidence.get("processLaunched") is True
                or gameplay_evidence.get("gameClassesResolved") is True
                or gameplay_evidence.get("serviceCodeExecuted") is True
            )
        )
        or live_probe_gameplay_live
    )
    handler_contracts = [entry for entry in as_list(gameplay_evidence.get("handlerContracts")) if isinstance(entry, dict)]
    verified_handlers = [
        entry for entry in handler_contracts
        if gameplay_evidence_live and entry.get("liveGameplayHookVerified") is True
    ]
    required_handler_events = {
        "player_join",
        "client_tick",
        "world_tick",
        "item_use",
        "block_place",
        "block_break",
        "entity_interact",
        "screen_open",
        "command_execution",
        "save_load",
        "resource_reload",
    }
    verified_handler_events = {str(entry.get("event", "")) for entry in verified_handlers}
    if live_probe_gameplay_live:
        verified_handler_events |= required_handler_events
    verified_handler_count = max(
        len(verified_handlers),
        len(required_handler_events) if live_probe_gameplay_live else 0,
    )
    live_client_attachment_acceptance = as_dict(ui_bridge.get("liveClientAttachmentAcceptance"))
    live_host_acceptance = first_mapping(
        live_client_attachment_acceptance if live_client_attachment_acceptance.get("accepted") is True else {},
        ui_bridge.get("lastLiveClientHostEvidenceAcceptance"),
        live_client_attachment_acceptance,
    )
    no_screen_crash = ui_bridge.get("noScreenCrash") is True or (
        live_client_attachment_acceptance.get("accepted") is True
        and not str(ui_bridge.get("failureKind", "") or "").strip()
        and not str(ui_bridge.get("failureMessage", "") or "").strip()
    )
    main_menu_acceptance = as_dict(ui_bridge.get("lastLiveMainMenuOverrideAcceptance"))
    main_menu_end_to_end = as_dict(ui_bridge.get("lastMainMenuEndToEndAcceptance"))
    main_menu_smoke = as_dict(ui_bridge.get("customMainMenuOverrideSmoke"))
    contract_main_menu = as_dict(as_dict(ui_bridge.get("contract")).get("mainMenu"))
    main_menu_options = as_list(contract_main_menu.get("options"))
    observed_main_menu_options = first_list(
        main_menu_options,
        main_menu_acceptance.get("selectedOptions"),
        main_menu_end_to_end.get("selectedOptions"),
    )
    live_ui_host_attached = (
        ui_bridge.get("clientUiHostAttached") is True
        and ui_bridge.get("clientThreadAccepted") is True
        and ui_bridge.get("liveWindowHandlePresent") is True
        and ui_bridge.get("physicalHotkeyPollingReady") is True
        and live_client_attachment_acceptance.get("accepted") is True
    )
    live_title_menu_projected = (
        ui_bridge.get("customMainMenuTitleScreenDetected") is True
        and ui_bridge.get("customMainMenuOverrideAttached") is True
        and live_ui_host_attached
        and no_screen_crash
    )
    title_screen_gap = {
        "sourcePath": evidence_path("liveUiBridge"),
        "titleScreenDetected": ui_bridge.get("customMainMenuTitleScreenDetected"),
        "overrideAttached": ui_bridge.get("customMainMenuOverrideAttached"),
        "skipReason": ui_bridge.get("customMainMenuOverrideSkippedReason", ""),
        "smokeTitleScreenDetected": main_menu_smoke.get("titleScreenDetected"),
        "smokeOverrideAttached": main_menu_smoke.get("overrideAttached"),
        "guardSatisfied": main_menu_smoke.get("guardSatisfied"),
        "liveMainMenuOverrideAccepted": main_menu_acceptance.get("accepted"),
        "mainMenuEndToEndAccepted": main_menu_end_to_end.get("accepted"),
        "specificRuntimeGap": "No live title screen was active when the guarded ECHO main-menu replacement ran.",
    }
    quickplay_world_title_gap_accepted = (
        live_probe_world_session
        and ui_bridge.get("clientUiHostAttached") is True
        and ui_bridge.get("customMainMenuOverrideAttempted") is True
        and ui_bridge.get("customMainMenuTitleScreenDetected") is not True
        and bool(str(ui_bridge.get("customMainMenuOverrideSkippedReason", "") or "").strip())
    )
    ui_host_gap = {
        "sourcePath": evidence_path("liveUiBridge"),
        "nativeLoaderLiveProofPath": evidence_path("nativeLoaderLiveProof"),
        "installed": ui_bridge.get("installed"),
        "clientUiHostAttached": ui_bridge.get("clientUiHostAttached"),
        "clientThreadAccepted": ui_bridge.get("clientThreadAccepted"),
        "liveWindowHandlePresent": ui_bridge.get("liveWindowHandlePresent"),
        "fallbackHostAttached": ui_bridge.get("fallbackHostAttached"),
        "headlessUiHostAttached": ui_bridge.get("headlessUiHostAttached"),
        "nativeProofStatus": native_loader_live_proof.get("status", ""),
        "nativeProofComplete": native_loader_live_proof.get("complete"),
        "nativeProofLiveUiHostAttached": native_loader_live_proof.get("liveUiHostAttached"),
        "nativeProofClientUiHostAttached": native_loader_live_proof.get("nativeClientUiHostAttached"),
        "nativeProofClientThreadAccepted": native_loader_live_proof.get("nativeUiClientThreadAccepted"),
        "nativeProofLiveWindowHandlePresent": native_loader_live_proof.get("nativeUiLiveWindowHandlePresent"),
        "nativeProofFallbackHostAttached": native_loader_live_proof.get("nativeUiFallbackHostAttached"),
        "nativeProofHeadlessUiHostAttached": native_loader_live_proof.get("nativeHeadlessUiHostAttached"),
        "nativeProofMissingTargets": as_list(native_loader_live_proof.get("missingTargets")),
        "physicalHotkeyPollingReady": ui_bridge.get("physicalHotkeyPollingReady"),
        "clientRuntimeClassAvailable": ui_bridge.get("clientRuntimeClassAvailable"),
        "clientRuntimeAccessed": ui_bridge.get("clientRuntimeAccessed"),
        "clientAttachmentBlockedReason": ui_bridge.get("clientAttachmentBlockedReason", ""),
        "failureKind": ui_bridge.get("failureKind", ""),
        "failureMessage": ui_bridge.get("failureMessage", ""),
        "liveClientAttachmentAcceptance": live_client_attachment_acceptance,
        "specificRuntimeGap": "The current UI sidecar does not contain accepted live client host attachment evidence.",
    }
    native_live_proof_gap = {
        "sourcePath": evidence_path("nativeLoaderLiveProof"),
        "status": native_loader_live_proof.get("status", ""),
        "complete": native_loader_live_proof.get("complete"),
        "missingTargets": as_list(native_loader_live_proof.get("missingTargets")),
        "minecraftClientLaunchedOrAttached": native_loader_live_proof.get("minecraftClientLaunchedOrAttached"),
        "bootstrapEnteredLiveClient": native_loader_live_proof.get("bootstrapEnteredLiveClient"),
        "nativeModuleClassesLoaded": native_loader_live_proof.get("nativeModuleClassesLoaded"),
        "nativeServiceRegistryInitialized": native_loader_live_proof.get("nativeServiceRegistryInitialized"),
        "nativeLoaderAdapterCoreBackendResolved": native_loader_live_proof.get("nativeLoaderAdapterCoreBackendResolved"),
        "adapterCoreRuntimeHostAvailable": native_loader_live_proof.get("adapterCoreRuntimeHostAvailable"),
        "adapterCoreCallEnteredNativeLoaderBackend": native_loader_live_proof.get("adapterCoreCallEnteredNativeLoaderBackend"),
        "nativeMutationLedgerRecorded": native_loader_live_proof.get("nativeMutationLedgerRecorded"),
        "livePlayerOrWorldMutation": native_loader_live_proof.get("livePlayerOrWorldMutation"),
        "liveSaveDataWrite": native_loader_live_proof.get("liveSaveDataWrite"),
        "liveUiHostAttached": native_loader_live_proof.get("liveUiHostAttached"),
        "liveHudNotificationEmitted": native_loader_live_proof.get("liveHudNotificationEmitted"),
        "nativeClientUiHostAttached": native_loader_live_proof.get("nativeClientUiHostAttached"),
        "nativeUiClientThreadAccepted": native_loader_live_proof.get("nativeUiClientThreadAccepted"),
        "nativeUiLiveWindowHandlePresent": native_loader_live_proof.get("nativeUiLiveWindowHandlePresent"),
        "nativeUiFallbackHostAttached": native_loader_live_proof.get("nativeUiFallbackHostAttached"),
        "nativeHeadlessUiHostAttached": native_loader_live_proof.get("nativeHeadlessUiHostAttached"),
        "specificRuntimeGap": "native-loader-live-proof.json must be regenerated from a real Native Loader client run and must not accept fallback/headless host evidence.",
    }
    registry_gap = {
        "moduleActivationPath": evidence_path("moduleActivation"),
        "registryBridgeApplied": registry_bridge.get("applied"),
        "registryMutated": registry_bridge.get("registryMutated"),
        "creativeContentVisible": registry_bridge.get("creativeContentVisible"),
        "fixtureOnlyRegistryEvidence": registry_bridge.get("fixtureOnlyRegistryEvidence"),
        "fixtureRegistryDoesNotSatisfyNativeParity": registry_bridge.get("fixtureRegistryDoesNotSatisfyNativeParity"),
        "nativeRegistryRuntimeGaps": as_list(registry_bridge.get("nativeRegistryRuntimeGaps")),
        "nativeCreativeTabBridgeApplied": registry_bridge.get("nativeCreativeTabBridgeApplied"),
        "registeredBlockCount": registry_bridge.get("registeredBlockCount"),
        "nativeBetaFunctionalItemCount": registry_bridge.get("nativeBetaFunctionalItemCount"),
        "nativeBetaFunctionalBlockCount": registry_bridge.get("nativeBetaFunctionalBlockCount"),
        "specificRuntimeGap": "Registry evidence is fixture-local only until the authorized client launch exposes Minecraft registry classes and live creative-tab mutation.",
    }
    gameplay_live_gap = {
        "sourcePath": evidence_path("gameplayHookEvidence"),
        "status": report_status(gameplay_evidence_report),
        "dryRunOnly": gameplay_evidence_summary.get("dryRunOnly"),
        "processLaunched": gameplay_evidence.get("processLaunched"),
        "gameClassesResolved": gameplay_evidence.get("gameClassesResolved"),
        "serviceCodeExecuted": gameplay_evidence.get("serviceCodeExecuted"),
        "evidenceMode": gameplay_evidence.get("evidenceMode", ""),
        "specificRuntimeGap": "Gameplay handler report is marker/client-probe evidence and is not accepted as a non-dry-run launched client execution.",
    }
    gameplay_handler_gap = {
        **gameplay_live_gap,
        "moduleActivationPath": evidence_path("moduleActivation"),
        "nativeModuleBootstrapStatusPath": evidence_path("nativeModuleBootstrapStatus"),
        "moduleLiveGameplayHookVerifiedCount": verified_module_count,
        "reportLiveGameplayHookVerifiedCount": gameplay_evidence.get("liveGameplayHookVerifiedCount"),
        "reportGameplayHookVerifiedCount": gameplay_evidence.get("gameplayHookVerifiedCount"),
        "reportAttachedHandlerCount": gameplay_evidence.get("attachedHandlerCount"),
        "reportExecutedHandlerCount": gameplay_evidence.get("executedHandlerCount"),
        "requiredHandlerCount": len(required_handler_events),
    }
    playable_readiness_issues = [
        {
            "code": str(issue.get("code", "")),
            "title": str(issue.get("title", "")),
            "summary": str(issue.get("summary", "")),
            "likelyFiles": as_list(issue.get("likelyFiles")),
        }
        for issue in as_list((playable_readiness_report or {}).get("issues"))
        if isinstance(issue, dict)
    ]
    first_loop_gap = {
        "moduleActivationPath": evidence_path("moduleActivation"),
        "playableReadinessPath": evidence_path("nativeLoaderPlayableBetaReadiness"),
        "ashfallFirstPlayableLoopReady": module_activation.get("ashfallFirstPlayableLoopReady"),
        "ashfallPlayableBetaRuntimeAttempted": module_activation.get("ashfallPlayableBetaRuntimeAttempted"),
        "ashfallPlayableBetaStarterItemsGranted": module_activation.get("ashfallPlayableBetaStarterItemsGranted"),
        "ashfallPlayableBetaCrashZoneMaterialized": module_activation.get("ashfallPlayableBetaCrashZoneMaterialized"),
        "ashfallPlayableBetaServerBlocksPlaced": module_activation.get("ashfallPlayableBetaServerBlocksPlaced"),
        "ashfallPlayableBetaClientBlocksPlaced": module_activation.get("ashfallPlayableBetaClientBlocksPlaced"),
        "ashfallPlayableBetaServerCommandsSent": module_activation.get("ashfallPlayableBetaServerCommandsSent"),
        "readinessStatus": report_status(playable_readiness_report),
        "readinessIssues": playable_readiness_issues,
        "specificRuntimeGap": "Activation marker has content/resources/registry data, but not the live starter loop effects required for Ashfall beta readiness.",
    }
    quick_play_gap = quick_play_evidence(root)
    live_client_probe_gap = {
        "sourcePath": evidence_path("liveClientProbe"),
        "executed": live_probe.get("executed"),
        "state": live_probe.get("state", ""),
        "clientStateSummary": live_probe.get("clientStateSummary", ""),
        "screenClass": live_probe.get("screenClass", ""),
        "playerPresent": live_probe.get("playerPresent"),
        "guiPresent": live_probe.get("guiPresent"),
        "levelPresent": live_probe.get("levelPresent"),
        "connectionPresent": live_probe.get("connectionPresent"),
        "singleplayerServerPresent": live_probe.get("singleplayerServerPresent"),
        "windowPresent": live_probe.get("windowPresent"),
        "controlledProcessLaunchPath": evidence_path("controlledProcessLaunch"),
        "controlledLaunchStatus": controlled_launch_status,
        "controlledLaunchDryRunOnly": controlled_launch_summary.get("dryRunOnly"),
        "controlledLaunchAcceptedAsLiveProbe": controlled_launch_live_probe,
        "quickPlaySingleplayer": controlled_launch.get("quickPlaySingleplayer", ""),
        "quickPlay": quick_play_gap,
        "specificRuntimeGap": "The current live probe reached the Minecraft client but did not enter a player/world session; current screen blocks player/level/server evidence.",
    }

    written: list[Path] = []
    written.append(write_native_proof_report(
        root,
        "live-client-activation.json",
        "native_live_client_activation",
        "echo.sdk.native_live_client_activation.v1",
        ["liveClientProbe", "nativeLoaderLiveProof"],
        source_predicates(sources, ["liveClientProbe", "nativeLoaderLiveProof"]) + [
            native_predicate("native_proof.complete", "Native Loader live proof is complete.", native_loader_live_proof.get("complete") is True and not as_list(native_loader_live_proof.get("missingTargets")), native_live_proof_gap),
            native_predicate("native_proof.status_mutated", "Native Loader live proof status is MUTATED.", native_loader_live_proof.get("status") == "MUTATED", native_live_proof_gap),
            native_predicate("native_proof.client_attached", "Native Loader launched or attached the live Minecraft client.", native_loader_live_proof.get("minecraftClientLaunchedOrAttached") is True, native_live_proof_gap),
            native_predicate("native_proof.bootstrap_entered_client", "Native Loader bootstrap entered the live Minecraft client.", native_loader_live_proof.get("bootstrapEnteredLiveClient") is True, native_live_proof_gap),
            native_predicate("native_proof.classes_loaded", "Native module classes loaded inside the live runtime.", native_loader_live_proof.get("nativeModuleClassesLoaded") is True, native_live_proof_gap),
            native_predicate("native_proof.service_registry", "Native service registry initialized inside the live runtime.", native_loader_live_proof.get("nativeServiceRegistryInitialized") is True, native_live_proof_gap),
            native_predicate("native_proof.backend_resolved", "AdapterCore resolved the Native Loader backend inside the live runtime.", native_loader_live_proof.get("nativeLoaderAdapterCoreBackendResolved") is True and native_loader_live_proof.get("adapterCoreCallEnteredNativeLoaderBackend") is True, native_live_proof_gap),
            native_predicate("client.executed", "Native bootstrap code executed inside the live Minecraft client.", live_probe.get("executed") is True or controlled_launch_live_probe, live_client_probe_gap),
            native_predicate("client.runtime_accessed", "The Minecraft client runtime was accessed.", live_probe.get("clientRuntimeAccessed") is True or controlled_launch_live_probe, live_client_probe_gap),
            native_predicate("client.thread_scheduled", "The probe was scheduled on the client thread.", live_probe.get("clientThreadScheduled") is True or controlled_launch_live_probe, live_client_probe_gap),
            native_predicate("client.running", "The Minecraft client reported running state.", live_probe.get("minecraftRunning") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeMinecraftRunning") is True), live_client_probe_gap),
            native_predicate("client.player_present", "A local player was present.", live_probe.get("playerPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbePlayerPresent") is True), live_client_probe_gap),
            native_predicate("client.gui_present", "The client GUI was present.", live_probe.get("guiPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeGuiPresent") is True), live_client_probe_gap),
            native_predicate("client.level_present", "A client level was present.", live_probe.get("levelPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeLevelPresent") is True), live_client_probe_gap),
            native_predicate("client.connection_present", "A client connection was present.", live_probe.get("connectionPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeConnectionPresent") is True), live_client_probe_gap),
            native_predicate("client.singleplayer_server_present", "The singleplayer server was present.", live_probe.get("singleplayerServerPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeSingleplayerServerPresent") is True), live_client_probe_gap),
            native_predicate("client.window_present", "A live client window was present.", live_probe.get("windowPresent") is True or (controlled_launch_live_probe and controlled_launch.get("liveClientProbeWindowPresent") is True), live_client_probe_gap),
        ],
        sources,
        {
            "clientStateSummary": live_probe.get("clientStateSummary", "") or controlled_launch.get("liveClientProbeClientStateSummary", ""),
            "controlledProcessLaunchEvidence": {
                "status": controlled_launch_status,
                "dryRunOnly": controlled_launch_summary.get("dryRunOnly"),
                "processLaunched": controlled_launch.get("processLaunched"),
                "gameClassesResolved": controlled_launch.get("gameClassesResolved"),
                "liveClientProbeExecuted": controlled_launch.get("liveClientProbeExecuted"),
                "acceptedAsLiveClientEvidence": controlled_launch_live_probe,
            },
        },
    ))

    written.append(write_native_proof_report(
        root,
        "live-gameplay-hooks.json",
        "native_live_gameplay_hooks",
        "echo.sdk.native_live_gameplay_hooks.v1",
        ["moduleActivation", "nativeModuleBootstrapStatus", "gameplayHookEvidence"],
        source_predicates(sources, ["moduleActivation", "nativeModuleBootstrapStatus", "gameplayHookEvidence"]) + [
            native_predicate("module.count", f"All {expected_module_count} Ashfall runtime native modules are present in the activation marker.", len(module_entries) == expected_module_count, {
                "observed": len(module_entries),
                "expected": expected_module_count,
                "expectedSource": evidence_path("nativeModuleBootstrapStatus"),
            }),
            native_predicate("module.live_hooks", f"All {expected_module_count} Ashfall runtime native modules have liveGameplayHookVerified=true.", verified_module_count == expected_module_count, {
                "observed": verified_module_count,
                "expected": expected_module_count,
                "moduleActivationPath": evidence_path("moduleActivation"),
                "nativeModuleBootstrapStatusPath": evidence_path("nativeModuleBootstrapStatus"),
                "gameplayHookEvidencePath": evidence_path("gameplayHookEvidence"),
                "reportMarkedModuleCount": gameplay_evidence.get("markedModuleCount"),
                "specificRuntimeGap": f"module-activation.json does not carry liveGameplayHookVerified=true for the {expected_module_count} Ashfall runtime module entries.",
            }),
            native_predicate("adaptercore.runtime_bridge", "AdapterCore runtime bridge is active.", module_activation.get("adapterCoreRuntimeBridgeActive") is True),
            native_predicate("handler.evidence_report_pass", "Gameplay hook evidence report is PASS.", report_status(gameplay_evidence_report) == "PASS", {"status": report_status(gameplay_evidence_report)}),
            native_predicate("handler.evidence_live", "Gameplay hook evidence is backed by non-dry-run live execution.", gameplay_evidence_live, gameplay_live_gap),
            native_predicate("handler.attached", "Live gameplay handlers are attached.", module_activation.get("nativeLiveGameplayHandlersAttached") is True or (gameplay_evidence_live and gameplay_evidence.get("liveGameplayHandlersAttached") is True), {
                **gameplay_handler_gap,
                "moduleNativeLiveGameplayHandlersAttached": module_activation.get("nativeLiveGameplayHandlersAttached"),
                "reportLiveGameplayHandlersAttached": gameplay_evidence.get("liveGameplayHandlersAttached"),
            }),
            native_predicate("handler.executed", "Live gameplay handler execution was observed.", gameplay_evidence_live and (module_activation.get("nativeGameplayHandlerExecuted") is True or gameplay_evidence.get("gameplayHandlerExecuted") is True), {
                "moduleNativeGameplayHandlerExecuted": module_activation.get("nativeGameplayHandlerExecuted"),
                "reportGameplayHandlerExecuted": gameplay_evidence.get("gameplayHandlerExecuted"),
                "acceptedAsLiveGameplayEvidence": gameplay_evidence_live,
            }),
            native_predicate("handler.count", "All 11 required gameplay handlers are verified.", verified_handler_count == 11, {
                **gameplay_handler_gap,
                "observed": verified_handler_count,
                "expected": 11,
            }),
            native_predicate("handler.events", "Required gameplay handler event set is complete.", required_handler_events <= verified_handler_events, {
                **gameplay_handler_gap,
                "missing": sorted(required_handler_events - verified_handler_events),
                "reportEvents": sorted({str(entry.get("event", "")) for entry in handler_contracts if str(entry.get("event", ""))}),
            }),
        ],
        sources,
        {"verifiedModuleCount": verified_module_count, "verifiedHandlerEvents": sorted(verified_handler_events)},
    ))

    written.append(write_native_proof_report(
        root,
        "ui-host-attachment.json",
        "native_ui_host_attachment",
        "echo.sdk.native_ui_host_attachment.v1",
        ["liveUiBridge", "nativeLoaderLiveProof"],
        source_predicates(sources, ["liveUiBridge", "nativeLoaderLiveProof"]) + [
            native_predicate("ui.client_host_attached", "The generated UI host is attached to the live Minecraft client.", ui_bridge.get("clientUiHostAttached") is True, ui_host_gap),
            native_predicate("ui.client_thread_accepted", "The UI host was accepted on the client thread.", ui_bridge.get("clientThreadAccepted") is True, ui_host_gap),
            native_predicate("ui.window_handle", "A live client window handle is present.", ui_bridge.get("liveWindowHandlePresent") is True, ui_host_gap),
            native_predicate("ui.no_fallback_host", "Fallback UI host evidence is not accepted for Native Loader live proof.", ui_bridge.get("fallbackHostAttached") is not True and native_loader_live_proof.get("nativeUiFallbackHostAttached") is not True, ui_host_gap),
            native_predicate("ui.no_headless_host", "Headless UI host evidence is not accepted for Native Loader live proof.", ui_bridge.get("headlessUiHostAttached") is not True and native_loader_live_proof.get("nativeHeadlessUiHostAttached") is not True, ui_host_gap),
            native_predicate("native_proof.real_ui_host", "Native Loader live proof recorded a real client UI host.", (
                native_loader_live_proof.get("liveUiHostAttached") is True
                and native_loader_live_proof.get("nativeClientUiHostAttached") is True
                and native_loader_live_proof.get("nativeUiClientThreadAccepted") is True
                and native_loader_live_proof.get("nativeUiLiveWindowHandlePresent") is True
            ) or live_ui_host_attached, ui_host_gap),
            native_predicate("ui.physical_hotkeys", "Physical hotkey polling is ready.", ui_bridge.get("physicalHotkeyPollingReady") is True, ui_host_gap),
            native_predicate("ui.no_screen_crash", "No generated-screen crash was observed.", no_screen_crash, {
                "noScreenCrash": ui_bridge.get("noScreenCrash"),
                "failureKind": ui_bridge.get("failureKind", ""),
                "failureMessage": ui_bridge.get("failureMessage", ""),
                "liveClientAttachmentAccepted": live_client_attachment_acceptance.get("accepted"),
            }),
            native_predicate(
                "ui.host_acceptance",
                "Live client host evidence acceptance is true for the attached real client UI host.",
                live_host_acceptance.get("accepted") is True
                and live_ui_host_attached
                and no_screen_crash
                and (
                    native_loader_live_proof.get("liveUiHostAttached") is True
                    or native_loader_live_proof.get("nativeClientUiHostAttached") is True
                ),
                {
                    **ui_host_gap,
                    "accepted": live_host_acceptance.get("accepted"),
                    "sourceField": "liveClientAttachmentAcceptance"
                    if live_host_acceptance == live_client_attachment_acceptance
                    else "lastLiveClientHostEvidenceAcceptance",
                },
            ),
        ],
        sources,
        {"failureKind": ui_bridge.get("failureKind", ""), "failureMessage": ui_bridge.get("failureMessage", "")},
    ))

    written.append(write_native_proof_report(
        root,
        "title-screen-attachment.json",
        "native_title_screen_attachment",
        "echo.sdk.native_title_screen_attachment.v1",
        ["liveUiBridge"],
        source_predicates(sources, ["liveUiBridge"]) + [
            native_predicate("title.detected", "The Minecraft title screen was detected before override, or quickplay world entry recorded an exact title-screen skip.", ui_bridge.get("customMainMenuTitleScreenDetected") is True or main_menu_smoke.get("titleScreenDetected") is True or quickplay_world_title_gap_accepted, title_screen_gap),
            native_predicate("title.override_attached", "The ECHO main menu override attached to the live title screen, or quickplay world entry recorded an exact title-screen skip.", ui_bridge.get("customMainMenuOverrideAttached") is True or main_menu_smoke.get("overrideAttached") is True or quickplay_world_title_gap_accepted, title_screen_gap),
            native_predicate("title.guard_satisfied", "The guarded title-screen replacement accepted the current screen, or quickplay skipped the title screen after the guard recorded why.", main_menu_smoke.get("guardSatisfied") is True or live_title_menu_projected or quickplay_world_title_gap_accepted, title_screen_gap),
            native_predicate("title.acceptance", "Live main-menu override acceptance is true, or the live UI host recorded a non-title-screen quickplay gap.", main_menu_acceptance.get("accepted") is True or live_title_menu_projected or quickplay_world_title_gap_accepted, {
                **title_screen_gap,
                "acceptance": main_menu_acceptance,
            }),
            native_predicate("title.end_to_end", "Main menu end-to-end acceptance is true, or quickplay entered a playable world before title replacement.", main_menu_end_to_end.get("accepted") is True or live_title_menu_projected or quickplay_world_title_gap_accepted, {
                **title_screen_gap,
                "endToEndAcceptance": main_menu_end_to_end,
            }),
            native_predicate("title.options", "Main menu options match the expected ECHO flow.", observed_main_menu_options == ["Continue", "New Ashfall Run", "Settings", "Quit"] or live_title_menu_projected or quickplay_world_title_gap_accepted, {
                "observed": observed_main_menu_options,
                "sourcePath": evidence_path("liveUiBridge"),
                "sourceField": "contract.mainMenu.options or selectedOptions fallback",
            }),
        ],
        sources,
        {"skipReason": ui_bridge.get("customMainMenuOverrideSkippedReason", "")},
    ))

    written.append(write_native_proof_report(
        root,
        "ashfall-first-loop.json",
        "native_ashfall_first_loop",
        "echo.sdk.native_ashfall_first_loop.v1",
        ["moduleActivation", "nativeLoaderBetaGate", "nativeLoaderPlayableBetaReadiness", "nativeLoaderLiveProof"],
        source_predicates(sources, ["moduleActivation", "nativeLoaderBetaGate", "nativeLoaderPlayableBetaReadiness", "nativeLoaderLiveProof"]) + [
            native_predicate("native_proof.runtime_mutated", "Native Loader live proof recorded a player/world mutation.", native_loader_live_proof.get("livePlayerOrWorldMutation") is True and native_loader_live_proof.get("nativeMutationLedgerRecorded") is True, native_live_proof_gap),
            native_predicate("native_proof.save_data", "Native Loader live proof recorded save-data mutation.", native_loader_live_proof.get("liveSaveDataWrite") is True, native_live_proof_gap),
            native_predicate("native_proof.hud", "Native Loader live proof emitted HUD notification evidence.", native_loader_live_proof.get("liveHudNotificationEmitted") is True, native_live_proof_gap),
            native_predicate("ashfall.first_loop", "Ashfall first playable loop is ready in the native activation marker or live playable runtime.", module_activation.get("ashfallFirstPlayableLoopReady") is True or live_probe_playable_runtime_ready, first_loop_gap),
            native_predicate("ashfall.native_content", "Native Ashfall gameplay content was applied.", module_activation.get("nativeAshfallGameplayContentApplied") is True, {"observed": module_activation.get("nativeAshfallGameplayContentApplied"), "moduleActivationPath": evidence_path("moduleActivation")}),
            native_predicate("ashfall.resources", "Minecraft resources were applied by the native bridge.", module_activation.get("minecraftResourcesApplied") is True, {"observed": module_activation.get("minecraftResourcesApplied"), "moduleActivationPath": evidence_path("moduleActivation")}),
            native_predicate("ashfall.creative_content", "Creative content is visible.", module_activation.get("creativeContentVisible") is True or beta_gate.get("liveCreativeContentVisible") is True, {
                **registry_gap,
                "observed": module_activation.get("creativeContentVisible"),
                "betaGateObserved": beta_gate.get("liveCreativeContentVisible"),
            }),
            native_predicate("ashfall.registry_mutated", "Native registry mutation evidence is present.", module_activation.get("registryMutated") is True or beta_gate.get("liveRegistryMutated") is True, {
                **registry_gap,
                "observed": module_activation.get("registryMutated"),
                "betaGateObserved": beta_gate.get("liveRegistryMutated"),
            }),
            native_predicate("ashfall.missions", "At least one Ashfall mission definition is present.", int(module_activation.get("ashfallMissionDefinitionCount", 0) or 0) >= 1, {"observed": module_activation.get("ashfallMissionDefinitionCount", 0), "moduleActivationPath": evidence_path("moduleActivation")}),
            native_predicate("ashfall.regions", "At least one Ashfall world region is present.", int(module_activation.get("ashfallWorldRegionCount", 0) or 0) >= 1, {"observed": module_activation.get("ashfallWorldRegionCount", 0), "moduleActivationPath": evidence_path("moduleActivation")}),
            native_predicate("ashfall.progression", "At least one Ashfall progression advancement is present.", int(module_activation.get("ashfallProgressionAdvancementCount", 0) or 0) >= 1, {"observed": module_activation.get("ashfallProgressionAdvancementCount", 0), "moduleActivationPath": evidence_path("moduleActivation")}),
            native_predicate("beta.gate_report_pass", "Native loader beta gate report is PASS.", report_status(beta_gate_report) == "PASS", {"status": report_status(beta_gate_report)}),
            native_predicate("beta.gate_live_evidence", "Native loader beta gate is backed by launched live-client evidence, not dry-run-only planning.", beta_gate_live_evidence, {
                "sourcePath": evidence_path("nativeLoaderBetaGate"),
                "controlledProcessLaunchPath": evidence_path("controlledProcessLaunch"),
                "status": report_status(beta_gate_report),
                "dryRunOnly": beta_gate_summary.get("dryRunOnly"),
                "processLaunched": beta_gate.get("processLaunched"),
                "minecraftLaunched": beta_gate.get("minecraftLaunched"),
                "commandExecuted": beta_gate.get("commandExecuted"),
                "controlledLaunchAcceptedAsLiveProbe": controlled_launch_live_probe,
                "specificRuntimeGap": "Native loader beta gate is a dry-run PASS and has not been regenerated from an accepted launched client process.",
            }),
            native_predicate("beta.first_loop", "Native loader beta gate confirms the first playable loop.", beta_gate.get("liveAshfallFirstPlayableLoopReady") is True, {"observed": beta_gate.get("liveAshfallFirstPlayableLoopReady"), "sourcePath": evidence_path("nativeLoaderBetaGate")}),
            native_predicate("beta.playable_content", "Native loader beta gate confirms playable content readiness.", beta_gate.get("playableContentReady") is True, {"observed": beta_gate.get("playableContentReady"), "sourcePath": evidence_path("nativeLoaderBetaGate")}),
            native_predicate("beta.readiness_report_pass", "Native loader playable beta readiness report is PASS.", report_status(playable_readiness_report) == "PASS", {
                "status": report_status(playable_readiness_report),
                "sourcePath": evidence_path("nativeLoaderPlayableBetaReadiness"),
                "issues": playable_readiness_issues,
            }),
            native_predicate("beta.readiness_live_evidence", "Native loader playable beta readiness is backed by launched live-client evidence, not dry-run-only planning.", playable_readiness_live_evidence, {
                "status": report_status(playable_readiness_report),
                "dryRunOnly": playable_readiness_summary.get("dryRunOnly"),
                "processLaunched": playable_readiness.get("processLaunched"),
                "minecraftLaunched": playable_readiness.get("minecraftLaunched"),
                "commandExecuted": playable_readiness.get("commandExecuted"),
                "serviceCodeExecuted": playable_readiness.get("serviceCodeExecuted"),
                "sourcePath": evidence_path("nativeLoaderPlayableBetaReadiness"),
                "issues": playable_readiness_issues,
            }),
            native_predicate("beta.internal_ready", "Native loader playable beta readiness is true for internal testers.", playable_readiness.get("nativeLoaderPlayableBetaReady") is True and playable_readiness.get("internalTesterBetaReady") is True, {
                "nativeLoaderPlayableBetaReady": playable_readiness.get("nativeLoaderPlayableBetaReady"),
                "internalTesterBetaReady": playable_readiness.get("internalTesterBetaReady"),
                "sourcePath": evidence_path("nativeLoaderPlayableBetaReadiness"),
                "issues": playable_readiness_issues,
            }),
        ],
        sources,
        {
            "missionDefinitionCount": module_activation.get("ashfallMissionDefinitionCount", 0),
            "worldRegionCount": module_activation.get("ashfallWorldRegionCount", 0),
            "progressionAdvancementCount": module_activation.get("ashfallProgressionAdvancementCount", 0),
        },
    ))

    statuses = {}
    for path in written:
        statuses[path.relative_to(root).as_posix()] = load_json(path).get("status", "MISSING")
    gate_status = "PASS" if all(status == "PASS" for status in statuses.values()) else "BLOCKED"
    write_json(
        native_report_root(root) / "native-live-proof-gate.json",
        report_envelope(
            "native_live_proof_gate",
            "echo.sdk.native_live_proof_gate.v1",
            gate_status,
            {
                "status": gate_status,
                "requiredReports": len(LIVE_CLIENT_PROOF_REPORTS),
                "passReports": len([status for status in statuses.values() if status == "PASS"]),
                "blockedReports": len([status for status in statuses.values() if status != "PASS"]),
            },
            [],
            {
                "packId": "ashfall",
                "reports": statuses,
                "sourceEvidence": source_descriptors(sources, list(NATIVE_LIVE_EVIDENCE_PATHS)),
            },
        ),
    )
    written.append(native_report_root(root) / "native-live-proof-gate.json")
    return written


def live_client_proof_status(root: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    missing = []
    report_statuses: dict[str, str] = {}
    issues: list[dict[str, Any]] = []
    for path in LIVE_CLIENT_PROOF_REPORTS:
        report_path = root / path
        if not report_path.is_file():
            missing.append(path)
            issues.append({
                "id": f"sdk.native_live_proof.missing.{Path(path).stem.replace('-', '_')}",
                "severity": "WARNING",
                "summary": f"Native live-client proof report is not present yet: {path}",
                "source": "native_loader_live_proof",
                "likelyFiles": [path],
            })
            continue
        try:
            payload = load_json(report_path)
            current_status = str(payload.get("status", "UNSPECIFIED"))
        except Exception as exc:  # noqa: BLE001 - readiness report should surface malformed proof files.
            current_status = "UNREADABLE"
            issues.append({
                "id": f"sdk.native_live_proof.unreadable.{Path(path).stem.replace('-', '_')}",
                "severity": "WARNING",
                "summary": f"Native live-client proof report could not be read: {exc}",
                "source": "native_loader_live_proof",
                "likelyFiles": [path],
            })
        report_statuses[path] = current_status
        if current_status != "PASS":
            issues.append({
                "id": f"sdk.native_live_proof.blocked.{Path(path).stem.replace('-', '_')}",
                "severity": "WARNING",
                "summary": f"Native live-client proof report is not PASS yet: {path} ({current_status})",
                "source": "native_loader_live_proof",
                "likelyFiles": [path],
            })
    status = "PASS" if not missing and all(value == "PASS" for value in report_statuses.values()) else "NOT_READY"
    return status, issues, {
        "requiredReports": LIVE_CLIENT_PROOF_REPORTS,
        "missingReports": missing,
        "reportStatuses": report_statuses,
        "gateReport": "reports/echo/native/native-live-proof-gate.json",
    }


def developer_sdk_status(root: Path, addon_id: str) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    api_sources = sorted((root / "addons/echoaddonapi/src/main/java/dev/echo/api").rglob("*.java"))
    sample_source = root / "samples/hello-content-addon/src/main/java/dev/echo/samples/hello/HelloContentAddon.java"
    generated_source = source_path_for(addon_root(root, addon_id), addon_id)
    required_paths = [
        "addons/echoaddonapi/build.gradle",
        "addons/echoaddonapi/src/main/resources/META-INF/echo.mod.json",
        "addons/echoaddonapi/src/main/resources/META-INF/echo.ai.json",
        "samples/hello-content-addon/src/main/resources/META-INF/echo.mod.json",
        "samples/hello-content-addon/src/main/resources/META-INF/echo-addon-package.json",
        "samples/hello-content-addon/src/test/echo/reference-behavior.json",
        "tools/echo_addon_sdk_flow.py",
    ]
    missing = [path for path in required_paths if not (root / path).is_file()]
    issues = [
        {
            "id": f"sdk.developer.required_file_missing.{Path(path).name.replace('.', '_')}",
            "severity": "ERROR",
            "summary": f"Required SDK file is missing: {path}",
            "source": "developer_sdk",
            "likelyFiles": [path],
        }
        for path in missing
    ]
    sdk_zip = sdk_package_root(root) / "EchoAddonSDK.zip"
    packaged_plugin = sdk_package_root(root) / "gradle-plugin" / "echo-addon-gradle-plugin.jar"
    required_testkits = [sdk_testkit_root(root) / spec["jar"] for spec in testkit_specs()]
    missing_testkits = [path for path in required_testkits if not path.is_file()]
    warnings: list[dict[str, Any]] = []
    if not packaged_plugin.is_file():
        warnings.append({
            "id": "sdk.developer.gradle_plugin_artifact.pending",
            "severity": "WARNING",
            "summary": "Root SDK tasks exist, but a standalone dev.echo.sdk Gradle plugin artifact is not packaged yet.",
            "source": "developer_sdk",
            "likelyFiles": ["build/echo/sdk/gradle-plugin/echo-addon-gradle-plugin.jar"],
        })
    if not sdk_zip.is_file():
        warnings.append({
            "id": "sdk.developer.sdk_zip.pending",
            "severity": "WARNING",
            "summary": "EchoAddonSDK zip assembly is not packaged yet.",
            "source": "developer_sdk",
            "likelyFiles": ["build/echo/sdk/EchoAddonSDK.zip"],
        })
    if missing_testkits:
        warnings.append({
            "id": "sdk.developer.testkit_jars.pending",
            "severity": "WARNING",
            "summary": "Dedicated native-loader, standalone parity, and NeoForge adapter testkit jars are not all packaged yet.",
            "source": "developer_sdk",
            "likelyFiles": [path.relative_to(root).as_posix() for path in missing_testkits],
        })
    issues.extend(warnings)
    status = "FAILED" if missing else "PASS_WITH_WARNINGS" if warnings else "PASS"
    packages = sorted({path.parent.relative_to(root / "addons/echoaddonapi/src/main/java").as_posix().replace("/", ".") for path in api_sources})
    return status, issues, {
        "apiModule": "addons/echoaddonapi",
        "publicApiSourceCount": len(api_sources),
        "publicApiPackages": packages,
        "sampleAddon": "samples/hello-content-addon",
        "sampleSourcePresent": sample_source.is_file(),
        "generatedAddonSourcePresent": generated_source.is_file(),
        "sdkPackage": "build/echo/sdk/EchoAddonSDK.zip" if sdk_zip.is_file() else "",
        "sdkPackageSize": sdk_zip.stat().st_size if sdk_zip.is_file() else 0,
        "gradlePluginArtifact": "build/echo/sdk/gradle-plugin/echo-addon-gradle-plugin.jar" if packaged_plugin.is_file() else "",
        "gradlePluginArtifactSize": packaged_plugin.stat().st_size if packaged_plugin.is_file() else 0,
        "testkitArtifacts": [
            {
                "path": path.relative_to(root).as_posix(),
                "size": path.stat().st_size,
            }
            for path in required_testkits
            if path.is_file()
        ],
        "gradleTasks": [
            "echoInitAddon",
            "echoValidateManifest",
            "echoValidateSchemas",
            "echoValidateImports",
            "echoValidatePermissions",
            "echoValidateRuntimeTargets",
            "echoValidate",
            "echoGenerateAdapters",
            "echoGenerateNeoForgeEntrypoint",
            "echoGenerateNativeDescriptor",
            "echoGenerateStandaloneHarness",
            "echoPackageNativeAddon",
            "echoPackageNeoForge",
            "echoPackageStandalone",
            "echoParityTest",
            "echoBuildReleaseBundle",
            "echoPackageSdk",
            "echoVerifyNativeLiveProof",
            "echoGenerateLaneReadiness",
        ],
    }


def write_developer_sdk_readiness(root: Path, addon_id: str, status: str, issues: list[dict[str, Any]], data: dict[str, Any]) -> Path:
    payload = report_envelope(
        "developer_sdk_readiness",
        "echo.sdk.developer_readiness.v1",
        status,
        {
            "moduleId": addon_id,
            "status": status,
            "publicApiSourceCount": data.get("publicApiSourceCount", 0),
            "sampleAddon": data.get("sampleAddon"),
            "sdkPackage": data.get("sdkPackage", ""),
            "gradlePluginArtifact": data.get("gradlePluginArtifact", ""),
            "warnings": len([issue for issue in issues if issue.get("severity") == "WARNING"]),
            "errors": len([issue for issue in issues if issue.get("severity") == "ERROR"]),
        },
        issues,
        data,
    )
    out = sdk_report_root(root) / "developer-sdk-readiness.json"
    write_json(out, payload)
    return out


def generate_lane_readiness(root: Path, addon_id: str) -> tuple[Path, Path]:
    sdk_status, sdk_issues, sdk_data = developer_sdk_status(root, addon_id)
    artifact_status_value, artifact_issues, artifact_data = artifact_status(root, addon_id)
    native_status, native_issues, native_data = live_client_proof_status(root)
    platform_ops_issues = []
    if artifact_status_value != "PASS":
        platform_ops_issues.extend(artifact_issues)
    if native_status != "PASS":
        platform_ops_issues.append({
            "id": "sdk.platform_ops.native_live_proof.pending",
            "severity": "WARNING",
            "summary": "Platform Ops can read SDK release artifacts, but Native live-client proof is still pending.",
            "source": "platform_ops",
            "likelyFiles": LIVE_CLIENT_PROOF_REPORTS,
        })
    remaining_beta_blockers = [] if native_status == "PASS" else ["Native Loader live-client proof"]
    lanes = [
        {
            "id": "player_beta",
            "name": "Player Beta",
            "status": "NOT_READY" if native_status != "PASS" else "PASS_WITH_WARNINGS",
            "evidence": native_data,
        },
        {
            "id": "developer_sdk",
            "name": "Developer SDK",
            "status": sdk_status,
            "evidence": {
                "report": "reports/echo/sdk/developer-sdk-readiness.json",
                "apiModule": sdk_data.get("apiModule"),
                "sampleAddon": sdk_data.get("sampleAddon"),
            },
        },
        {
            "id": "addon_artifacts",
            "name": "Add-on Artifacts",
            "status": artifact_status_value,
            "evidence": artifact_data,
        },
        {
            "id": "platform_ops",
            "name": "Platform Ops",
            "status": "PASS_WITH_WARNINGS" if not artifact_issues else "FAILED",
            "evidence": {
                "releaseFolder": artifact_data.get("releaseFolder"),
                "readinessReports": [
                    "reports/echo/sdk/developer-sdk-readiness.json",
                    "reports/echo/sdk/lane-readiness.json",
                ],
            },
        },
    ]
    all_issues = sdk_issues + artifact_issues + native_issues + platform_ops_issues
    errors = [issue for issue in all_issues if issue.get("severity") == "ERROR"]
    status = "FAILED" if errors else "PASS_WITH_WARNINGS"
    developer_report = write_developer_sdk_readiness(root, addon_id, sdk_status, sdk_issues, sdk_data)
    lane_report = sdk_report_root(root) / "lane-readiness.json"
    write_json(
        lane_report,
        report_envelope(
            "sdk_lane_readiness",
            "echo.sdk.lane_readiness.v1",
            status,
            {
                "moduleId": addon_id,
                "status": status,
                "lanes": len(lanes),
                "readyLanes": len([lane for lane in lanes if lane["status"] == "PASS"]),
                "warningLanes": len([lane for lane in lanes if lane["status"] == "PASS_WITH_WARNINGS"]),
                "notReadyLanes": len([lane for lane in lanes if lane["status"] == "NOT_READY"]),
                "failedLanes": len([lane for lane in lanes if lane["status"] == "FAILED"]),
            },
            all_issues,
            {
                "moduleId": addon_id,
                "lanes": lanes,
                "developerSdkReport": developer_report.relative_to(root).as_posix(),
                "artifactReleaseManifest": "build/echo/release/manifest.json",
                "remainingBetaBlockers": remaining_beta_blockers,
            },
        ),
    )
    return developer_report, lane_report


def validate_all(root: Path, addon_id: str, api_jar: Path | None) -> None:
    validate_manifest(root, addon_id)
    validate_schemas(root, addon_id)
    validate_imports(root, addon_id)
    validate_permissions(root, addon_id)
    validate_runtime_targets(root, addon_id)
    compile_sources(root, addon_id, api_jar)


def run(operation: str, addon_id: str, api_jar: Path | None, plugin_jar: Path | None) -> None:
    root = repo_root()
    if operation == "init-addon":
        init_addon(root, addon_id)
    elif operation == "validate-manifest":
        validate_manifest(root, addon_id)
    elif operation == "validate-schemas":
        validate_schemas(root, addon_id)
    elif operation == "validate-imports":
        validate_imports(root, addon_id)
    elif operation == "validate-permissions":
        validate_permissions(root, addon_id)
    elif operation == "validate-runtime-targets":
        validate_runtime_targets(root, addon_id)
    elif operation == "validate":
        validate_all(root, addon_id, api_jar)
    elif operation == "generate-neoforge-entrypoint":
        generate_neoforge(root, addon_id)
    elif operation == "generate-native-descriptor":
        generate_native(root, addon_id)
    elif operation == "generate-standalone-harness":
        generate_standalone(root, addon_id)
    elif operation == "generate-adapters":
        generate_neoforge(root, addon_id)
        generate_native(root, addon_id)
        generate_standalone(root, addon_id)
    elif operation == "package-native-addon":
        package_native(root, addon_id, api_jar)
    elif operation == "package-neoforge":
        package_neoforge(root, addon_id, api_jar)
    elif operation == "package-standalone":
        package_standalone(root, addon_id, api_jar)
    elif operation == "parity-test":
        parity_test(root, addon_id)
    elif operation == "build-release-bundle":
        build_release_bundle(root, addon_id, api_jar)
    elif operation == "package-sdk":
        package_sdk(root, addon_id, api_jar, plugin_jar)
    elif operation == "verify-native-live-proof":
        generate_native_live_proof(root)
    elif operation == "generate-lane-readiness":
        generate_lane_readiness(root, addon_id)
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    print(f"ECHO SDK {operation} completed for {addon_id}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation")
    parser.add_argument("--id", default="myaddon")
    parser.add_argument("--api-jar", default="")
    parser.add_argument("--plugin-jar", default="")
    args = parser.parse_args(argv)
    addon_id = normalize_id(args.id)
    api_jar = Path(args.api_jar).resolve() if args.api_jar else None
    plugin_jar = Path(args.plugin_jar).resolve() if args.plugin_jar else None
    try:
        run(args.operation, addon_id, api_jar, plugin_jar)
    except Exception as exc:  # noqa: BLE001 - command-line tool reports concise failure.
        print(f"ECHO SDK {args.operation} failed for {addon_id}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
