# My Native Module — Native Module Template

## Files

- `build.gradle` — SDK plugin and dependencies.
- `echo-native-addon.descriptor.json` — metadata with service declaration.
- `NativeModule.java` — entry point.
- `NativeService.java` — minimal service implementation.
- `NativeModuleTest.java` — service registration test.

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
