# ECHO Native SDK Maven Artifacts

## Local Publishing

```bash
# Publish all SDK artifacts to local Maven repo
./gradlew publishToMavenLocal
```

Artifacts are installed to `~/.m2/repository/dev/echo/native/`.

## Artifacts

| Artifact ID | Type | Coordinates | Description |
|---|---|---|---|
| `echoaddonapi` | library | `dev.echo.native:echoaddonapi:1.0.0-RC1` | Public addon API surface. |
| `echo-native-contracts` | library | `dev.echo.native:echo-native-contracts:1.0.0-RC1` | Runtime contracts and descriptors. |
| `echo-sdk-gradle-plugin` | plugin | `dev.echo.native:echo-sdk-gradle-plugin:1.0.0-RC1` | Build plugin for addon projects. |
| `echo-native-testkit` | library | `dev.echo.native:echo-native-testkit:1.0.0-RC1` | Headless loader tests. |

## Verification

```bash
# List local artifacts
ls ~/.m2/repository/dev/echo/native/

# Verify source jars exist
ls ~/.m2/repository/dev/echo/native/echoaddonapi/1.0.0-RC1/
# Expected: echoaddonapi-1.0.0-RC1.jar, echoaddonapi-1.0.0-RC1-sources.jar
```

## Consuming in an Addon

```groovy
plugins {
    id 'dev.echo.native.echo-sdk-gradle-plugin' version '1.0.0-RC1'
}

dependencies {
    implementation 'dev.echo.native:echoaddonapi:1.0.0-RC1'
    implementation 'dev.echo.native:echo-native-contracts:1.0.0-RC1'
    testImplementation 'dev.echo.native:echo-native-testkit:1.0.0-RC1'
}
```

## Snapshot / Release Repositories

- Snapshots: `https://maven.echo.dev/snapshots`
- RCs: `https://maven.echo.dev/rc`
- Releases: `https://maven.echo.dev/releases`

## Acceptance

- `echoaddonapi` source jar present.
- `echo-native-contracts` source jar present.
- `echo-sdk-gradle-plugin` artifact resolvable.
- All artifacts publish to local Maven without errors.
