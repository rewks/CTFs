from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secrets import randbelow
from hashlib import sha256
import os, json, requests

class MyClient:
    def __init__(self, g, p):
        self.g = int(g, 16) 
        self.p = int(p, 16)
        self.compute_public_key()

    def compute_public_key(self):
        self.a = randbelow(self.p)
        self.public_key = pow(self.g, self.a, self.p)

    def establish_session_key(self, server_public_key):
        key = pow(server_public_key, self.a, self.p)
        self.session_key = sha256(str(key).encode()).digest()

    def encrypt_packet(self, packet):
        iv = os.urandom(16)
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        encrypted_packet = iv + cipher.encrypt(pad(packet.encode(), 16))
        return {'packet_data': b64encode(encrypted_packet).decode()}

    def decrypt_packet(self, packet):
        decoded_packet = b64decode(packet.encode())
        iv = decoded_packet[:16]
        encrypted_packet = decoded_packet[16:]
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        try:
            decrypted_packet = unpad(cipher.decrypt(encrypted_packet), 16)
            packet_data = decrypted_packet.decode()
        except:
            return {'error': 'Malformed packet.'}

        return {'packet_data': packet_data}

    def get_decrypted_challenge(self, challenge_packet):
        decoded_packet = b64decode(challenge_packet)
        iv = decoded_packet[:16]
        ciphertext = decoded_packet[16:]
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        challenge = unpad(plaintext, 16)
        return challenge

url = 'http://94.237.54.201:41779'

# Step 1
r = requests.post(f'{url}/api/request-session-parameters')
resp = json.loads(r.text)
client = MyClient(resp['g'], resp['p'])

# Step 2 
data = { 'client_public_key': client.public_key }
headers = { 'Content-Type': 'application/json' }
r = requests.post(f'{url}/api/init-session', data=json.dumps(data), headers=headers)
resp = json.loads(r.text)
client.establish_session_key(int(resp['server_public_key'], 16))

# Step 3 
r = requests.post(f'{url}/api/request-challenge')
resp = json.loads(r.text)
encrypted_challenge = resp['encrypted_challenge']
challenge = sha256(client.get_decrypted_challenge(encrypted_challenge)).hexdigest()

# Step 4
data = client.encrypt_packet('flag')
data['challenge'] = challenge
headers = { 'Content-Type': 'application/json' }
r = requests.post(f'{url}/api/dashboard', data=json.dumps(data), headers=headers)
resp = json.loads(r.text)
flag = client.decrypt_packet(resp['packet_data'])
print(flag)
