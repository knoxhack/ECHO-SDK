# ECHO Native API Reference

## Public API Snapshot

The full public API snapshot is published as:
- `reports/echo/native/plan3/plan3-public-api-snapshot.json`
- Source jars: `echoaddonapi-<version>-sources.jar`, `echo-native-contracts-<version>-sources.jar`

## Stability Annotations

All public types are annotated with one of the following:

| Annotation | Semver Contract | Use In |
|---|---|---|
| `@Stable` | Patch-safe; no breaking changes within major version | Production addons, public integrations |
| `@Beta` | Minor shape changes possible; migration notes in changelog | Early adopters, public packs |
| `@Experimental` | May change or disappear without deprecation | Internal tooling, previews |
| `@Internal` | Not for external use; no compatibility guarantee | ECHO internal modules only |
| `@Deprecated` | Retained for migration; removal target announced | Replace immediately |

Look for `dev.echo.nativeplatform.contracts.EchoNativeApiStatus` on classes and methods.

## Core Services

### EchoCoreServices

```java
// Registry
EchoCoreServices.contentRegistry().registerBlock(id, block);

// Optional lookups (no-op safe)
EchoOptionalServices.index();
EchoOptionalServices.holoMap();
EchoOptionalServices.terminal();
EchoOptionalServices.missionCore();

// Player / Server lifecycle
EchoCoreServices.playerService();
EchoCoreServices.serverLifecycle();
```

### EchoNativeAddonRuntime

Passed to every addon during initialization:

```java
runtime.registerService(String contractId, Object implementation);
runtime.registerEventHandler(EchoNativeEventChannel channel, Consumer<EchoEvent> handler);
runtime.policy(); // Current NativePolicy
```

### EchoNetService

Networking contracts in `echonetcore`:

```java
EchoNetService.registerPacketDescriptor(PacketDescriptor desc);
EchoNetService.sendToPlayer(ServerPlayer player, EchoPacket packet);
EchoNetService.broadcastToDimension(ResourceKey<Level> dim, EchoPacket packet);
```

## Contracts (echo-native-contracts)

Key records and interfaces:

- `EchoNativeAddonDescriptor` — validated addon metadata.
- `EchoNativeBootstrapPlan` — loader boot sequence.
- `EchoNativeAddonRuntimeDiscoveryPlan` — addon discovery and ordering.
- `EchoNativeAccessPolicy` — runtime capability visibility rules.
- `EchoNativeApiStability` — stability annotation helper.

## AdapterCore Bridge Types

- `EchoNativeRuntimeHost` — registry/capability/event host.
- `EchoBackendEnergyBridge` — energy handler portability.
- `EchoBackendFluidBridge` — fluid handler portability.
- `EchoBlockDefinition` — portable block metadata.
- `EchoClientAdapter` / `EchoCommandAdapter` — lane-agnostic client/command hooks.

## Deprecation Policy

1. A type marked `@Deprecated` includes a `since` version and optional `replacement` reference.
2. Deprecated APIs remain present for at least one full minor release.
3. Removal is announced in the RC release notes at least one cycle in advance.
4. Breaking removals are only performed at major version boundaries.

## SDK Versions

| Artifact | Version | Stability |
|---|---|---|
| `echoaddonapi` | `1.0.0-RC` | Beta |
| `echo-native-contracts` | `1.0.0-RC` | Beta |
| `echo-sdk-gradle-plugin` | `1.0.0-RC` | Beta |
| `echo-native-testkit` | `1.0.0-RC` | Beta |

See [Compatibility Matrix](NATIVE_COMPATIBILITY_MATRIX.md) for runtime version mapping.
