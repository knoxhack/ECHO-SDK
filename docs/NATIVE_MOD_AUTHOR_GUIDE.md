# ECHO Native Mod Author Guide

## Getting Started

1. Clone or download the ECHO Native SDK.
2. Apply the `echo-sdk-gradle-plugin` to your addon project.
3. Pick a [template](NATIVE_TEMPLATES.md) matching your addon type.
4. Write your addon descriptor, service registrations, and content.
5. Validate with `./gradlew validateAddon` and package with `./gradlew packageAddon`.

## Project Structure

```
my-addon/
  build.gradle
  src/main/java/.../MyAddon.java
  src/main/resources/META-INF/echo.mod.json
  src/main/resources/data/myaddon/...
  src/test/java/.../MyAddonTest.java
```

## Descriptor

Every addon needs `echo.mod.json`:

```json
{
  "schema": "echo.mod.v1",
  "id": "myaddon",
  "name": "My Addon",
  "version": "1.0.0-RC1",
  "entrypoint": "com.example.myaddon.MyAddon",
  "side": "common",
  "provides": ["myaddon.registry"],
  "access": {
    "nativeClasspath": ["addon.jar"]
  },
  "apiStability": "beta"
}
```

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Unique modid. Lowercase, no spaces. |
| `name` | Yes | Human-readable name. |
| `version` | Yes | Semver string. |
| `entrypoint` | Yes | Class implementing `EchoNativeModuleEntrypoint`. |
| `side` | Yes | `common`, `client`, or `server`. |
| `provides` | No | Feature IDs this addon provides. |
| `access.nativeClasspath` | Yes | Release-mode classpath entries, usually `addon.jar`. |

## Service Registration

Use `EchoCoreServices` or `EchoNativeModuleLoadContext` to register providers:

```java
public class MyAddon implements EchoNativeModuleEntrypoint {
    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        context.registerService("myaddon:registry_service", new MyRegistryService(), "registry");
    }

    @Override
    public void registerContent(EchoNativeModuleLoadContext context) {
        EchoNativeServiceMutation mutation = EchoNativeServiceMutation.of(
                "myaddon", "registry", "declare_content", "myaddon:example", EchoNativeRuntimeSide.COMMON);
        context.recordMutation(EchoNativeMutationReceipt.mutated("myaddon:registry_service", mutation, 1));
    }
}
```

Keep registrations idempotent and safe to call multiple times during reloads.

## Optional Integration

Never hard-reference optional addons. Use service lookup:

```java
Optional<IndexService> index = EchoOptionalServices.index();
index.ifPresent(i -> i.registerProvider(myDocsProvider));
```

## Build & Package

```bash
# Compile and run tests
./gradlew build

# Validate descriptor and service contracts
./gradlew validateAddon

# Produce .echo-addon distribution
./gradlew packageEchoNativeAddon
```

Output lands in `build/echo-native/addons/<id>-<version>.echo-addon`.

## Testing

Use the `echo-native-testkit` dependency for in-memory loader tests:

```groovy
testImplementation 'dev.echo.native:echo-native-testkit:1.0.0-RC1'
```

```java
@Test
public void testBootstrap() {
    EchoNativeTestLoader loader = new EchoNativeTestLoader();
    loader.loadAddon("myaddon");
    assertTrue(loader.isServiceRegistered("myaddon:registry_service"));
}
```

## Publishing

See [Release Packaging Guide](NATIVE_RELEASE_PACKAGING_GUIDE.md) for artifact naming, checksums, and metadata requirements.
