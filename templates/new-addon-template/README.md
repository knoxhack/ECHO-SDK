# My Addon - New Addon Template

## Files

- `build.gradle` - SDK plugin and dependencies.
- `echo.mod.json` - addon metadata.
- `MyAddon.java` - minimal `EchoNativeModuleEntrypoint`.
- `MyAddonTest.java` - testkit bootstrap test.

## Build

```bash
./gradlew clean check packageEchoNativeAddon
```

## Expected Output

- `build/echo-native/addons/myaddon-1.0.0-RC1.echo-addon`
- packaged `addon.jar` inside the `.echo-addon`
- `build/reports/myaddon-parity.json`

## Policy

This template uses the Native-first RC1 path. For NeoForge compatibility, use a bridge/compat template and keep `@Mod` code out of the Native-first entrypoint.
