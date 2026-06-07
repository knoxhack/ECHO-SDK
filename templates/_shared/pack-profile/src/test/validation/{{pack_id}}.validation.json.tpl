{
  "schema": "echo.sdk.validation.v1",
  "packId": "{{pack_id}}",
  "template": "{{template_id}}",
  "checks": [
    {
      "id": "pack_profile_present",
      "kind": "file_exists",
      "path": "packs/{{pack_dir}}/echo.pack.json"
    },
    {
      "id": "pack_profile_has_root",
      "kind": "metadata_field_present",
      "path": "packs/{{pack_dir}}/echo.pack.json",
      "field": "rootModule"
    }
  ]
}
