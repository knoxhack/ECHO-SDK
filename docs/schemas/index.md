# Schemas

Schemas define the machine-readable contracts used by launchers, modules, packs, and tools.

## Core Schemas

- Module descriptor: `META-INF/echo.mod.json`
- Addon package: `schemas/echo-addon-package.schema.json`
- Pack manifest: `schemas/echo-pack.schema.json`
- Release Index entry: `schemas/release-index-entry.schema.json`
- Product update entry: `schemas/product-update-entry.schema.json`
- Publisher: `schemas/publisher.schema.json`
- Trust tier: `schemas/trust.schema.json`
- Block entry: `schemas/block.schema.json`
- Channel: `schemas/channel.schema.json`
- Module release manifest: `schemas/module-release-manifest.schema.json`
- Content graph: `schemas/content-graph.schema.json`
- Content graph node: `schemas/content-graph-node.schema.json`
- Content graph edge: `schemas/content-graph-edge.schema.json`
- Content graph export plan: `schemas/content-graph-export-plan.schema.json`
- Content feature list: `schemas/content-feature-list.schema.json`
- Content graph evidence summary: `schemas/content-graph-evidence.schema.json` (`content-graph-evidence.json` in ECHO module releases)
- Pack release metadata: `echo-release.json`
- Pack manifest: edition-specific `.pack.json`

Schema changes must be reflected in SDK docs and docs CI before release.

Run `python tools/validate_echo_contracts.py --json` before changing contract fixtures.

Hytale runtime support is intentionally out of scope for the current content graph schemas. See `docs/schemas/hytale-adapter-rfc.md` for the adapter/codegen and runtime-gate requirements that must exist before Hytale evidence can be treated as playable support.
