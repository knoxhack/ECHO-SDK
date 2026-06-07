# {{display_name}} Pack Profile

## Purpose

Describe the planned pack identity, root module, game mode, and release channel.

## Owner Module

`{{module_id}}`

## Inputs

- `packs/{{pack_dir}}/echo.pack.json`
- workspace scan reports
- module graph reports

## Outputs

- `reports/echo/pack-profile.json`
- `reports/echo/pack-readiness.json`

## Gradle Command

```powershell
.\gradlew loadEchoPackProfile -PechoPack={{pack_id}}
.\gradlew generateEchoPackReadiness -PechoPack={{pack_id}} -PechoAddonSet=beta
```

## Safety Behavior

The template writes only metadata. It does not download modules, modify installs, or launch Minecraft.

## Known Limitations

Generated profiles are planned placeholders until their root module, features, assets, lockfile, and readiness gates are reviewed.
