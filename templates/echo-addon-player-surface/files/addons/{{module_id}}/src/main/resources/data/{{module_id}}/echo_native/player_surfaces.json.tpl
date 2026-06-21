{
  "schemaVersion": "echo.native.player_surface_manifest.v1",
  "ownerModule": "{{module_id}}",
  "requiredHostServices": [
    "echo.native.screens",
    "echo.input.bindings"
  ],
  "hostTargets": [
    "neoforge",
    "echo_native",
    "echo_runtime_standalone",
    "standalone_engine"
  ],
  "surfaces": [
    {
      "id": "{{module_id}}:surface/{{feature_id}}",
      "title": "{{display_name}}",
      "intent": "modal",
      "surface": "screen",
      "contract": "echo.ui.surface.v1",
      "requiredHostServices": [
        "echo.native.screens",
        "echo.input.bindings"
      ],
      "capabilities": [
        "screen",
        "modal"
      ],
      "themeTokens": [
        "echothemecore:token/default_surface"
      ],
      "inputBindings": [
        "echoinputcore:binding/menu_confirm"
      ],
      "actions": [
        {
          "id": "close",
          "label": "Close",
          "action": "{{module_id}}:action/{{feature_id}}/close"
        }
      ],
      "controlledNodes": [
        "{{module_id}}:module"
      ],
      "fallbacks": {
        "neoforge": "{{module_id}}:screen/{{feature_id}}",
        "echo_native": "native://screen/{{feature_id}}",
        "echo_runtime_standalone": "standalone://screen/{{feature_id}}",
        "standalone_engine": "engine://screen/{{feature_id}}"
      }
    }
  ]
}
