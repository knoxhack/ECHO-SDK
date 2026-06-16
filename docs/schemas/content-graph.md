# ECHO Content Graph

The `.ECHO Content Graph` is a runtime-neutral, portable semantic model of ECHO modules, addons, and gameplay content.

## Schema Family

| File | Schema ID | Purpose |
|------|-----------|---------|
| `content-graph.schema.json` | `echo.content_graph.v1` | Top-level graph document |
| `content-graph-node.schema.json` | `echo.content_graph.node.v1` | Typed node envelope |
| `content-graph-edge.schema.json` | `echo.content_graph.edge.v1` | Typed relationship |
| `content-graph-export-plan.schema.json` | `echo.content_graph.export_plan.v1` | Per-runtime export planning |
| `content-feature-list.schema.json` | `echo.content_feature_list.v1` | Human-facing feature list |
| `content-graph-evidence.schema.json` | `echo.content_graph.evidence.v1` | Canonical release/workspace graph evidence summary |

## Node Kinds

- `echo:module`
- `echo:addon`
- `echo:dependency`
- `echo:asset`
- `echo:block`
- `echo:item`
- `echo:creative_tab`
- `echo:recipe`
- `echo:entity`
- `echo:npc`
- `echo:region`
- `echo:trigger`
- `echo:effect`
- `echo:mission`
- `echo:objective`
- `echo:ui_intent`
- `echo:setting`
- `echo:system`

## Edge Kinds

- `addon_contains_module`
- `module_requires_module`
- `module_declares_runtime`
- `block_uses_asset`
- `item_uses_asset`
- `creative_tab_contains_item`
- `recipe_consumes_item`
- `recipe_outputs_item`
- `mission_has_objective`
- `objective_targets_node`
- `ui_intent_controls_node`
- `trigger_invokes_effect`
- `region_contains_trigger`
- `setting_affects_system`
- `system_declares_capability`

## UI Intent Model

UI surfaces are represented as `echo:ui_intent` nodes with neutral `intent` values and per-runtime `fallbacks`.

Supported intents:

- `selection_menu`
- `detail_panel`
- `notification`
- `terminal_page`
- `map_overlay`
- `scanner_result`
- `inventory_action`
- `confirmation_prompt`
- `settings_panel`
- `progress_tracker`

## Runtime Hints

Runtime-specific implementation detail belongs only inside `runtimeHints.<target>`:

- `runtimeHints.neoforge`
- `runtimeHints.echo_native`
- `runtimeHints.echo_runtime_standalone`
- `runtimeHints.hytale`

Portable fields must never contain NeoForge screen classes, block entity classes, registry classes, or Minecraft package names.

## Export Planning

The export plan schema supports planning statuses:

- `direct`
- `adapter_required`
- `fallback`
- `blocked`
- `not_applicable`

Hytale export is planning-only; no runtime code generation is produced by this schema. Status values such as `direct`, `adapter_required`, `fallback`, and `blocked` are export planning evidence only and must not be displayed as playable/runtime support.

Entity and NPC nodes use typed actor planning. If a node lacks a Hytale actor contract or explicit fallback, the export plan should mark it `blocked` with:

- `blockedReasonCode`
- `contract`
- `requiredAdapter`
- `recommendedFix`

These fields describe the missing adapter contract only. They are not a Hytale runtime schema and must not be treated as generated Hytale content.

## Evidence Summary

Tools that do not need the full graph should publish or display a compact `echo.content_graph.evidence.v1` summary. For ECHO module releases, this is published as the root-level `content-graph-evidence.json` artifact and is the canonical release evidence document. Local scanners may emit the same shape as workspace or installed evidence, but should label that source separately from release evidence.

Required aggregate fields:

- `graphCount`, `moduleCount`, `nodeCount`, `edgeCount`, `featureCount`, `exportPlanCount`
- `hytaleBlockerCount` and optional `hytaleSummary`
- `modules[]` entries with per-module counts, `validationState`, `hytaleBlockers`, and `validationIssues`

Hytale blocker normalization is canonical: prefer explicit `nodes[]` entries where `status === "blocked"` and format them as `<nodeId>: <rationale>`. If only `summary.blocked` is present, report the blocked count as summary evidence. Legacy `blockers[]` arrays may be displayed for compatibility but should not be emitted by new generators.

The evidence summary is diagnostic metadata. It must not be treated as a Hytale runtime export or as proof that target runtime assets were generated.
Do not introduce or claim a Hytale runtime schema from this evidence document alone; a Hytale adapter/codegen contract and runtime validation gate must exist first.

## Example Graph Document

A complete `content-graph.json` for a tiny module (`echocore`) that defines one block, one item, one recipe, one mission, and the UI intent that opens the mission terminal:

```json
{
  "schemaVersion": "echo.content_graph.v1",
  "id": "echocore:content_graph/1.0.0",
  "moduleId": "echocore",
  "generatedAt": "2026-06-14T12:00:00Z",
  "modules": ["echocore"],
  "provenance": {
    "generatedBy": "generate-content-graph.mjs",
    "generatedAt": "2026-06-14T12:00:00Z",
    "sourceRepo": "knoxhack/ECHO-Modules",
    "commitSha": "a1b2c3d"
  },
  "nodes": [
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:module",
      "id": "echocore:module/echocore",
      "moduleId": "echocore",
      "displayName": "ECHO Core",
      "description": "Foundation blocks, items, and systems shared by ECHO experiences.",
      "capabilities": ["block_registry", "item_registry", "recipe_provider"]
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:block",
      "id": "echocore:block/ashfall_bricks",
      "moduleId": "echocore",
      "displayName": "Ashfall Bricks",
      "data": { "hardness": 1.5, "material": "stone", "resistance": 6.0 },
      "runtimeHints": {
        "neoforge": { "blockClass": "dev.echo.echocore.block.AshfallBricksBlock", "registryName": "ashfall_bricks" },
        "hytale": { "voxelShape": "cube", "textureSet": "ashfall_bricks" }
      }
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:item",
      "id": "echocore:item/ashfall_ingot",
      "moduleId": "echocore",
      "displayName": "Ashfall Ingot",
      "data": { "maxStackSize": 64, "rarity": "common" },
      "runtimeHints": {
        "neoforge": { "itemClass": "dev.echo.echocore.item.AshfallIngotItem" }
      }
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:recipe",
      "id": "echocore:recipe/ashfall_bricks_from_ingots",
      "moduleId": "echocore",
      "displayName": "Ashfall Bricks from Ingots",
      "data": { "type": "crafting_shaped", "category": "building" }
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:mission",
      "id": "echocore:mission/rescue_survivors",
      "moduleId": "echocore",
      "displayName": "Rescue Survivors",
      "description": "Locate and rescue stranded survivors in the Ashfall wastes.",
      "data": { "repeatable": false, "minLevel": 3 }
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:objective",
      "id": "echocore:objective/find_survivor_beacon",
      "moduleId": "echocore",
      "displayName": "Find the Survivor Beacon",
      "data": { "targetCount": 1 }
    },
    {
      "schemaVersion": "echo.content_graph.node.v1",
      "kind": "echo:ui_intent",
      "id": "echocore:ui_intent/mission_terminal",
      "moduleId": "echocore",
      "displayName": "Mission Terminal",
      "intent": "terminal_page",
      "actions": [
        { "id": "open", "label": "Open Mission Terminal" },
        { "id": "track", "label": "Track Active Mission", "requires": "echocore:mission/rescue_survivors" }
      ],
      "fallbacks": {
        "neoforge": "echocore:screen/mission_terminal",
        "echo_native": "native://mission/terminal",
        "hytale": "hytale://ui/mission-terminal"
      }
    }
  ],
  "edges": [
    {
      "schemaVersion": "echo.content_graph.edge.v1",
      "id": "echocore:edge/recipe_consumes_ingot",
      "kind": "recipe_consumes_item",
      "from": "echocore:recipe/ashfall_bricks_from_ingots",
      "to": "echocore:item/ashfall_ingot",
      "moduleId": "echocore",
      "data": { "count": 4 }
    },
    {
      "schemaVersion": "echo.content_graph.edge.v1",
      "id": "echocore:edge/recipe_outputs_bricks",
      "kind": "recipe_outputs_item",
      "from": "echocore:recipe/ashfall_bricks_from_ingots",
      "to": "echocore:block/ashfall_bricks",
      "moduleId": "echocore",
      "data": { "count": 1 }
    },
    {
      "schemaVersion": "echo.content_graph.edge.v1",
      "id": "echocore:edge/mission_has_objective",
      "kind": "mission_has_objective",
      "from": "echocore:mission/rescue_survivors",
      "to": "echocore:objective/find_survivor_beacon",
      "moduleId": "echocore"
    },
    {
      "schemaVersion": "echo.content_graph.edge.v1",
      "id": "echocore:edge/objective_targets_beacon",
      "kind": "objective_targets_node",
      "from": "echocore:objective/find_survivor_beacon",
      "to": "echocore:block/ashfall_bricks",
      "moduleId": "echocore",
      "data": { "interaction": "scan" }
    },
    {
      "schemaVersion": "echo.content_graph.edge.v1",
      "id": "echocore:edge/ui_controls_mission",
      "kind": "ui_intent_controls_node",
      "from": "echocore:ui_intent/mission_terminal",
      "to": "echocore:mission/rescue_survivors",
      "moduleId": "echocore"
    }
  ],
  "unresolvedReferences": [
    {
      "id": "echodeepreach:item/radio",
      "context": "echocore:mission/rescue_survivors rewards",
      "required": false,
      "moduleId": "echocore"
    }
  ]
}
```

## Node Examples

### Block node with runtime-specific classes

```json
{
  "schemaVersion": "echo.content_graph.node.v1",
  "kind": "echo:block",
  "id": "echocore:block/ashfall_bricks",
  "moduleId": "echocore",
  "displayName": "Ashfall Bricks",
  "tags": ["building", "stone"],
  "data": { "hardness": 1.5, "material": "stone" },
  "runtimeHints": {
    "neoforge": { "blockClass": "dev.echo.echocore.block.AshfallBricksBlock" },
    "hytale": { "voxelShape": "cube" }
  }
}
```

### UI intent node

```json
{
  "schemaVersion": "echo.content_graph.node.v1",
  "kind": "echo:ui_intent",
  "id": "echocore:ui_intent/scanner_result",
  "moduleId": "echocore",
  "displayName": "Scanner Result",
  "intent": "scanner_result",
  "actions": [
    { "id": "inspect", "label": "Inspect" },
    { "id": "mark", "label": "Mark on Map" }
  ],
  "fallbacks": {
    "neoforge": "echocore:screen/scanner_result",
    "echo_native": "native://ui/scanner-result",
    "echo_runtime_standalone": "standalone://ui/scanner-result",
    "hytale": "hytale://ui/scanner-result"
  }
}
```

## Edge Examples

Edges are directional. `from` and `to` must reference node `id`s present in the graph.

```json
{
  "schemaVersion": "echo.content_graph.edge.v1",
  "id": "echocore:edge/creative_tab_contains_ingot",
  "kind": "creative_tab_contains_item",
  "from": "echocore:creative_tab/materials",
  "to": "echocore:item/ashfall_ingot",
  "moduleId": "echocore",
  "data": { "order": 12 }
}
```

```json
{
  "schemaVersion": "echo.content_graph.edge.v1",
  "id": "echocore:edge/region_contains_trigger",
  "kind": "region_contains_trigger",
  "from": "echocore:region/ashfall_wastes",
  "to": "echocore:trigger/radiation_pulse",
  "moduleId": "echocore",
  "optional": true
}
```

## Feature List Example

`features.json` is derived from the graph and gives humans a per-runtime readiness summary.

```json
{
  "schemaVersion": "echo.content_feature_list.v1",
  "moduleId": "echocore",
  "generatedAt": "2026-06-14T12:00:00Z",
  "features": [
    {
      "id": "echocore:feature/ashfall_blocks",
      "title": "Ashfall Blocks",
      "description": "Craftable building blocks made from Ashfall ingots.",
      "nodes": ["echocore:block/ashfall_bricks", "echocore:recipe/ashfall_bricks_from_ingots"],
      "runtimes": {
        "neoforge": "supported",
        "echo_native": "supported",
        "echo_runtime_standalone": "supported",
        "hytale": "planned"
      },
      "tags": ["building", "crafting"]
    }
  ]
}
```

## Export Plan Example

An export plan declares how each graph node maps to a target runtime. The Hytale plan below marks one node as adapter-required and another as blocked until a runtime hint is supplied.

```json
{
  "schemaVersion": "echo.content_graph.export_plan.v1",
  "target": "hytale",
  "sourceGraphId": "echocore:content_graph/1.0.0",
  "plannedAt": "2026-06-14T12:00:00Z",
  "nodes": [
    {
      "nodeId": "echocore:block/ashfall_bricks",
      "kind": "echo:block",
      "status": "adapter_required",
      "rationale": "Hytale block adapter maps custom block state.",
      "mappedTo": "hytale:block/custom"
    },
    {
      "nodeId": "echocore:item/ashfall_ingot",
      "kind": "echo:item",
      "status": "direct",
      "rationale": "Item shape maps directly to Hytale item JSON."
    },
    {
      "nodeId": "echocore:entity/waste_stalker",
      "kind": "echo:entity",
      "status": "blocked",
      "rationale": "Hytale entity contract not defined.",
      "contract": "echo.hytale.entity_contract.v1",
      "requiredAdapter": "echo.hytale.entity_adapter.v1",
      "blockedReasonCode": "HYTALE_ACTOR_CONTRACT_MISSING",
      "recommendedFix": "Define echo.hytale.entity_contract.v1 hints or an explicit Hytale fallback for this entity node."
    },
    {
      "nodeId": "echocore:mission/rescue_survivors",
      "kind": "echo:mission",
      "status": "fallback",
      "rationale": "Mission system not available; emit quest JSON instead."
    }
  ],
  "summary": {
    "direct": 1,
    "adapter_required": 1,
    "fallback": 1,
    "blocked": 1,
    "not_applicable": 0
  }
}
```

## Runtime Hints

Portable fields must never contain NeoForge screen classes, block entity classes, registry classes, or Minecraft package names. Put those values inside `runtimeHints.<target>`.

### Allowed

```json
{
  "runtimeHints": {
    "neoforge": { "blockClass": "dev.echo.echocore.block.AshfallBricksBlock" },
    "echo_native": { "bootstrapClass": "dev.echo.echocore.native.EchoCoreBootstrap" },
    "hytale": { "textureSet": "ashfall_bricks" }
  }
}
```

### Forbidden (portable-field pollution)

```json
{
  "data": { "neoforgeScreenClass": "dev.echo.echocore.client.gui.MyScreen" }
}
```

Keep runtime-specific keys in `runtimeHints` so the same graph document can be consumed by every ECHO runtime without leaking implementation details.

## Unresolved References

`unresolvedReferences.json` (and the optional top-level `unresolvedReferences` array) records edges that point outside the module set. This helps authors find missing dependencies before release.

```json
[
  {
    "id": "echodeepreach:item/radio",
    "context": "echocore:mission/rescue_survivors rewards",
    "required": false,
    "moduleId": "echocore"
  }
]
```

## Usage Examples

### Generating a module graph

From `ECHO-Modules`:

```bash
node scripts/generate-content-graph.mjs --all --write
node scripts/validate-content-graph.mjs --strict
```

This writes per-module outputs under `dist/echo-module-release/<module>/<version>/.echo/content-graph/`:

- `content-graph.json` - canonical graph
- `content-graph.md` - human-readable summary
- `features.json` - derived feature list
- `provenance.json` - generation provenance
- `unresolved-references.json` - optional reference audit
- `export-plans/{neoforge,echo_native,echo_runtime_standalone,hytale}.json`

It also writes `dist/echo-module-release/content-graph-evidence.json`, the aggregate release artifact validated by `content-graph-evidence.schema.json`.

### Consuming a graph in a runtime

From `ECHO-Standalone-Runtime`:

```bash
./gradlew runStandaloneContentGraphLoadSmoke -PechoModulesRepoRoot=/path/to/ECHO-Modules
```

The smoke harness loads every `.echo/content-graph/content-graph.json`, maps nodes into runtime registries, and reports diagnostics.

### Indexing a graph artifact

Release-Index `modules/*.json` entries should index a `content-graph` artifact:

```json
{
  "artifacts": {
    "content-graph": {
      "file": "echocore-1.0.0-content-graph.json",
      "sha256": "...",
      "size": 12345,
      "url": "https://github.com/knoxhack/ECHO-Modules/releases/download/.../echocore-1.0.0-content-graph.json",
      "runtimeTarget": "content-graph",
      "buildMode": "generated",
      "contains": [".echo/content-graph/content-graph.json"]
    }
  }
}
```

The Release-Index validator enforces this role for `module` and `addon` entries. When a release-level aggregate is available, Release Index should expose it with role `content-graph-evidence` and file `content-graph-evidence.json`.
