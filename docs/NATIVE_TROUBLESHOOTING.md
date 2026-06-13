# ECHO Native Troubleshooting

## Installation Issues

### `NativeAddonDescriptorValidationException` on launch

**Cause**: An addon descriptor is missing a required field or contains invalid JSON.
**Fix**:
1. Check `logs/latest.log` for the exact field name and addon ID.
2. Open the addon jar and inspect `META-INF/echo.mod.json`.
3. Ensure `id`, `version`, `entrypoint`, `side`, and `access.nativeClasspath` are present and valid.
4. Re-package the addon after fixing the descriptor.

### `UnsupportedClassVersionError`

**Cause**: Running with Java older than 25.
**Fix**: Install Java 25 and point your launcher to it.

### Loader does not discover an addon

**Cause**: The `.echo-addon` is not installed, descriptor is missing, or the release classpath is incomplete.
**Fix**:
1. Confirm the package filename ends with `.echo-addon` and is in the correct install folder.
2. Open the jar and verify `META-INF/echo.mod.json` exists.
3. Check that `access.nativeClasspath` includes the packaged `addon.jar`.

## Runtime Issues

### `NoClassDefFoundError` for an optional addon

**Cause**: Hard import of an optional addon class without `EchoOptionalServices` guard.
**Fix**: Replace direct references with service lookups or `EchoOptionalServices`:

```java
// Wrong
TerminalService t = TerminalService.instance(); // crashes if absent

// Right
EchoOptionalServices.terminal().ifPresent(t -> t.registerCard(card));
```

### Crash during lifecycle setup

**Cause**: Service registration throwing an exception prevents further addon boot.
**Fix**:
1. Wrap registration in try/catch and log instead of crash.
2. Use `EchoNativeModuleLoadContext.registerService(serviceId, impl, surfaces...)` from `registerServices`.
3. Check the addon's parity report for missing NeoForge bridge dependencies.

### Networking packets not arriving

**Cause**: Packet descriptor missing `side` or `channel` mismatch.
**Fix**:
1. Verify `EchoNetService.registerPacketDescriptor()` was called during initialization.
2. Ensure the packet record implements `EchoPacket` and has a valid `channel` field.
3. Check that sender and receiver agree on schema version.

## Build Issues

### `./gradlew validateAddon` fails with contract errors

**Cause**: A registered service does not implement its declared contract.
**Fix**:
1. Compare the service class against the contract interface.
2. Ensure the contract ID in `echo.mod.json` matches the runtime registration.

### `./gradlew packageAddon` produces no jar

**Cause**: Missing `packageAddon` task configuration or descriptor validation blocked packaging.
**Fix**:
1. Run `./gradlew validateAddon` first and resolve errors.
2. Ensure `echo-sdk-gradle-plugin` is applied and the `echoNative` block is configured.

## Performance Issues

### Stuttering or high tick times

**Cause**: An addon registered a heavy system without a RuntimeGuard budget.
**Fix**:
1. Check `echocore.toml` for budget warnings.
2. Register a budget for your heavy system:

```java
EchoCoreServices.runtimeGuard().registerBudget("echoexample:heavy_sim", 2.0);
```

3. Split work across multiple ticks or use async datapack loading where possible.

## Getting More Help

- Run `/echo export-diagnostics` in-game to produce a support bundle.
- Open an issue using the [Bug Report](../.github/ISSUE_TEMPLATE/bug_report.md) or [Addon Author Support](../.github/ISSUE_TEMPLATE/addon_author_support.md) template.
- Include `latest.log`, `debug.log`, the parity report, and your descriptor JSON.
