package {{package_name}}.examples;

public final class {{class_name}}NativeModuleContract {
    private {{class_name}}NativeModuleContract() {
    }

    public static String providedFeature() {
        return "{{feature_id}}";
    }

    public static String moduleHealthKey() {
        return "{{module_id}}:health/native-module";
    }
}
