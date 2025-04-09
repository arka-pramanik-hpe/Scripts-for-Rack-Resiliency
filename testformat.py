import textwrap

def pretty_print_error(error_message):
    try:
        # Convert escape sequences (like \n and \t) to their actual characters.
        unescaped_message = error_message.encode('utf-8').decode('unicode_escape')
    except Exception:
        unescaped_message = error_message

    # Wrap each line to 100 characters for readability.
    wrapped_lines = [textwrap.fill(line, width=100) for line in unescaped_message.splitlines()]
    return "\n".join(wrapped_lines)

# Example usage:
error_example = "(403)\\nReason: Forbidden\\nHTTP response headers: HTTPHeaderDict({'Audit-Id': '9c47dee6-ab74-44d7-a3a5-6af3c644849f', 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'X-Content-Type-Options': 'nosniff', 'X-Kubernetes-Pf-Flowschema-Uid': 'c9c274fb-d31f-4569-8323-27135dfaf780', 'X-Kubernetes-Pf-Prioritylevel-Uid': '2ff1e87a-7e06-4d2d-9cb1-e6f403199d8d', 'Date': 'Thu, 20 Mar 2025 06:47:16 GMT', 'Content-Length': '354'})\\nHTTP response body: {\"kind\":\"Status\",\"apiVersion\":\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"configmaps \\\"rrs-map\\\" is forbidden: User \\\"system:serviceaccount:rack-resiliency:k8s-zone-reader\\\" cannot patch resource \\\"configmaps\\\" in API group \\\"\\\" in the namespace \\\"rack-resiliency\\\"\",\"reason\":\"Forbidden\",\"details\":{\"name\":\"rrs-map\",\"kind\":\"configmaps\"},\"code\":403}\\n\\n"
print(simple_pretty_print(error_example))
