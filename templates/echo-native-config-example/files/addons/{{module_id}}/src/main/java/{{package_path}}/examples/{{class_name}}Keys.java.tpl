package {{package_name}}.examples;

public final class {{class_name}}Keys {
    public static final String CONFIG_SCOPE = "{{module_id}}.common";
    public static final String ENABLED = CONFIG_SCOPE + ".enabled";

    private {{class_name}}Keys() {
    }

    public static String configReceipt() {
        return "{{module_id}}:config/" + CONFIG_SCOPE;
    }
}
