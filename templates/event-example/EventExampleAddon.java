package com.example.eventexample;

import dev.echo.nativeplatform.contracts.EchoNativeLoadStatus;
import dev.echo.nativeplatform.contracts.EchoNativeModuleEntrypoint;
import dev.echo.nativeplatform.contracts.EchoNativeModuleLoadContext;
import dev.echo.nativeplatform.contracts.EchoNativeMutationReceipt;
import dev.echo.nativeplatform.contracts.EchoNativeRuntimeSide;
import dev.echo.nativeplatform.contracts.EchoNativeServiceMutation;

import java.util.Map;

public class EventExampleAddon implements EchoNativeModuleEntrypoint {
    public static final String MODULE_ID = "eventexample";
    public static final String SERVICE_ID = MODULE_ID + ":native_service";

    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        context.registerService(SERVICE_ID, new NativeService(MODULE_ID), "registry", "events");
    }

    @Override
    public void registerContent(EchoNativeModuleLoadContext context) {
        EchoNativeServiceMutation mutation = new EchoNativeServiceMutation(
                MODULE_ID,
                "registry",
                "declare_content",
                MODULE_ID + ":example",
                EchoNativeRuntimeSide.COMMON,
                Map.of("template", "EventExampleAddon")
        );
        context.recordMutation(new EchoNativeMutationReceipt(
                MODULE_ID,
                SERVICE_ID,
                mutation.surface(),
                mutation.action(),
                mutation.target(),
                EchoNativeLoadStatus.MUTATED,
                mutation.side(),
                MODULE_ID + ":registry/example",
                1,
                mutation.evidence()
        ));
    }

    public record NativeService(String moduleId) {
    }
}
