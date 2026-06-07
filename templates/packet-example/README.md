# Packet Example

Demonstrates receiving custom packets through the ECHO Native event bus.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/packetexample-1.0.0-echo-native.jar`

## Policy

`NATIVE`. For direct NeoForge `SimpleChannel` usage, use `NEOFORGE_BRIDGE` and `EchoNativeRuntimeHost` networking delegates.
