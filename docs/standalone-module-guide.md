# Standalone Module Guide

Standalone modules are packaged as `<module>-<version>-standalone.jar` files.

## Required Metadata

- `META-INF/echo.mod.json`
- Runtime classes/resources needed by the standalone runtime

Standalone Edition manifests declare `moduleArtifactFamily: "standalone"`.
