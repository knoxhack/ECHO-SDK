{
  "schema": "echo.mod.v1",
  "id": "{{module_id}}",
  "name": "{{mod_name}}",
  "version": "1.0.0-RC1",
  "type": "addon",
  "kind": "{{kind}}",
  "role": "{{role}}",
  "entrypoint": "{{package_name}}.{{class_name}}",
  "publisher": "local",
  "channel": "rc",
  "official": false,
  "trustLevel": "local",
  "standalone": true,
  "clientOnly": false,
  "serverOnly": false,
  "side": "common",
  "requires": [],
  "optional": [],
  "provides": [
    "{{feature_id}}"
  ],
  "consumes": [],
  "gameModes": [],
  "permissions": [
    "{{feature_id}}"
  ],
  "assets": [],
  "transforms": [],
  "access": {
    "nativeClasspath": [
      "addon.jar"
    ],
    "requiresConfirmationForWriteActions": true
  },
  "apiStability": "beta",
  "ai": {
    "requiresHumanReview": false,
    "recommendedAgentLanes": [
      "architect_agent",
      "diagnostics_agent",
      "release_agent"
    ]
  },
  "deprecatedFeatures": [],
  "replacements": [],
  "conflicts": []
}
