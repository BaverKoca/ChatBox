import socket
import threading
import sqlite3
from crypto_utils import CryptoHandler, send_blob, recv_blob

class SecureServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.clients = {}  # {socket: (addr, crypto_handler)}
        self.server_crypto = CryptoHandler()
        self._init_db()

    def _init_db(self):
        """Initialize message database"""
        with sqlite3.connect('messages.db') as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    sender TEXT,
                    ciphertext BLOB,
                    signature BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _save_message(self, sender: str, ciphertext: bytes, signature: bytes):
        """Store encrypted message"""
        with sqlite3.connect('messages.db') as conn:
            conn.execute(
                "INSERT INTO messages (sender, ciphertext, signature) VALUES (?, ?, ?)",
                (sender, ciphertext, signature)
            )

    def _handle_client(self, sock, addr):
        """Manage client connection"""
        try:
            # 1. Receive client's public key
            client_pubkey = recv_blob(sock)
            
            # 2. Send server's public key
            send_blob(sock, self.server_crypto.public_key)
            
            # 3. Receive and decrypt DES key
            encrypted_des = recv_blob(sock)
            des_key = self.server_crypto.rsa_decrypt(self.server_crypto.private_key, encrypted_des)
            
            # Create client-specific crypto handler
            client_crypto = CryptoHandler()
            client_crypto.des_key = des_key
            client_crypto.public_key = client_pubkey
            
            self.clients[sock] = (addr, client_crypto)
            print(f"[NEW CLIENT] {addr} connected")
            
            # Message handling loop
            while True:
                ciphertext = recv_blob(sock)
                signature = recv_blob(sock)
                
                try:
                    # Decrypt message using sender's key
                    msg = client_crypto.decrypt_message(ciphertext, signature, client_pubkey)
                    print(f"[{addr[0]}] {msg}")
                    self._save_message(addr[0], ciphertext, signature)

                    # Re-broadcast original *plaintext* message
                    self._broadcast(sock, msg)
                except ValueError as e:
                    print(f"[INVALID MESSAGE from {addr[0]}] {e}")

                    
        except (ConnectionError, OSError):
            print(f"[CLIENT DISCONNECTED] {addr}")
        finally:
            sock.close()
            self.clients.pop(sock, None)

    def _broadcast(self, sender_sock: socket.socket, plain_msg: str):
        sender_addr = self.clients[sender_sock][0][0]  # IP of sender
        tagged_msg = f"{sender_addr}: {plain_msg}"

        for sock, (addr, crypto) in self.clients.items():
            if sock != sender_sock:
                try:
                    ciphertext, signature = self.server_crypto.encrypt_message(tagged_msg, des_key=crypto.des_key)
                    send_blob(sock, ciphertext)
                    send_blob(sock, signature)
                except Exception as e:
                    print(f"[BROADCAST FAILED] to {addr}: {e}")



    def _admin_console(self):
        """System administrator interface"""
        while True:
            cmd = input("\n[ADMIN] Command (clients/kick/exit): ").strip().lower()
            if cmd == 'clients':
                print(f"Connected clients: {len(self.clients)}")
                for sock, (addr, _) in self.clients.items():
                    print(f"- {addr[0]}:{addr[1]}")
            elif cmd.startswith('kick'):
                ip = cmd.split()[1]
                for sock, (addr, _) in list(self.clients.items()):
                    if addr[0] == ip:
                        sock.close()
                        del self.clients[sock]
                        print(f"Kicked {ip}")
            elif cmd == 'exit':
                break

    def start(self):
        """Start the secure server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

        # Start admin thread
        threading.Thread(target=self._admin_console, daemon=True).start()

        # Accept connections
        while True:
            try:
                sock, addr = server.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(sock, addr),
                    daemon=True
                ).start()
            except KeyboardInterrupt:
                print("\nShutting down server...")
                break
            except Exception as e:
                print(f"[SERVER ERROR] {e}")

        # Cleanup
        server.close()
        for sock in list(self.clients.keys()):
            sock.close()
        print("[SERVER STOPPED]")

if __name__ == '__main__':
    server = SecureServer()
    server.start()