# {{mod_name}}

## Purpose

Describe the production purpose of `{{module_id}}` before adding it to a real pack.

## Owner Module

`{{module_id}}`

## Inputs

- ECHO module metadata
- ECHO AI metadata
- Feature contracts for `{{feature_id}}`

## Outputs

- A scanned module entry
- A module graph node
- A feature provider declaration

## Report Schema

This scaffold is consumed by `workspace-scan.json`, `scanned-modules.json`, `module-graph.json`, and `feature-graph.json`.

## Gradle Command

```powershell
.\gradlew scanEchoWorkspace -PechoAddonSet=beta
.\gradlew generateEchoModuleGraph -PechoAddonSet=beta
```

## Launcher Usage

Launcher usage is blocked until the module is explicitly added to a reviewed pack profile.

## Command Center Usage

Command Center can display the module after workspace reports are regenerated.

## CyberDex/Codex Usage

Use `META-INF/echo.ai.json` safe edit zones and protected files before assigning automation.

## Safety Behavior

Generated modules are local-only and planning-safe until manually registered.

## Failure Behavior

Missing or invalid metadata should produce diagnostics, not scanner crashes.

## Known Limitations

The scaffold is not production content and has no runtime gameplay behavior beyond module initialization.

## Next Planned Improvements

Replace placeholder contracts, review dependencies, and add focused tests before pack integration.
