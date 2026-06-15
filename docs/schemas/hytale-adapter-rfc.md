# Hytale Adapter RFC

Status: planning-only.

The `.ECHO Content Graph` can describe Hytale export readiness, but no UI, release gate, or runtime may claim Hytale playable/runtime support from `direct`, `adapter_required`, `fallback`, or `blocked` evidence alone.

Before Hytale status can become runtime-supported, the platform needs:

1. A named target API source, including version, license assumptions, and the authoritative schema/API location.
2. A supported node-kind matrix for every `echo:*` node kind that can map to Hytale.
3. A codegen or adapter output contract, including repository path, generated file layout, and package/install expectations.
4. Blocker reduction criteria that define when `blocked` evidence can be removed from module export plans.
5. A separate runtime validation gate that loads or executes the generated Hytale adapter outputs.

Until those items exist, `export-plans/hytale.json` and `content-graph-evidence.json` are planning and diagnostics artifacts only.
