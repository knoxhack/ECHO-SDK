package dev.echo.gradle;

import java.util.LinkedHashMap;
import java.util.Map;
import org.gradle.api.Plugin;
import org.gradle.api.Project;
import org.gradle.api.provider.Provider;

public final class EchoSdkPlugin implements Plugin<Project> {
    @Override
    public void apply(Project project) {
        EchoSdkExtension extension = project.getExtensions().create("echoSdk", EchoSdkExtension.class);
        extension.getAddonId().convention("myaddon");
        extension.getPythonExecutable().convention("python");
        extension.getToolScript().convention(project.getLayout().getProjectDirectory().file("tools/echo_addon_sdk_flow.py"));

        Map<String, String> operations = new LinkedHashMap<>();
        operations.put("echoInitAddon", "init-addon");
        operations.put("echoValidateManifest", "validate-manifest");
        operations.put("echoValidateSchemas", "validate-schemas");
        operations.put("echoValidateImports", "validate-imports");
        operations.put("echoValidatePermissions", "validate-permissions");
        operations.put("echoValidateRuntimeTargets", "validate-runtime-targets");
        operations.put("echoValidate", "validate");
        operations.put("echoGenerateAdapters", "generate-adapters");
        operations.put("echoGenerateNeoForgeEntrypoint", "generate-neoforge-entrypoint");
        operations.put("echoGenerateNativeDescriptor", "generate-native-descriptor");
        operations.put("echoGenerateStandaloneHarness", "generate-standalone-harness");
        operations.put("echoPackageNativeAddon", "package-native-addon");
        operations.put("echoPackageNeoForge", "package-neoforge");
        operations.put("echoPackageStandalone", "package-standalone");
        operations.put("echoParityTest", "parity-test");
        operations.put("echoBuildReleaseBundle", "build-release-bundle");
        operations.put("echoPackageSdk", "package-sdk");
        operations.put("echoVerifyNativeLiveProof", "verify-native-live-proof");
        operations.put("echoGenerateLaneReadiness", "generate-lane-readiness");

        operations.forEach((taskName, operation) -> registerSdkTask(project, extension, taskName, operation));
    }

    private static void registerSdkTask(Project project, EchoSdkExtension extension, String taskName, String operation) {
        Provider<String> description = project.provider(() -> "Runs the ECHO SDK " + operation.replace('-', ' ') + " step.");
        project.getTasks().register(taskName, EchoSdkTask.class, task -> {
            task.setGroup("echo sdk");
            task.setDescription(description.get());
            task.getOperation().convention(operation);
            task.getAddonId().convention(extension.getAddonId());
            task.getPythonExecutable().convention(extension.getPythonExecutable());
            task.getToolScript().convention(extension.getToolScript());
            task.getApiJar().convention(extension.getApiJar());
        });
    }
}
