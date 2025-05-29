import socket
import threading
from crypto_utils import CryptoHandler, send_blob, recv_blob

class SecureClient:
    def __init__(self, host='192.168.15.11', port=12345):
        self.host = host
        self.port = port
        self.crypto = CryptoHandler()
        self.sock = None
        self.server_pubkey = None

    def _establish_connection(self):
        """Handles secure handshake"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        
        # 1. Send client's RSA public key
        send_blob(self.sock, self.crypto.public_key)
        
        # 2. Receive server's RSA public key
        self.server_pubkey = recv_blob(self.sock)
        
        # 3. Send DES key encrypted with server's public key
        encrypted_des = self.crypto.rsa_encrypt(self.server_pubkey, self.crypto.des_key)
        send_blob(self.sock, encrypted_des)
        
        print(f"[CONNECTED] Session established with {self.host}:{self.port}")

    def _receive_loop(self):
        """Handles incoming messages"""
        while True:
            try:
                ciphertext = recv_blob(self.sock)
                signature = recv_blob(self.sock)
                
                try:
                    msg = self.crypto.decrypt_message(ciphertext, signature, self.server_pubkey)
                    print(f"\n[Received] {msg}")
                except ValueError as e:
                    print(f"\n[ERROR] Message verification failed: {e}")
                    
            except (ConnectionError, OSError) as e:
                print(f"\n[DISCONNECTED] Server connection lost: {e}")
                break
            except Exception as e:
                print(f"\n[ERROR] Unexpected error: {e}")
                break

    def send_message(self, message: str):
        """Sends encrypted message"""
        try:
            ciphertext, signature = self.crypto.encrypt_message(message)
            send_blob(self.sock, ciphertext)
            send_blob(self.sock, signature)
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")

    def start(self):
        """Main client interface"""
        try:
            self._establish_connection()
            threading.Thread(target=self._receive_loop, daemon=True).start()
            
            while True:
                try:
                    msg = input("> ")
                    if msg.lower() == 'exit':
                        break
                    self.send_message(msg)
                except KeyboardInterrupt:
                    break
                    
        finally:
            if self.sock:
                self.sock.close()
            print("[CLOSED] Connection terminated")

if __name__ == '__main__':
    client = SecureClient()
    client.start()