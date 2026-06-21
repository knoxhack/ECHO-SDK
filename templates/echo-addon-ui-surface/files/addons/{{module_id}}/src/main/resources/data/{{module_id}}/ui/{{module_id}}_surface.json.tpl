{
  "schemaVersion": "echo.ui.surface.v1",
  "id": "{{module_id}}:surface/{{feature_id}}",
  "ownerModule": "{{module_id}}",
  "kind": "modal",
  "layoutId": "{{module_id}}:layout/{{feature_id}}",
  "themeTokens": [
    "echothemecore:token/default_surface"
  ],
  "requiredHostServices": [
    "echo.native.screens",
    "echo.input.bindings"
  ],
  "actions": [
    {
      "id": "close",
      "label": "Close",
      "action": "{{module_id}}:action/{{feature_id}}/close"
    }
  ],
  "dataProviders": [
    "{{module_id}}:provider/{{feature_id}}"
  ],
  "fallbackPolicy": {
    "defaultStatus": "blocked",
    "reason": "Player-facing UI must be implemented by an ECHO Native host adapter before release."
  }
}

