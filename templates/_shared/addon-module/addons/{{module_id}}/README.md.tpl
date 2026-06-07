# {{mod_name}}

Generated from `{{template_id}}`.

## Purpose

`{{module_id}}` starts as a local-only ECHO SDK addon for the `{{role}}` role and `{{feature_id}}` feature.

## Safety

This scaffold does not edit the real workspace settings, does not launch Minecraft, does not download modules, and does not perform repair actions. Review metadata and dependencies before promoting it into an official addon set.

## Validation

```powershell
.\gradlew :{{module_id}}:compileJava -PechoAddonSet=beta
.\gradlew scanEchoWorkspace -PechoAddonSet=beta
.\gradlew generateEchoModuleGraph -PechoAddonSet=beta
```
