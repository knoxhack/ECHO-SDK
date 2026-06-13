plugins {
    id 'java-library'
    id 'maven-publish'
    id 'dev.echo.native.echo-sdk-gradle-plugin' version '1.0.0-RC1'
}

version = mod_version
group = mod_group_id

repositories {
    mavenLocal()
    maven { url 'https://maven.echo.dev/rc' }
    mavenCentral()
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
    withSourcesJar()
    withJavadocJar()
}

dependencies {
    compileOnly 'dev.echo.native:echoaddonapi:1.0.0-RC1'
    compileOnly 'dev.echo.native:echoadaptercore:1.0.0-RC1'
    compileOnly 'dev.echo.native:echo-native-contracts:1.0.0-RC1'
    testImplementation 'dev.echo.native:echo-native-testkit:1.0.0-RC1'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

test {
    useJUnitPlatform()
}

tasks.register('verifyNativeAddonBoundaries') {
    group = 'verification'
    description = 'Fails when a Native-first addon imports loader internals or direct mod-loader APIs.'
    def sources = fileTree('src/main/java') {
        include '**/*.java'
    }
    inputs.files(sources)
    doLast {
        def forbidden = [
                'dev.echo.nativeplatform.loader',
                'net.neoforged',
                'net.minecraftforge',
                'net.fabricmc'
        ]
        def offenders = sources.files.findAll { file ->
            def text = file.getText('UTF-8')
            forbidden.any { marker -> text.contains(marker) }
        }
        if (!offenders.empty) {
            throw new GradleException("Native-first addons must use the public ECHO SDK only: ${offenders*.path}")
        }
    }
}

tasks.register('validateNativeDescriptor') {
    group = 'verification'
    description = 'Validates the minimum Native addon descriptor fields before packaging.'
    def descriptorFile = file('src/main/resources/META-INF/echo.mod.json')
    inputs.file(descriptorFile)
    doLast {
        def descriptor = new groovy.json.JsonSlurper().parse(descriptorFile)
        if (descriptor.schema != 'echo.mod.v1') {
            throw new GradleException('echo.mod.json schema must be echo.mod.v1')
        }
        if (descriptor.id != mod_id) {
            throw new GradleException("echo.mod.json id must match mod_id=${mod_id}")
        }
        if (!descriptor.entrypoint) {
            throw new GradleException('echo.mod.json must declare entrypoint')
        }
        if (!descriptor.access?.nativeClasspath?.contains('addon.jar')) {
            throw new GradleException('echo.mod.json access.nativeClasspath must include addon.jar for release-mode loading')
        }
    }
}

tasks.named('check') {
    dependsOn tasks.named('verifyNativeAddonBoundaries')
    dependsOn tasks.named('validateNativeDescriptor')
}

tasks.register('packageEchoNativeAddon', Zip) {
    group = 'distribution'
    description = 'Packages this project as a release-mode .echo-addon.'
    dependsOn tasks.named('jar')
    dependsOn tasks.named('validateNativeDescriptor')
    archiveFileName = "${mod_id}-${mod_version}.echo-addon"
    destinationDirectory = layout.buildDirectory.dir('echo-native/addons')
    from('src/main/resources/META-INF/echo.mod.json')
    from(tasks.named('jar').flatMap { it.archiveFile }) {
        rename { 'addon.jar' }
    }
}

tasks.register('packageAddon') {
    group = 'distribution'
    description = 'Compatibility alias for packageEchoNativeAddon.'
    dependsOn tasks.named('packageEchoNativeAddon')
}

publishing {
    publications {
        register('mavenJava', MavenPublication) {
            from components.java
        }
    }
}
