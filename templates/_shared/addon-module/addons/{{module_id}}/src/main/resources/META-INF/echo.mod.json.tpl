{
  "schema": "echo.mod.v1",
  "id": "{{module_id}}",
  "name": "{{mod_name}}",
  "version": "1.0.0",
  "type": "addon",
  "kind": "{{kind}}",
  "role": "{{role}}",
  "entrypoint": "{{package_name}}.{{class_name}}",
  "publisher": "KnoxHack",
  "channel": "beta",
  "official": false,
  "trustLevel": "local",
  "standalone": true,
  "clientOnly": false,
  "serverOnly": false,
  "side": "common",
  "requires": [
    "echocore"
  ],
  "optional": [],
  "provides": [
    "{{feature_id}}"
  ],
  "consumes": [
    "echo.core"
  ],
  "gameModes": [
    "ashfall",
    "echo_prime",
    "arcana_division"
  ],
  "permissions": [
    "{{feature_id}}"
  ],
  "assets": [],
  "transforms": [],
  "access": {
    "requiresConfirmationForWriteActions": true
  },
  "apiStability": "experimental",
  "ai": {
    "requiresHumanReview": false,
    "recommendedAgentLanes": [
      "architect_agent",
      "diagnostics_agent"
    ]
  },
  "deprecatedFeatures": [],
  "replacements": [],
  "conflicts": []
}
