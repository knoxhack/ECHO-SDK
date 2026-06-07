package {{package_name}}.examples;

public final class {{class_name}}Parity {
    private {{class_name}}Parity() {
    }

    public static boolean hasMutationReceipt(String receipt) {
        return receipt != null && receipt.startsWith("{{module_id}}:");
    }

    public static String parityReportId() {
        return "{{module_id}}:parity/native-sdk";
    }
}
