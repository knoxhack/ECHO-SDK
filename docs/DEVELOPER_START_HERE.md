# Developer Start Here

External mods should integrate through ECHO Core services and optional integration checks. Avoid direct hard references to optional addons unless your module declares them as required.

Use [API Index](api/index.md), [Optional Integrations](api/optional_integrations.md), and [Integration Examples](examples/integrations/index.md).

Stability labels:
- Stable: safe for external integrations.
- Beta: usable, but minor shape changes may happen before full API freeze.
- Experimental: creator/testing surface.
- Internal: do not rely on it externally.
