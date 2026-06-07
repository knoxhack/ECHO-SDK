#!/usr/bin/env python3
"""Normalize Gradle printReleaseManifest output for ECHO module releases."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModuleArtifact:
    modulePath: str
    modId: str
    version: str
    sourceJarPath: str
    jarAssetName: str
    sha256: str
    size: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest_line(line: str, line_number: int) -> tuple[str, str, str, Path]:
    parts = line.rstrip("\n").split("|")
    if len(parts) != 4:
        raise ValueError(f"Malformed manifest line {line_number}: expected 4 pipe-delimited fields")
    module_path, mod_id, version, jar_path = (part.strip() for part in parts)
    if not module_path or not mod_id or not version or not jar_path:
        raise ValueError(f"Malformed manifest line {line_number}: fields must not be empty")
    return module_path, mod_id, version, Path(jar_path)


def normalize(input_path: Path, output_dir: Path) -> list[ModuleArtifact]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[ModuleArtifact] = []
    used_asset_names: set[str] = set()

    lines = [line for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"No release manifest rows found in {input_path}")

    for index, line in enumerate(lines, start=1):
        module_path, mod_id, version, jar_path = parse_manifest_line(line, index)
        if not jar_path.is_file():
            raise FileNotFoundError(f"Release jar does not exist for {module_path}: {jar_path}")

        asset_name = jar_path.name
        if asset_name.lower() in used_asset_names:
            raise ValueError(f"Duplicate release jar asset name '{asset_name}' from {module_path}")
        used_asset_names.add(asset_name.lower())

        target_path = output_dir / asset_name
        shutil.copy2(jar_path, target_path)
        artifacts.append(
            ModuleArtifact(
                modulePath=module_path,
                modId=mod_id,
                version=version,
                sourceJarPath=str(jar_path),
                jarAssetName=asset_name,
                sha256=sha256_file(target_path),
                size=target_path.stat().st_size,
            )
        )

    artifacts.sort(key=lambda item: (item.modulePath, item.modId, item.version))
    return artifacts


def write_outputs(output_dir: Path, artifacts: list[ModuleArtifact]) -> None:
    index = {
        "formatVersion": 1,
        "generatedBy": "tools/normalize_echo_release_manifest.py",
        "artifactCount": len(artifacts),
        "artifacts": [contract_artifact(artifact) for artifact in artifacts],
    }
    (output_dir / "echo-modules-index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    with (output_dir / "release-manifest.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["modulePath", "modId", "version", "jarAssetName", "sha256", "size"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for artifact in artifacts:
            writer.writerow(contract_artifact(artifact))

    checksum_rows: list[str] = []
    for path in sorted(output_dir.rglob("*")):
        if path.is_file() and path.name != "checksums.sha256":
            rel = path.relative_to(output_dir).as_posix()
            checksum_rows.append(f"{sha256_file(path)}  {rel}")
    (output_dir / "checksums.sha256").write_text("\n".join(checksum_rows) + "\n", encoding="utf-8")


def contract_artifact(artifact: ModuleArtifact) -> dict[str, str | int]:
    return {
        "modulePath": artifact.modulePath,
        "modId": artifact.modId,
        "version": artifact.version,
        "jarAssetName": artifact.jarAssetName,
        "sha256": artifact.sha256,
        "size": artifact.size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize ECHO Gradle release manifest output.")
    parser.add_argument("--input", required=True, type=Path, help="Raw output from gradlew printReleaseManifest.")
    parser.add_argument("--out", required=True, type=Path, help="Output directory for release assets.")
    args = parser.parse_args()

    artifacts = normalize(args.input, args.out)
    write_outputs(args.out, artifacts)
    print(f"Normalized {len(artifacts)} ECHO module artifact(s) into {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
