# My Native Module - Native Module Template

## Files

- `build.gradle` - SDK plugin and dependencies.
- `echo.mod.json` - metadata with service declaration.
- `NativeModule.java` - `EchoNativeModuleEntrypoint` entry point.
- `NativeService.java` - minimal service implementation.
- `NativeModuleTest.java` - service registration test.

## Build

```bash
./gradlew clean check packageEchoNativeAddon
```

## Expected Output

- `build/echo-native/addons/mynativemodule-1.0.0-RC1.echo-addon`
- packaged `addon.jar` inside the `.echo-addon`

## Policy

`NATIVE` policy. This template demonstrates a module that registers its own registrar and service contract. No NeoForge bridge code is required.

## AdapterCore Gameplay Proof

Modules that mutate gameplay through AdapterCore should use `EchoAdapterCoreGameplayMutationService` and record returned `EchoNativeMutationReceipt` values. A queued command, diagnostic report, or descriptor-only claim is not release proof; player-visible state changes need a receipt with host-state, save-write, HUD/event, or packet/event evidence.
