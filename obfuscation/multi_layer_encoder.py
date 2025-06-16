import base64
import argparse

def xor_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def encode_multi_layer(filepath, key='RedTeam123'):
    with open(filepath, 'r') as f:
        original = f.read()
    
    xor_encoded = xor_encrypt(original, key)
    base64_encoded = base64.b64encode(xor_encoded.encode()).decode()

    return base64_encoded

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-layer obfuscation encoder")
    parser.add_argument("input", help="Input PowerShell script")
    parser.add_argument("output", help="Output obfuscated file")
    parser.add_argument("--key", help="XOR key (default: RedTeam123)", default="RedTeam123")

    args = parser.parse_args()

    obfuscated = encode_multi_layer(args.input, args.key)
    with open(args.output, 'w') as f:
        f.write(obfuscated)

    print(f"[+] Obfuscated payload written to {args.output}")
