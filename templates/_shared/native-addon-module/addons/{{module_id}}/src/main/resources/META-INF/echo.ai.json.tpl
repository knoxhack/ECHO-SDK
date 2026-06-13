{
  "schema": "echo.ai.v1",
  "module": "{{module_id}}",
  "safeEditZones": [
    "src/main/java/**",
    "src/main/resources/**",
    "docs/**",
    "README.md"
  ],
  "protectedFiles": [
    "build/**",
    "managed installs",
    "user saves"
  ],
  "recommendedAgentLanes": [
    "architect_agent",
    "runtime_agent",
    "test_agent",
    "release_agent"
  ]
}
