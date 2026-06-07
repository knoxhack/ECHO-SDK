package {{package_name}}.examples;

public final class {{class_name}}Keys {
    public static final String BIOME_MODIFIER = "{{module_id}}:biome_modifier/main";
    public static final String PLACED_FEATURE = "{{module_id}}:placed_feature/main";

    private {{class_name}}Keys() {
    }

    public static String worldgenReceipt(String key) {
        return "{{module_id}}:worldgen/" + key;
    }
}
