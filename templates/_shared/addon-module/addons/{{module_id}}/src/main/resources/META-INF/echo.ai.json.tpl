{
  "schema": {
    "id": "echo.ai",
    "version": "1",
    "kind": "echo_ai_metadata"
  },
  "module": "{{module_id}}",
  "summary": "{{mod_name}} generated from the {{template_name}} SDK template.",
  "owners": [
    {
      "name": "KnoxHack",
      "role": "platform owner",
      "areas": [
        "{{role}}",
        "{{feature_id}}"
      ]
    }
  ],
  "importantPackages": [
    "{{package_name}}"
  ],
  "mainClasses": [
    "{{class_name}}"
  ],
  "commonTasks": [
    {
      "id": "validate_{{module_id}}",
      "label": "Validate {{mod_name}}",
      "summary": "Check metadata, compile behavior, and Native-ready boundaries for {{module_id}}.",
      "suggestedLanes": [
        "architect_agent",
        "diagnostics_agent"
      ],
      "acceptanceHints": [
        "metadata_valid",
        "scan_visible",
        "build_attempted"
      ]
    }
  ],
  "doNotEdit": [
    "generated resources",
    "user save data",
    "managed install targets"
  ],
  "protectedFiles": [
    "addons/{{module_id}}/src/generated/**",
    "addons/{{module_id}}/src/main/resources/data/**/player/**"
  ],
  "safeEditZones": [
    "src/main/java/**",
    "src/main/resources/assets/{{module_id}}/**",
    "docs/**",
    "README.md"
  ],
  "requiresHumanReview": false,
  "testCommands": [
    ".\\gradlew :{{module_id}}:compileJava -PechoAddonSet=beta"
  ],
  "buildCommands": [
    ".\\gradlew build -PechoAddonSet=beta"
  ],
  "recommendedAgentLanes": [
    "architect_agent",
    "diagnostics_agent"
  ],
  "knownScreens": [],
  "knownRegistries": [
    "{{feature_id}}"
  ],
  "commonDiagnostics": [
    {
      "code": "ECHO-SDK-METADATA-VERIFY",
      "severity": "NOTICE",
      "category": "module_manifest",
      "summary": "Generated module metadata should be reviewed before promotion to official packs.",
      "usualFix": "Run validateEchoSdkTemplates, scanEchoWorkspace, and generateEchoModuleGraph before wiring the module into a pack."
    }
  ],
  "promptHints": [
    "Keep generated SDK modules local-only until reviewed.",
    "Do not edit settings.gradle unless the operator explicitly requests workspace registration.",
    "Preserve common/server safety unless this template is intentionally extended with isolated client code."
  ]
}
