{
  "schemaVersion": "echo.pack.v1",
  "id": "{{pack_id}}",
  "name": "{{display_name}}",
  "publisher": "KnoxHack",
  "type": "{{kind}}",
  "status": "planned",
  "rootModule": "{{module_id}}",
  "gameMode": "{{pack_id}}_survival",
  "worldProfile": "{{pack_id}}_world",
  "startProfile": "{{pack_id}}_start",
  "theme": "{{pack_id}}_theme",
  "releaseChannel": "dev-local",
  "strictOfficialOnly": true,
  "minecraftVersion": "26.1.2",
  "loader": {
    "kind": "neoforge",
    "version": "26.1.2.29-beta"
  },
  "variants": [
    "standard",
    "performance",
    "cinematic",
    "server",
    "creator",
    "dev"
  ],
  "channels": [
    "stable",
    "beta",
    "alpha",
    "nightly",
    "dev-local",
    "experimental"
  ],
  "requiredModules": [
    "echocore",
    "{{module_id}}"
  ],
  "optionalModules": [],
  "requiredFeatures": [
    "echo.core",
    "{{feature_id}}"
  ],
  "optionalFeatures": []
}
