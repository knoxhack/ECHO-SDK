# Testkit Example

Demonstrates headless loader tests using `echo-native-testkit`.

## Build

```bash
./gradlew build
./gradlew test
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/testkitexample-1.0.0-echo-native.jar`
- Test results show 1 passed test with live service interaction.

## Policy

`NATIVE`. Testkit spins up an in-memory loader without a full Minecraft client or server. Ideal for CI and fast feedback loops.
