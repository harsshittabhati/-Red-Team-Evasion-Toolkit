# Red-Team-Evasion-Toolkit
This repository contains professionally engineered evasion scripts and implants used in autonomous red team operations across hybrid cloud environments. All tools are mapped to MITRE ATT&amp;CK tactics and are designed for stealth, persistence, and C2 evasion.

## 📦 Components

### 1. rust_c2/
> Custom Command & Control written in Rust (encrypted beacons)
- **main.rs**: Skeleton client that encrypts a JSON heartbeat with AES and sends via HTTPS.
- **Cargo.toml**: Dependencies (`openssl`, `reqwest`, `serde_json`).

### 2. empire_scripts/
> PowerShell Empire scripts for DNS-over-HTTPS (DoH) exfiltration.
- **dns_over_https.ps1**: Chunks and exfiltrates file data via Cloudflare DoH.
- **README.md**: Usage instructions and integration with Empire GUI.

### 3. obfuscation/
> Scripts to obfuscate payloads and evade EDR.
- **powershell_base64_encoded.ps1**: Base64 encodes a script payload.
- **multi_layer_encoder.py**: Wraps payload in multiple encoding layers.

### 4. persistence/
> Windows persistence mechanisms.
- **win_persistence.ps1**: Creates registry autorun entries and scheduled tasks silently.

## 🗒️ Getting Started
1. **Clone** the repo
2. **Inspect** each folder’s README
3. **Run** tests in a secure, isolated lab

## ⚠️ Disclaimer
This toolkit is strictly for **Educational & Authorized** use in controlled environments. Unauthorized use is prohibited.
