import struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import os

# Network Framing
def send_blob(sock, data: bytes):
    """Safe sending of length-prefixed data"""
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)

def recv_blob(sock) -> bytes:
    """Safe receiving of length-prefixed data"""
    def recv_exact(n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Connection closed prematurely")
            data += packet
        return data
    
    length_bytes = recv_exact(4)
    length = struct.unpack('>I', length_bytes)[0]
    if length > 10 * 1024 * 1024:  # 10MB max
        raise ValueError("Message too large")
    return recv_exact(length)

# Cryptography
class CryptoHandler:
    def __init__(self):
        self.private_key, self.public_key = self._generate_rsa_keys()
        self.des_key = self._generate_des_key()

    @staticmethod
    def _generate_rsa_keys():
        key = RSA.generate(2048)
        return key.export_key(), key.publickey().export_key()

    @staticmethod
    def _generate_des_key():
        return os.urandom(8)

    def encrypt_message(self, message: str, des_key=None) -> tuple[bytes, bytes]:
        """Returns (ciphertext, signature). Use provided DES key or default one."""
        if not isinstance(message, str):
            raise TypeError("Message must be string")

        key = des_key or self.des_key
        iv = os.urandom(8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        padded = pad(message.encode(), DES.block_size)
        ciphertext = iv + cipher.encrypt(padded)

        h = SHA256.new(ciphertext)
        signature = pkcs1_15.new(RSA.import_key(self.private_key)).sign(h)

        return ciphertext, signature


    def decrypt_message(self, ciphertext: bytes, signature: bytes, sender_pubkey: bytes) -> str:
        """Returns decrypted message or raises error"""
        # Verify signature first
        h = SHA256.new(ciphertext)
        try:
            pkcs1_15.new(RSA.import_key(sender_pubkey)).verify(h, signature)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid signature: {e}")

        # Then decrypt
        if len(ciphertext) < 16 or len(ciphertext) % 8 != 0:
            raise ValueError("Invalid ciphertext length")
        
        iv, ct = ciphertext[:8], ciphertext[8:]
        cipher = DES.new(self.des_key, DES.MODE_CBC, iv)
        
        try:
            return unpad(cipher.decrypt(ct), DES.block_size).decode()
        except ValueError as e:
            raise ValueError(f"Decryption failed: {e}")

    @staticmethod
    def rsa_encrypt(pubkey: bytes, data: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(RSA.import_key(pubkey))
        return cipher.encrypt(data)

    @staticmethod
    def rsa_decrypt(privkey: bytes, data: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(RSA.import_key(privkey))
        return cipher.decrypt(data)