# {{display_name}}

Native-first ECHO addon generated from the public SDK template.

## Build

```bash
./gradlew build
./gradlew packageEchoNativeAddon
```

The packaged addon is written to `build/echo-native/addons/{{module_id}}-1.0.0-RC1.echo-addon`.

## Public API Boundary

Use `echoaddonapi`, `echoadaptercore`, and `echo-native-contracts`. Do not import `echo-native-loader`, NeoForge, Forge, or Fabric APIs from a Native-first addon.
