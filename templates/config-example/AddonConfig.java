package com.example.configexample;

public class AddonConfig {
    public int maxItems = 64;
    public boolean enableDebug = false;

    public static AddonConfig load(String modid) {
        // In production, load from config/<modid>.toml or datapack
        return new AddonConfig();
    }
}
