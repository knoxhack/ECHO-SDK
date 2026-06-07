# My Addon — New Addon Template

## Files

- `build.gradle` — SDK plugin and dependencies.
- `echo-native-addon.descriptor.json` — addon metadata.
- `MyAddon.java` — minimal entry point.
- `MyAddonTest.java` — testkit bootstrap test.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/myaddon-1.0.0-echo-native.jar`
- `build/reports/myaddon-parity.json`

## Policy

This template uses `nativePolicy: NATIVE`. To start with NeoForge compatibility, change to `NEOFORGE_BRIDGE` and keep your `@Mod` entry point alongside the native one.
