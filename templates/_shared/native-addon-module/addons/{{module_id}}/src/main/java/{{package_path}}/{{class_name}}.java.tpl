package {{package_name}};

import dev.echo.nativeplatform.contracts.EchoNativeModuleEntrypoint;
import dev.echo.nativeplatform.contracts.EchoNativeModuleLoadContext;
import dev.echo.nativeplatform.contracts.EchoNativeRegistryService;
import dev.echo.nativeplatform.contracts.EchoNativeRuntimeSide;
import dev.echo.nativeplatform.contracts.EchoNativeServiceMutation;

import java.util.Map;

public final class {{class_name}} implements EchoNativeModuleEntrypoint {
    public static final String MODULE_ID = "{{module_id}}";
    public static final String SERVICE_ID = MODULE_ID + ".sdk.service";
    public static final String FEATURE_ID = "{{feature_id}}";

    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        context.registerService(SERVICE_ID, new NativeSdkService(MODULE_ID, FEATURE_ID), "registry", "events");
    }

    @Override
    public void registerContent(EchoNativeModuleLoadContext context) {
        EchoNativeServiceMutation mutation = new EchoNativeServiceMutation(
                MODULE_ID,
                "registry",
                "declare_content",
                MODULE_ID + ":example",
                EchoNativeRuntimeSide.COMMON,
                Map.of("featureId", FEATURE_ID)
        );
        context.serviceRegistry()
                .service("echo.native.registry", EchoNativeRegistryService.class)
                .map(registry -> registry.register(mutation))
                .ifPresent(context::recordMutation);
    }

    public record NativeSdkService(String moduleId, String featureId) {
    }
}
