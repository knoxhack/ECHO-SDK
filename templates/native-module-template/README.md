# My Native Module â€” Native Module Template

## Files

- `build.gradle` â€” SDK plugin and dependencies.
- `echo.mod.json` â€” metadata with service declaration.
- `NativeModule.java` â€” entry point.
- `NativeService.java` â€” minimal service implementation.
- `NativeModuleTest.java` â€” service registration test.

## Build

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageAddon
```

## Expected Output

- `build/libs/mynativemodule-1.0.0-echo-native.jar`

## Policy

`NATIVE` policy. This template demonstrates a module that registers its own registrar and service contract. No NeoForge bridge code is required.
