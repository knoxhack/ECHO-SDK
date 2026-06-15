# ECHO Native API Reference

## Public API Snapshot

The public RC1 API is published through these artifacts:

- `dev.echo.native:echo-native-contracts:1.0.0-RC1`
- `dev.echo.native:echoaddonapi:1.0.0-RC1`
- `dev.echo.native:echoadaptercore:1.0.0-RC1`
- `dev.echo.native:echo-native-testkit:1.0.0-RC1` for tests only
- `dev.echo.native:echo-sdk-gradle-plugin:1.0.0-RC1`

Source and Javadoc jars are required for public SDK artifacts before stable `1.0.0`.

## Stability Annotations

All public packages must be classified as one of:

| Stability | Semver Contract | Use In |
|---|---|---|
| `STABLE` | Patch-safe; no breaking changes within the major version | Production addons, public integrations |
| `BETA` | Minor shape changes possible; migration notes required | RC adopters, public packs |
| `INTERNAL` | No compatibility guarantee | ECHO implementation code only |
| `TEST_ONLY` | Test fixtures and harnesses only | Addon tests and validation |

## Canonical Entrypoint

Native-first addons implement `EchoNativeModuleEntrypoint`.

```java
public final class MyAddon implements EchoNativeModuleEntrypoint {
    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        context.registerService("myaddon:service", new MyService(), "registry");
    }
}
```

Do not implement or import `EchoNativeAddon`, `EchoNativeAddonRuntime`, NeoForge `@Mod`, Forge/Fabric loader classes, or `echo-native-loader` implementation classes for Native-first addons.

## EchoNativeModuleLoadContext

Passed to every `EchoNativeModuleEntrypoint` lifecycle method:

```java
context.registerService(String serviceId, Object implementation, String... surfaces);
context.serviceRegistry();
context.recordMutation(EchoNativeMutationReceipt receipt);
context.resolveDependency(String moduleId);
context.missingDependency(String moduleId);
```

`recordMutation` is for receipts returned by typed host services. Addons must not self-mint a `MUTATED` receipt to prove runtime mutation.

## Typed Host Services

Use typed host services to prove Native mutations:

```java
EchoNativeServiceMutation mutation = EchoNativeServiceMutation.of(
        "myaddon",
        "registry",
        "declare_content",
        "myaddon:example",
        EchoNativeRuntimeSide.COMMON
);

context.serviceRegistry()
        .service("echo.native.registry", EchoNativeRegistryService.class)
        .map(registry -> registry.register(mutation))
        .ifPresent(context::recordMutation);
```

A module counts as `MUTATED` only when a typed host service returns an `EchoNativeMutationReceipt` with status `MUTATED`. Descriptor metadata, legacy `activateNative(Map)`, diagnostic maps, and report-only claims are not mutation proof in release mode.

AdapterCore gameplay mutations use `EchoAdapterCoreGameplayMutationService`. The service accepts `EchoNativeServiceMutation` requests for inventory, player state, world blocks, structures, block entities, capabilities, save data, HUD, packets, and events. `MUTATED` responses must carry host-state, save-write, HUD/event, or packet/event evidence; queued-only and diagnostic-only evidence is never release proof.

## Contracts

Key public records and interfaces:

- `EchoNativeModuleEntrypoint` - canonical Native addon entrypoint.
- `EchoNativeModuleLoadContext` - lifecycle context, service registry access, and host receipt recording.
- `EchoNativeAddonDescriptor` - validated `META-INF/echo.mod.json` metadata.
- `EchoNativeServiceMutation` - requested host mutation.
- `EchoNativeMutationReceipt` - typed host mutation proof.
- `EchoAdapterCoreGameplayMutationService` - typed AdapterCore gameplay mutation backend contract.
- `EchoNativeRegistryService` - registry/content host service.
- `EchoNativeRuntimeSide` - common/client/server routing.
- `EchoNativeAccessPolicy` - runtime capability visibility rules.
- `EchoNativeApiStability` - stability annotation helper.

## AdapterCore Bridge Types

- `EchoNativeRuntimeHost` - registry/capability/event host.
- `EchoNativeRuntimeHost.NativeMutationReceipt` - AdapterCore receipt required for release-proof `MUTATED` gameplay results.
- `EchoBackendEnergyBridge` - energy handler portability.
- `EchoBackendFluidBridge` - fluid handler portability.
- `EchoBlockDefinition` - portable block metadata.
- `EchoClientAdapter` / `EchoCommandAdapter` - lane-agnostic client/command hooks.

## Testkit

Use `echo-native-testkit` for headless addon validation:

```java
EchoNativeSdkTestkit.Environment env = EchoNativeSdkTestkit.common("myaddon");
EchoNativeModuleLoadContext context = env.loadEntrypoint(new MyAddon());
env.goldenParity().requireOnlyTypedReceipts();
```

## Deprecation Policy

1. A deprecated type includes a `since` version and optional replacement reference.
2. Deprecated APIs remain present for at least one full minor release.
3. Removal is announced in RC release notes at least one cycle in advance.
4. Breaking removals are only performed at major version boundaries.

## SDK Versions

| Artifact | Version | Stability |
|---|---|---|
| `echoaddonapi` | `1.0.0-RC1` | Beta |
| `echoadaptercore` | `1.0.0-RC1` | Beta |
| `echo-native-contracts` | `1.0.0-RC1` | Beta |
| `echo-sdk-gradle-plugin` | `1.0.0-RC1` | Beta |
| `echo-native-testkit` | `1.0.0-RC1` | Beta |

See [Compatibility Matrix](NATIVE_COMPATIBILITY_MATRIX.md) for runtime version mapping.
