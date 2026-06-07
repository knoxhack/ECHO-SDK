package dev.echo.gradle;

import java.util.ArrayList;
import java.util.List;
import javax.inject.Inject;
import org.gradle.api.DefaultTask;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.provider.Property;
import org.gradle.api.tasks.Input;
import org.gradle.api.tasks.InputFile;
import org.gradle.api.tasks.Optional;
import org.gradle.api.tasks.TaskAction;
import org.gradle.api.tasks.options.Option;
import org.gradle.process.ExecOperations;

public abstract class EchoSdkTask extends DefaultTask {
    @Input
    public abstract Property<String> getOperation();

    @Input
    public abstract Property<String> getAddonId();

    @Input
    public abstract Property<String> getPythonExecutable();

    @InputFile
    public abstract RegularFileProperty getToolScript();

    @Optional
    @InputFile
    public abstract RegularFileProperty getApiJar();

    @Inject
    public abstract ExecOperations getExecOperations();

    @Option(option = "id", description = "ECHO add-on module id.")
    public void setId(String id) {
        getAddonId().set(id);
    }

    @TaskAction
    public void runSdkOperation() {
        List<String> args = new ArrayList<>();
        args.add(getPythonExecutable().get());
        args.add(getToolScript().get().getAsFile().getAbsolutePath());
        args.add(getOperation().get());
        args.add("--id");
        args.add(getAddonId().get());
        if (getApiJar().isPresent()) {
            args.add("--api-jar");
            args.add(getApiJar().get().getAsFile().getAbsolutePath());
        }
        getExecOperations().exec(spec -> {
            spec.setWorkingDir(getProject().getProjectDir());
            spec.commandLine(args);
        });
    }
}
