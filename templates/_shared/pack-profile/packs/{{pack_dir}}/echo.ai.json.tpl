{
  "schema": {
    "id": "echo.ai",
    "version": "1",
    "kind": "echo_ai_metadata"
  },
  "module": "{{pack_id}}",
  "summary": "{{display_name}} pack profile generated from the ECHO SDK pack template.",
  "owners": [
    {
      "name": "KnoxHack",
      "role": "pack owner",
      "areas": [
        "pack profile",
        "pack readiness"
      ]
    }
  ],
  "importantPackages": [],
  "mainClasses": [],
  "commonTasks": [
    {
      "id": "validate_pack_profile",
      "label": "Validate pack profile",
      "summary": "Run the PackOS profile loader and readiness reports before using this pack profile.",
      "suggestedLanes": [
        "packaging_agent",
        "diagnostics_agent"
      ],
      "acceptanceHints": [
        "pack_profile_valid",
        "readiness_generated"
      ]
    }
  ],
  "doNotEdit": [
    "user saves",
    "managed install targets"
  ],
  "protectedFiles": [
    "saves/**",
    "mods/**"
  ],
  "safeEditZones": [
    "packs/{{pack_dir}}/**",
    "docs/**"
  ],
  "requiresHumanReview": true,
  "testCommands": [
    ".\\gradlew loadEchoPackProfile -PechoPack={{pack_id}}"
  ],
  "buildCommands": [
    ".\\gradlew generateEchoPackReadiness -PechoPack={{pack_id}} -PechoAddonSet=beta"
  ],
  "recommendedAgentLanes": [
    "packaging_agent",
    "diagnostics_agent"
  ],
  "knownScreens": [],
  "knownRegistries": [],
  "commonDiagnostics": [],
  "promptHints": [
    "Keep generated pack profiles planned until required modules and features exist.",
    "Do not add fake asset paths or fake lockfile success."
  ]
}
