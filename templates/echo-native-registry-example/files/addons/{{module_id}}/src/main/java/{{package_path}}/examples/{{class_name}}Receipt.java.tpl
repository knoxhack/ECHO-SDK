package {{package_name}}.examples;

public final class {{class_name}}Receipt {
    private {{class_name}}Receipt() {
    }

    public static String contentId(String name) {
        return "{{module_id}}:" + name;
    }

    public static String mutationReceipt(String contentId) {
        return "{{module_id}}:registry/" + contentId;
    }
}
