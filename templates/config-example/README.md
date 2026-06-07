# Config Example

Demonstrates loading and exposing addon configuration through a service.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/configexample-1.0.0-echo-native.jar`

## Policy

`NATIVE`. Config can be TOML or datapack-driven. For NeoForge `ModConfigSpec`, use `NEOFORGE_BRIDGE` and access through `EchoNativeRuntimeHost`.
