# {{display_name}} Native Release Checklist

- Uses `echoaddonapi`, `echoadaptercore`, and `echo-native-contracts` only.
- Avoids `echo-native-loader` implementation imports.
- Avoids direct NeoForge runtime imports.
- Declares typed mutation receipts for content changes.
- Provides parity evidence for lifecycle, registries, events, config, networking, resources, and save data.
