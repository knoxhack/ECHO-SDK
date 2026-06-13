pluginManagement {
    repositories {
        mavenLocal()
        maven { url = uri('https://maven.echo.dev/rc') }
        gradlePluginPortal()
        mavenCentral()
    }
}

rootProject.name = '{{module_id}}'
