package dev.echo.gradle;

import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.provider.Property;

public abstract class EchoSdkExtension {
    public abstract Property<String> getAddonId();

    public abstract Property<String> getPythonExecutable();

    public abstract RegularFileProperty getToolScript();

    public abstract RegularFileProperty getApiJar();
}
