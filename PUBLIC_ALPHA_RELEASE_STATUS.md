# ECHO SDK Release Status

The active Native SDK release line is `1.0.0-RC1`.

The canonical Native addon scaffold now proves the external developer workflow:

1. Generate a fresh addon project.
2. Resolve `dev.echo.native` public SDK artifacts.
3. Compile without NeoForge or `echo-native-loader` imports.
4. Run `echo-native-testkit`.
5. Package a `.echo-addon`.
6. Load through ECHO Native release mode without dev classpath fallback.

The SDK should still be described as beta/RC until the Native Platform stable gates pass and public Maven/release provenance is attached. Stable `1.0.0` is blocked until all public artifacts have source and Javadoc jars, the canonical template is proven from a clean checkout, and Release Index metadata no longer carries warning/block/source-linked stable blockers.

Workflow-built provenance is now routed through `.github/workflows/native-sdk-rc1-provenance.yml`. That workflow builds the public SDK jars from `ECHO-Native-Platform`, `ECHO-Modules`, and `ECHO-SDK`, stages the 15 RC1 main/source/Javadoc jars, uploads the staged set, and emits GitHub build provenance attestations. Do not mark the SDK stable until the Release Index verifies those attestations against the indexed release asset digests.
