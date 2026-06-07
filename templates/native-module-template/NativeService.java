package com.example.mynativemodule;

import dev.echo.api.registry.EchoRegistryRegistrar;

public class NativeService {
    private final EchoRegistryRegistrar registrar;

    public NativeService(EchoRegistryRegistrar registrar) {
        this.registrar = registrar;
    }

    public EchoRegistryRegistrar getRegistrar() {
        return registrar;
    }
}
