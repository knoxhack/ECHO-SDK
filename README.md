# ECHO SDK

Source of truth for ECHO schemas, contracts, templates, API docs, and developer/creator onboarding.

## Purpose

Source of truth for ECHO schemas, contracts, templates, API docs, and developer/creator onboarding.

## What Lives Here

SDK docs, schemas, samples, templates, API stability notes, native authoring guidance, release packaging contracts, and the canonical `.ECHO Content Graph` schema family.

## Release And Update Role

Owns SDK documentation and template releases. Runtime/player artifacts are owned by launcher, module, pack, or runtime repos.

## Current Native SDK Line

The active Native SDK line is `1.0.0-RC1`. The canonical Native addon template compiles against `echo-native-contracts`, `echoaddonapi`, `echoadaptercore`, and `echo-native-testkit`, packages a `.echo-addon`, and has been proven in an external clean project loaded by ECHO Native release mode.

Do not document Native-first addons as importing NeoForge, Forge, Fabric, or `echo-native-loader`. Addons prove mutation only through typed host services returning `EchoNativeMutationReceipt`.

## Unified ECHO Native Player Runtime

ECHO Native is the canonical player-facing contract model for Native Loader,
NeoForge, Standalone Runtime, and Standalone Engine. Runtimes are host adapters;
ECHO modules own menus, HUDs, inventory, keybinds, overlays, terminal, index,
diagnostics, save/session warnings, and gameplay action contracts. Pack
repositories are selectors, asset/configuration owners, and evidence fixtures
only. See [docs/UNIFIED_ECHO_NATIVE_PLAYER_RUNTIME.md](docs/UNIFIED_ECHO_NATIVE_PLAYER_RUNTIME.md)
and [docs/schemas/unified-native-player-runtime.md](docs/schemas/unified-native-player-runtime.md).
Module-owned player surface manifests use `echo.native.player_surface_manifest.v1`
under `data/<module>/echo_native/player_surfaces.json`.

## Public Or Private

Public is recommended for third-party addon and pack developers. Private is acceptable only for unreleased internal contracts.

## Build And Dev Commands

Run commands from the repository root.

- `python tools/echo_sdk.py validate templates --json`
- `python tools/validate_echo_contracts.py --json`
- `python tools/test_echo_contract_schemas.py --json`
- `node scripts/stage-native-sdk-rc1-release.mjs --clean --require-complete`
- `node scripts/test-stage-native-sdk-rc1-release.mjs`
- `python tools/echo_sdk.py create addon --template new-addon-template --id <id> --role community_addon --kind addon --output-root <path>`
- `.\gradlew.bat -p <generated-addon> clean check packageEchoNativeAddon`

## Native SDK RC1 Provenance

`.github/workflows/native-sdk-rc1-provenance.yml` is the workflow-built provenance lane for the public Native SDK RC1 jars. It checks out `ECHO-Native-Platform`, `ECHO-Modules`, and `ECHO-SDK`, builds the five public SDK components, stages the 15 main/source/Javadoc jars with `scripts/stage-native-sdk-rc1-release.mjs`, uploads the staged set as a workflow artifact, and emits GitHub build provenance attestations for the exact staged bytes.

Run it with `publish_release=true` only when replacing the `v1.0.0-RC1` release assets intentionally. Release Index promotion still has to verify the attested digests before changing SDK trust from `source-linked`.

## Artifact Ownership

SDK template bundles, schema snapshots, content graph schemas, and documentation artifacts belong here. Runtime module artifacts (including the generated `-content-graph.json` sidecars and embedded `.echo/content-graph/` trees) stay in `ECHO-Modules`.

## Docs Index

- [docs/getting-started.md](docs/getting-started.md)
- [docs/api/index.md](docs/api/index.md)
- [docs/schemas/index.md](docs/schemas/index.md)
- [docs/schemas/content-graph.md](docs/schemas/content-graph.md)
- [docs/UNIFIED_ECHO_NATIVE_PLAYER_RUNTIME.md](docs/UNIFIED_ECHO_NATIVE_PLAYER_RUNTIME.md)
- [docs/schemas/unified-native-player-runtime.md](docs/schemas/unified-native-player-runtime.md)
- [docs/examples/index.md](docs/examples/index.md)
- [docs/release-packaging.md](docs/release-packaging.md)
- [docs/ecosystem-artifact-ownership.md](docs/ecosystem-artifact-ownership.md)
- [docs/native-addon-guide.md](docs/native-addon-guide.md)
- [docs/neoforge-module-guide.md](docs/neoforge-module-guide.md)
- [docs/standalone-module-guide.md](docs/standalone-module-guide.md)
- [docs/api/optional_integrations.md](docs/api/optional_integrations.md)
- [docs/API_INDEX.md](docs/API_INDEX.md)
- [docs/API_STABILITY.md](docs/API_STABILITY.md)
- [docs/creator_guides/build_your_first_echo_pack.md](docs/creator_guides/build_your_first_echo_pack.md)
- [docs/CREATOR_START_HERE.md](docs/CREATOR_START_HERE.md)
- [docs/CREATOR_TEMPLATES.md](docs/CREATOR_TEMPLATES.md)
- [docs/CREATOR_TOOLING_API.md](docs/CREATOR_TOOLING_API.md)
- [docs/DEVELOPER_START_HERE.md](docs/DEVELOPER_START_HERE.md)
- [docs/examples/integrations/index.md](docs/examples/integrations/index.md)
- [PUBLIC_ALPHA_RELEASE_STATUS.md](PUBLIC_ALPHA_RELEASE_STATUS.md)

## Related Repos

- [knoxhack/ECHO-Launcher](https://github.com/knoxhack/ECHO-Launcher)
- [knoxhack/ECHO-Modules](https://github.com/knoxhack/ECHO-Modules)
- [knoxhack/ECHO-Ashfall-Native-Edition](https://github.com/knoxhack/ECHO-Ashfall-Native-Edition)
- [knoxhack/ECHO-Ashfall-NeoForge-Edition](https://github.com/knoxhack/ECHO-Ashfall-NeoForge-Edition)
- [knoxhack/ECHO-Ashfall-Standalone-Edition](https://github.com/knoxhack/ECHO-Ashfall-Standalone-Edition)
- [knoxhack/ECHO-Release-Index](https://github.com/knoxhack/ECHO-Release-Index)
- [knoxhack/ECHO-Native-Platform](https://github.com/knoxhack/ECHO-Native-Platform)
- [knoxhack/ECHO-Standalone-Runtime](https://github.com/knoxhack/ECHO-Standalone-Runtime)
- [knoxhack/ECHO-Developer-Studio](https://github.com/knoxhack/ECHO-Developer-Studio)
- [knoxhack/ECHO-Addons-Studio](https://github.com/knoxhack/ECHO-Addons-Studio)
- [knoxhack/ECHO-Platform-Website](https://github.com/knoxhack/ECHO-Platform-Website)
