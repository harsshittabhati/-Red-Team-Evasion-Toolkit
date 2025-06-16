
# Rust C2 Client

This is a prototype of a Rust-based C2 client that:
- 📡 Secure HTTPS communication
- 🔐 AES-GCM encryption and base64 encoding
- 💻 Remote command execution
- 🧠 Anti-analysis checks
- 🧾 Encrypted beaconing + response handling

### Requirements
- Rust 1.56+
- `openssl` library

### Build
```bash
cd rust_c2/client
cargo build --release
```

### Usage
```bash
RUST_BACKTRACE=1 ./target/release/client
```
Then from another terminal:
```
Example:
curl -k -X POST https://127.0.0.1:5000/send -d 'whoami'
```
