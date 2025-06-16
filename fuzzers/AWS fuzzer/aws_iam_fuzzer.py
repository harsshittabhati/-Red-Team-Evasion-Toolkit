# aws_iam_fuzzer.py
import boto3
from botocore.exceptions import ClientError

def attempt_action(service, action):
    try:
        client = boto3.client(service)
        method = getattr(client, action)
        print(f"[+] Trying {service}.{action}()")
        response = method()
        print(f"[✓] Success: {response}\n")
    except AttributeError:
        print(f"[!] Method {action} not found in {service}")
    except ClientError as e:
        print(f"[x] Denied: {service}.{action}() → {e.response['Error']['Code']}")

# Commonly fuzzed services and actions
target_services = {
    "iam": ["list_users", "list_roles", "list_policies", "get_user"],
    "ec2": ["describe_instances", "describe_security_groups"],
    "s3": ["list_buckets"],
    "sts": ["get_caller_identity"]
}

for service, actions in target_services.items():
    for action in actions:
        attempt_action(service, action)
