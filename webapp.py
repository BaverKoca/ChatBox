from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_messages():
    with sqlite3.connect('messages.db') as conn:
        cur = conn.execute("SELECT sender, ciphertext FROM messages ORDER BY timestamp DESC LIMIT 30")
        messages = []
        for sender, ciphertext in cur.fetchall():
            # For demo, just show sender and ciphertext (not decrypted)
            messages.append(f"{sender}: {ciphertext.hex()[:32]}...")
        return messages[::-1]

@app.route('/')
def main():
    return render_template('main.html', now=datetime.now())

@app.route('/chat', methods=['GET'])
def chat():
    messages = get_messages()
    return render_template('index.html', messages=messages, now=datetime.now())

@app.route('/send', methods=['POST'])
def send():
    # This demo endpoint just stores the message as plaintext (not secure)
    msg = request.form.get('message')
    with sqlite3.connect('messages.db') as conn:
        conn.execute("INSERT INTO messages (sender, ciphertext, signature) VALUES (?, ?, ?)",
                     ("WebUser", msg.encode(), b""))
    return redirect('/chat')

if __name__ == '__main__':
    app.run(debug=True)
