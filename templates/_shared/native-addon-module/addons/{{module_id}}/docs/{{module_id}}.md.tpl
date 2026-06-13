# {{display_name}} Native Contract

- Entrypoint: `{{package_name}}.{{class_name}}`
- Descriptor: `src/main/resources/META-INF/echo.mod.json`
- Package: `build/echo-native/addons/{{module_id}}-1.0.0-RC1.echo-addon`
- Primary feature: `{{feature_id}}`

This addon is release-mode ready only after `./gradlew clean check packageEchoNativeAddon` passes and the resulting `.echo-addon` loads without inferred or local build classpath fallback.
