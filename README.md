# ECHO SDK

Source of truth for ECHO schemas, contracts, templates, API docs, and developer/creator onboarding.

## Purpose

Source of truth for ECHO schemas, contracts, templates, API docs, and developer/creator onboarding.

## What Lives Here

SDK docs, schemas, samples, templates, API stability notes, native authoring guidance, and release packaging contracts.

## Release And Update Role

Owns SDK documentation and template releases. Runtime/player artifacts are owned by launcher, module, pack, or runtime repos.

## Public Or Private

Public is recommended for third-party addon and pack developers. Private is acceptable only for unreleased internal contracts.

## Build And Dev Commands

Run commands from the repository root.

- `python tools/echo_sdk.py validate templates --json`
- `python tools/validate_echo_contracts.py --json`
- `python tools/test_echo_contract_schemas.py --json`

## Artifact Ownership

SDK template bundles, schema snapshots, and documentation artifacts belong here. Runtime module artifacts stay in `ECHO-Modules`.

## Docs Index

- [docs/getting-started.md](docs/getting-started.md)
- [docs/api/index.md](docs/api/index.md)
- [docs/schemas/index.md](docs/schemas/index.md)
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
