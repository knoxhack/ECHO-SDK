# Unified ECHO Native Player Runtime

The Unified ECHO Native Player Runtime is the cross-host contract model for
player-facing ECHO UI and gameplay.

ECHO Native is the contract layer. Native Loader, NeoForge, Standalone Runtime,
and Standalone Engine are host adapters for that layer. NeoForge may use
Minecraft internals underneath, but ECHO modules own the player-facing menus,
HUD, inventory, keybinds, overlays, terminal, index, diagnostics, save/session
warnings, and gameplay action contracts.

Ashfall and other official packs are conformance fixtures. They do not own
platform UI or gameplay contracts.

## Ownership

| Area | Owner |
| --- | --- |
| Schemas and public contract docs | ECHO-SDK |
| Runtime SPI, typed services, mutation receipts | ECHO-Native-Platform |
| Player-facing feature definitions | ECHO-Modules |
| Host-specific implementations | Runtime repositories |
| Pack selection, assets, configuration, evidence fixtures | Pack repositories |

## Runtime Hosts

| Host id | Role |
| --- | --- |
| `echo_native` | Reference ECHO Native host (Native Loader). |
| `neoforge` | Minecraft compatibility host that adapts ECHO contracts to NeoForge APIs. |
| `echo_runtime_standalone` | Disk-backed parity harness for CI, offline development, and runtime proof. |
| `standalone_engine` | Clean player host for the same ECHO contracts. |

## Schema Family

| Schema | Purpose |
| --- | --- |
| `echo-native-host.schema.json` | Host identity, lifecycle state, services, module graph identity, and capability report. |
| `echo-ui-surface.schema.json` | Menus, screens, HUD layers, overlays, terminal pages, index pages, diagnostics, and fallback policy. |
| `echo-input-binding.schema.json` | Input contexts, default keys, remapping, controller prompts, and conflict groups. |
| `echo-inventory-surface.schema.json` | Hotbar, backpack, equipment, crafting, item actions, and tooltip providers. |
| `echo-gameplay-action.schema.json` | Normalized player/world/session actions that must route through AdapterCore receipts. |
| `echo-save-session.schema.json` | Save identity, Content Graph fingerprint, loaded modules, migration state, and session state. |
| `echo-runtime-conformance.schema.json` | Per-host support/adaptation/fallback/blocker evidence for surfaces and actions. |
| `echo-player-surface-manifest.schema.json` | Module-owned player surface manifest consumed by Content Graph generation. |
| `echo-theme-tokens.schema.json` | Module-owned theme token palette referenced by player surfaces. |
| `echo-playtest-scenario.schema.json` | Playtest scenario steps that verify player surfaces across hosts. |

## Module Surface Manifests

Modules declare player-facing routes in `data/<module>/echo_native/player_surfaces.json`
using `schemaVersion: "echo.native.player_surface_manifest.v1"`. The manifest names
the owner module, host targets, required host services, and each player surface or
contract entry the module owns.

The generator converts these manifests into Content Graph `echo:ui_intent` nodes
and adaptation edges for `neoforge`, `echo_native`, `echo_runtime_standalone`, and
`standalone_engine`. Runtimes consume the generated graph and the SDK contracts;
they should not keep private screen, HUD, input, inventory, terminal, index, or
gameplay action lists as the player-facing source of truth.

## Release Rule

A player-facing feature cannot pass player-ready release gates if it exists only
inside one runtime, one host adapter, or one pack repository. It must have:

- an SDK contract or approved schema extension,
- a module-owned manifest/resource,
- Content Graph nodes and adaptation plans,
- host adapter evidence,
- and runtime conformance evidence.

`fallback` is temporary evidence and does not satisfy full parity unless an
explicit release policy grants it. `blocked` must include a human-readable reason
for Launcher, DependencyDoctor, and developer tooling.

## Mutation Rule

Gameplay success must be backed by AdapterCore mutation receipts. These proof
kinds can satisfy player-ready conformance:

- `HOST_STATE`
- `SAVE_WRITE`
- `HUD_EVENT`
- `PACKET_EVENT`

These are non-proof states and must not satisfy player-ready conformance:

- `DIAGNOSTIC_ONLY`
- `QUEUED_ONLY`
- `METADATA_ONLY`
