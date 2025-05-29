# Chat Box (Whatsapp-Clone)

A modern, secure, and open-source chat application inspired by WhatsApp. Chat Box features a beautiful web UI, real-time encrypted messaging, and a Python client/server for advanced users. Built with Flask, Python, and strong cryptography.

---

<p align="center">
  <img src="static/Chat%20Illustration.png" alt="Landing Page" width="400"/>
</p>

---

## 🚀 Features
- **End-to-End Encryption:** Messages are encrypted with DES and signed with RSA for privacy and authenticity.
- **Modern Web UI:** Responsive, WhatsApp-inspired design with team, features, and contact sections.
- **Real-Time Messaging:** Auto-refreshing chat interface for seamless conversations.
- **Multi-Platform:** Use the web app or the Python client/server for secure messaging.
- **Open Source:** Built by students, for everyone. Free to use and extend.
- **SQLite Database:** Securely stores encrypted messages, sender, and timestamp.

---

## 🗂️ Project Structure
```text
Whatsapp-Clone/
├── webapp.py           # Flask web server (main entry for web chat)
├── server.py           # Secure socket server for encrypted chat
├── client.py           # Secure socket client
├── crypto_utils.py     # All cryptographic logic (DES, RSA, signatures)
├── models.py           # SQLAlchemy models (optional, for DB structure)
├── messages.db         # SQLite database
├── static/             # Static files (images, CSS)
│   └── Chat Illustration.png
├── templates/          # HTML templates for Flask
│   ├── index.html      # Landing page
│   └── chat.html       # Chat interface
└── README.md
```

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.8+
- [Flask](https://flask.palletsprojects.com/)
- [pycryptodome](https://www.pycryptodome.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) (optional, for models.py)

Install dependencies:
```bash
pip install flask pycryptodome sqlalchemy
```

### Database Initialization
The database is created automatically on first run. To manually create it:
```python
import sqlite3
with sqlite3.connect('messages.db') as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            ciphertext BLOB,
            signature BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
```

### Running the Web App
```bash
python webapp.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

### (Optional) Secure Socket Server/Client
- Start the server: `python server.py`
- Start a client: `python client.py`

---

## 🔒 Encryption Architecture
- **DES (CBC mode):** Encrypts message content with a random IV for each message.
- **RSA (2048-bit):** Used for key exchange and digital signatures.
- **Signatures:** Every message is signed and verified for authenticity.
- **Key Exchange:** Secure handshake between client and server.
- **Database:** Only encrypted messages and signatures are stored.

---

## 💡 How It Works
- **Web App:** Users chat via a beautiful web interface. Messages are encrypted before storage and decrypted for display.
- **Python Client/Server:** Advanced users can run the secure socket server and connect with the Python client for terminal-based encrypted chat.
- **Database:** All messages are stored encrypted, with digital signatures and timestamps.

---

## 👨‍💻 Team
<table>
  <tr>
    <td align="center"><img src="https://ui-avatars.com/api/?name=Baver+Koca&background=075e54&color=fff&size=80" width="60"/><br/><b>Baver Koca</b><br><a href="mailto:baver.koca00@gmail.com">Email</a> | <a href="https://github.com/BaverKoca">GitHub</a> | <a href="https://www.linkedin.com/in/baver-koca">LinkedIn</a></td>
    <td align="center"><img src="https://ui-avatars.com/api/?name=Sanusi&background=25d366&color=fff&size=80" width="60"/><br/><b>Sanusi</b></td>
    <td align="center"><img src="https://ui-avatars.com/api/?name=Saeed+Bizri&background=128c7e&color=fff&size=80" width="60"/><br/><b>Saeed Bizri</b></td>
  </tr>
</table>

---

## 📬 Contact
<p>
  <a href="mailto:baver.koca00@gmail.com"><img src="https://img.icons8.com/color/32/gmail-new.png" alt="Email" style="vertical-align:middle;"> baver.koca00@gmail.com</a><br>
  <a href="https://github.com/BaverKoca"><img src="https://img.icons8.com/ios-glyphs/32/25d366/github.png" alt="GitHub" style="vertical-align:middle;"> github.com/BaverKoca</a><br>
  <a href="https://www.linkedin.com/in/baver-koca"><img src="https://img.icons8.com/color/32/linkedin.png" alt="LinkedIn" style="vertical-align:middle;"> linkedin.com/in/baver-koca</a>
</p>

---

## 📝 License
MIT License. Free for personal and commercial use.

---

## 🙏 Credits
- Inspired by WhatsApp
- Built with Python, Flask, and PyCryptodome
- UI icons from [Icons8](https://icons8.com/)