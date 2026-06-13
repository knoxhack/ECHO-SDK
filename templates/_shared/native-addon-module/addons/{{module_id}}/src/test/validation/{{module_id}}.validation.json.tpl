{
  "schema": "echo.validation.v1",
  "moduleId": "{{module_id}}",
  "expectedEntrypoint": "{{package_name}}.{{class_name}}",
  "expectedPackage": "build/echo-native/addons/{{module_id}}-1.0.0-RC1.echo-addon",
  "requiresReleaseModeClasspath": true,
  "forbiddenImports": [
    "dev.echo.nativeplatform.loader",
    "net.neoforged",
    "net.minecraftforge",
    "net.fabricmc"
  ]
}
