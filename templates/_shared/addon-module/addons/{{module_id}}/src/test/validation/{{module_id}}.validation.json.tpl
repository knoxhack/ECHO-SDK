{
  "schema": "echo.sdk.validation.v1",
  "module": "{{module_id}}",
  "template": "{{template_id}}",
  "checks": [
    {
      "id": "metadata_present",
      "kind": "file_exists",
      "path": "src/main/resources/META-INF/echo.mod.json"
    },
    {
      "id": "ai_metadata_present",
      "kind": "file_exists",
      "path": "src/main/resources/META-INF/echo.ai.json"
    },
    {
      "id": "safe_edit_zones_present",
      "kind": "metadata_field_present",
      "path": "src/main/resources/META-INF/echo.ai.json",
      "field": "safeEditZones"
    },
    {
      "id": "feature_declared",
      "kind": "metadata_field_contains",
      "path": "src/main/resources/META-INF/echo.mod.json",
      "field": "provides",
      "value": "{{feature_id}}"
    }
  ]
}
