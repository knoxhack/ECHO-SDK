# Event Example

Demonstrates subscribing to ECHO Native events via `EchoEventBus`.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/eventexample-1.0.0-echo-native.jar`

## Policy

`NATIVE`. Events are lane-agnostic where a Native equivalent exists. NeoForge-specific events require `NEOFORGE_BRIDGE` policy and `EchoNativeRuntimeHost`.
