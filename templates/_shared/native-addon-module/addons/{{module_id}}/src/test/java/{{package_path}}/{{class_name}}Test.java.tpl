package {{package_name}};

import dev.echo.nativeplatform.contracts.EchoNativeModuleLoadContext;
import dev.echo.nativeplatform.testkit.EchoNativeSdkTestkit;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertTrue;

public final class {{class_name}}Test {
    @Test
    void registersThroughTypedRegistryService() {
        EchoNativeSdkTestkit.Environment env = EchoNativeSdkTestkit.common({{class_name}}.MODULE_ID);
        EchoNativeModuleLoadContext context = new EchoNativeModuleLoadContext(
                env.moduleFixture("{{package_name}}.{{class_name}}").moduleDescriptor(),
                env.serviceRegistry(),
                Map.of()
        );

        {{class_name}} addon = new {{class_name}}();
        addon.registerServices(context);
        addon.registerContent(context);

        assertTrue(context.serviceRegistry().hasService({{class_name}}.SERVICE_ID));
        assertTrue(context.mutationReceipts().stream()
                .anyMatch(receipt -> receipt.mutated() && "echo.native.registry".equals(receipt.serviceId())));
        env.goldenParity().requireMutatedServices("echo.native.registry");
        env.goldenParity().requireOnlyTypedReceipts();
    }
}
