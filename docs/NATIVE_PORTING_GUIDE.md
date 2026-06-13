# Porting Guide from NeoForge to ECHO Native

This guide is for moving a NeoForge-style addon toward the ECHO Native `1.0.0-RC1` workflow. Native-first addons compile against the public SDK, package as `.echo-addon`, and load in release mode without direct NeoForge, Forge, Fabric, or loader-internal imports.

## Porting Checklist

### 1. Project Setup

- Apply the ECHO SDK Gradle plugin from the RC channel.
- Compile against the public SDK artifacts: `echo-native-contracts`, `echoaddonapi`, `echoadaptercore`, and `echo-native-testkit`.
- Keep NeoForge dependencies in a bridge/compat source set or separate bridge template, not in the Native-first entrypoint.
- Run `./gradlew clean check packageEchoNativeAddon` before treating the addon as release-mode ready.

### 2. Descriptor

Create `META-INF/echo.mod.json` with the Native descriptor schema:

```json
{
  "schema": "echo.mod.v1",
  "id": "exampleaddon",
  "version": "1.0.0-RC1",
  "entrypoint": "com.example.ExampleAddon",
  "side": "common",
  "access": {
    "nativeClasspath": ["addon.jar"]
  }
}
```

Release mode requires the packaged `access.nativeClasspath` entry. Gradle or IDE classpath inference is a development convenience only and is rejected for player-facing releases.

### 3. Entry Point Migration

Native-first code implements `EchoNativeModuleEntrypoint`:

```java
import dev.echo.nativeplatform.contracts.EchoNativeModuleEntrypoint;
import dev.echo.nativeplatform.contracts.EchoNativeModuleLoadContext;
import dev.echo.nativeplatform.contracts.EchoNativeRegistryService;
import dev.echo.nativeplatform.contracts.EchoNativeRuntimeSide;
import dev.echo.nativeplatform.contracts.EchoNativeServiceMutation;

public final class ExampleAddon implements EchoNativeModuleEntrypoint {
    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        EchoNativeServiceMutation mutation = EchoNativeServiceMutation.of(
                "exampleaddon",
                "registry",
                "declare_content",
                "exampleaddon:copper_wrench",
                EchoNativeRuntimeSide.COMMON
        );
        context.serviceRegistry()
                .service("echo.native.registry", EchoNativeRegistryService.class)
                .map(registry -> registry.register(mutation))
                .ifPresent(context::recordMutation);
    }
}
```

Do not implement or document `EchoNativeAddon` or `EchoNativeAddonRuntime`; they are not the RC1 public entrypoint model. Keep `@Mod` classes only in explicit NeoForge bridge projects.

### 4. Mutation Proof

A module is `MUTATED` only when a typed host service returns an `EchoNativeMutationReceipt` with status `MUTATED`. Descriptor metadata, diagnostic maps, lifecycle history, self-minted receipts, and legacy `activateNative(Map)` claims are not mutation proof.

### 5. Events, Registry, Networking, and Config

Use typed ECHO host services or SDK contracts for Native-first functionality:

- Registry/content: `EchoNativeRegistryService` and typed registry receipts.
- Events: Native event service contracts when available.
- Networking: Native packet/channel contracts when available.
- Config: SDK config contracts or datapack-friendly data, with NeoForge config specs kept in the bridge lane.

If a feature still requires NeoForge APIs, keep that work in a `NEOFORGE_BRIDGE` compatibility project and label it as bridge-only.

### 6. Testing

Add `echo-native-testkit` smoke tests and assert typed mutation receipts:

```java
EchoNativeSdkTestkit.loadReleaseMode(addonPath)
        .requireLoaded("exampleaddon")
        .requireOnlyTypedReceipts("exampleaddon");
```

The external author workflow is:

```bash
./gradlew clean check packageEchoNativeAddon
```

Then load the produced `.echo-addon` through ECHO Native release mode.

## Common Pitfalls

- Direct `ModList`, Forge, Fabric, or NeoForge imports in Native-first code.
- Using descriptor claims or lifecycle callbacks as mutation proof.
- Shipping a dev jar/classes directory instead of a `.echo-addon`.
- Missing `side` or loading client-only code on the server.
- Marking bridge/compat templates as Native-first release evidence.

See [Native Mod Author Guide](NATIVE_MOD_AUTHOR_GUIDE.md), [Native API Reference](NATIVE_API_REFERENCE.md), and [Native Example Addon Walkthrough](NATIVE_EXAMPLE_ADDON_WALKTHROUGH.md) for the canonical RC1 workflow.
