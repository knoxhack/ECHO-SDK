# Screen/HUD Example

Demonstrates a client-side HUD overlay registered as a service.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/screenhudexample-1.0.0-echo-native.jar`

## Policy

`NATIVE`. `side: CLIENT`. For direct NeoForge `Overlay` registration, use `NEOFORGE_BRIDGE` and `EchoClientAdapter`.
