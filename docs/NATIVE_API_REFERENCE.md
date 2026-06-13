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

### EchoNativeModuleLoadContext

Passed to every `EchoNativeModuleEntrypoint` lifecycle method:

```java
context.registerService(String serviceId, Object implementation, String... surfaces);
context.recordMutation(EchoNativeMutationReceipt receipt);
context.resolveDependency(String moduleId);
context.missingDependency(String moduleId);
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

- `EchoNativeAddonDescriptor` â€” validated addon metadata.
- `EchoNativeBootstrapPlan` â€” loader boot sequence.
- `EchoNativeAddonRuntimeDiscoveryPlan` â€” addon discovery and ordering.
- `EchoNativeAccessPolicy` â€” runtime capability visibility rules.
- `EchoNativeApiStability` â€” stability annotation helper.

## AdapterCore Bridge Types

- `EchoNativeRuntimeHost` â€” registry/capability/event host.
- `EchoBackendEnergyBridge` â€” energy handler portability.
- `EchoBackendFluidBridge` â€” fluid handler portability.
- `EchoBlockDefinition` â€” portable block metadata.
- `EchoClientAdapter` / `EchoCommandAdapter` â€” lane-agnostic client/command hooks.

## Deprecation Policy

1. A type marked `@Deprecated` includes a `since` version and optional `replacement` reference.
2. Deprecated APIs remain present for at least one full minor release.
3. Removal is announced in the RC release notes at least one cycle in advance.
4. Breaking removals are only performed at major version boundaries.

## SDK Versions

| Artifact | Version | Stability |
|---|---|---|
| `echoaddonapi` | `1.0.0-RC1` | Beta |
| `echo-native-contracts` | `1.0.0-RC1` | Beta |
| `echo-sdk-gradle-plugin` | `1.0.0-RC1` | Beta |
| `echo-native-testkit` | `1.0.0-RC1` | Beta |

See [Compatibility Matrix](NATIVE_COMPATIBILITY_MATRIX.md) for runtime version mapping.
