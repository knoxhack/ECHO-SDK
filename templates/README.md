# ECHO Native Templates and Examples

## Canonical Template

| Template | Location | Description |
|---|---|---|
| New addon | `_shared/native-addon-module/` through `new-addon-template` | Canonical Native-first addon scaffold. |

The canonical template generates a fresh Gradle project with:

- `META-INF/echo.mod.json`.
- `EchoNativeModuleEntrypoint`.
- Public SDK dependencies for `1.0.0-RC1`.
- Typed Native registry service usage.
- `echo-native-testkit` smoke test.
- `packageEchoNativeAddon` producing `.echo-addon`.

## Legacy Examples

Older example folders such as `registry-example/`, `event-example/`, `packet-example/`, `config-example/`, `screen-hud-example/`, `worldgen-example/`, and `testkit-example/` are reference material only until refreshed to the canonical template contract. Do not use them as release-mode proof if they self-mint mutation receipts or skip `packageEchoNativeAddon`.

## Policy Notes

Native-first templates must not import NeoForge, Forge, Fabric, or `echo-native-loader` implementation classes. Mutation proof comes from typed host services returning `EchoNativeMutationReceipt`, not from addon-created diagnostic records.

NeoForge support is a separate bridge/compat lane. Keep `@Mod` classes and NeoForge dependencies out of Native-first scaffolds unless the project is explicitly a bridge template.

## Acceptance

- Canonical template generation renders a fresh Gradle project.
- Generated project resolves `dev.echo.native` `1.0.0-RC1` artifacts.
- Generated project passes `./gradlew clean check packageEchoNativeAddon`.
- Packaged `.echo-addon` contains `META-INF/echo.mod.json` and `addon.jar`.
- Release-mode load passes without dev classpath fallback.
