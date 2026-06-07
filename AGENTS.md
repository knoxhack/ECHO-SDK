# ECHO Mod Stack — Agent Notes

## Build

```bash
# Full workspace build (all addons)
gradlew.bat buildEchoWorkspace -PechoAddonSet=all

# Single module compile check
gradlew.bat :echocore:compileJava
```

## Architecture

- **Core layer**: `echocore` (shared APIs, services, registries), `echonetcore` (networking)
- **Root mod**: `echoashfallprotocol` (main survival chapter; registers its own content into shared services)
- **Addons**: Each optional addon lives under `addons/`. Addons should not hardcode content from other addons.

## Integration Patterns

### Optional Dependency Checks
Use `ModList.get().isLoaded("modid")` in mod main class setup. Prefer `EchoIntegrations.current()` for complex checks.

### Service Registration
Addons register capabilities into `EchoCoreServices` (e.g., `registerWorldRegionService`, `registerFactionActionHandler`).
The root mod (`echoashfallprotocol`) should also guard cross-addon service registration behind `isLoaded` checks.

### WorldCore Data-Driven Regions/Hazards
`echoworldcore` loads JSON region/hazard definitions from **all namespaces** under:
- `data/<namespace>/echoworldcore/world_regions/`
- `data/<namespace>/echoworldcore/world_hazards/`

Java base definitions go through `WorldRegionService.registerRegionDefinition()` and are overrideable by JSON datapacks.
Ashfall-specific regions/hazards were moved from `echoworldcore` Java builtins into `echoashfallprotocol`:
- Java: `AshfallWorldCoreBuiltins.java` (registered behind `isLoaded("echoworldcore")`)
- JSON: `addons/echoashfallprotocol/src/main/resources/data/echoashfallprotocol/echoworldcore/world_regions/`

## Schema & Datapack Conventions

- Schemas live in `core/echocore/src/main/resources/assets/echocore/schemas/`
- Datapack examples live in `core/echocore/src/main/resources/data/echocore/datapack_examples/`
- Schema index: `schemas/README.md`

## `neoforge.mods.toml` Conventions

- Every optional cross-addon dependency should have a `reason` field.
- `versionRange="[1.0.0,)"` (or `[1.1.0,)` for echocore)
- Optional cross-addon relationships should use `ordering="NONE"` so soft integrations do not create NeoForge mod sorting cycles.
- Required dependencies on shared API/provider modules should use `ordering="AFTER"`.
- Use `side="BOTH"` unless the integration is strictly client-only.
