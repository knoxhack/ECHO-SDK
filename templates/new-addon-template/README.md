# My Addon â€” New Addon Template

## Files

- `build.gradle` â€” SDK plugin and dependencies.
- `echo.mod.json` â€” addon metadata.
- `MyAddon.java` â€” minimal entry point.
- `MyAddonTest.java` â€” testkit bootstrap test.

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
