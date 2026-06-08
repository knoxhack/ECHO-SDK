# API Index

The public API surface is organized around module descriptors, runtime services, registry contracts, diagnostics, lifecycle hooks, and release metadata.

## Primary Areas

| Area | What to use |
| --- | --- |
| Addon identity | `META-INF/echo.mod.json`, addon ID, version, type, kind, role |
| Runtime targeting | `access.adapterCore.runtimes`, `standalone`, NeoForge metadata |
| Dependencies | `requires`, `optional`, `provides`, `consumes` |
| Stability | [API Stability](../API_STABILITY.md) |
| Optional integrations | [Optional Integrations](optional_integrations.md) |

Java API classes currently live in the module source repos, especially `ECHO-Modules/addons/echoaddonapi/src/main/java/dev/echo/api`.
