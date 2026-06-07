# Worldgen Example

Demonstrates registering a datapack-friendly worldgen feature service.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/worldgenexample-1.0.0-echo-native.jar`

## Policy

`NATIVE`. Prefer datapack JSON for features, biomes, and structures. Use Java only for procedural logic that cannot be expressed in JSON.
