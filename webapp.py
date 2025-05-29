from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from crypto_utils import CryptoHandler

app = Flask(__name__)
crypto = CryptoHandler()

def get_messages():
    with sqlite3.connect('messages.db') as conn:
        cur = conn.execute("SELECT sender, ciphertext, signature FROM messages ORDER BY timestamp DESC LIMIT 30")
        messages = []
        for sender, ciphertext, signature in cur.fetchall():
            try:
                # Decrypt message for display
                msg = crypto.decrypt_message(ciphertext, signature, crypto.public_key)
                messages.append(f"{sender}: {msg}")
            except Exception:
                messages.append(f"{sender}: [Unable to decrypt]")
        return messages[::-1]

@app.route('/')
def main():
    return render_template('index.html', now=datetime.now())

@app.route('/chat', methods=['GET'])
def chat():
    messages = get_messages()
    return render_template('chat.html', messages=messages, now=datetime.now())

@app.route('/send', methods=['POST'])
def send():
    msg = request.form.get('message')
    ciphertext, signature = crypto.encrypt_message(msg)
    with sqlite3.connect('messages.db') as conn:
        conn.execute("INSERT INTO messages (sender, ciphertext, signature) VALUES (?, ?, ?)",
                     ("WebUser", ciphertext, signature))
    return redirect('/chat')

if __name__ == '__main__':
    app.run(debug=True)
