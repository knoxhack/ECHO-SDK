# ECHO Native Templates and Examples

## Templates

| Template | Location | Description |
|---|---|---|
| New addon | `new-addon-template/` | Minimal NATIVE addon scaffold. |
| Native module | `native-module-template/` | Module with registrar and service. |

## Examples

| Example | Location | Policy | Side |
|---|---|---|---|
| Registry | `registry-example/` | NATIVE | BOTH |
| Event | `event-example/` | NATIVE | BOTH |
| Packet | `packet-example/` | NATIVE | BOTH |
| Config | `config-example/` | NATIVE | BOTH |
| Screen/HUD | `screen-hud-example/` | NATIVE | CLIENT |
| Worldgen | `worldgen-example/` | NATIVE | BOTH |
| Testkit | `testkit-example/` | NATIVE | BOTH |

## Each Template Contains

- `build.gradle` â€” SDK plugin, dependencies, `packageAddon` config.
- `echo.mod.json` â€” validated metadata.
- Minimal source file(s) â€” entry point and helper classes.
- Test fixture â€” `EchoNativeTestLoader` bootstrap or service test.
- `README.md` â€” build commands, expected output, policy notes.

## Policy Notes

All templates default to `nativePolicy: NATIVE`. To use NeoForge compatibility:
1. Change `nativePolicy` to `NEOFORGE_BRIDGE`.
2. Add a NeoForge `@Mod` entry point alongside the native one.
3. Use `EchoNativeRuntimeHost` for NeoForge-specific registries.

To use Standalone:
1. Change `nativePolicy` to `STANDALONE`.
2. Avoid NeoForge-only imports.
3. Verify with testkit before packaging.

## Acceptance

- All templates generate via `./gradlew build`.
- All templates compile.
- All templates package via `./gradlew packageAddon`.
- All templates have native/neoforge/standalone policy guidance in README.
