import eventlet
import socket
import os
import json
from flask import Flask, send_file, render_template
from flask_socketio import SocketIO, emit

eventlet.monkey_patch()

app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = os.path.join("logs", "labeled_intrusions.json")

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/logs/labeled_intrusions.json")
def get_logs():
    return send_file(LOG_FILE)

@socketio.on('connect')
def on_connect():
    print("\u26a1 Client connected")

@socketio.on('new_log')
def handle_new_log(data):
    print("\ud83d\udd34 New intrusion detected:", data)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    emit("new_log", data, broadcast=True)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    open(LOG_FILE, "a").close()
    try:
        socketio.run(app, host="0.0.0.0", port=5000)
    except OSError as e:
        if e.errno == 10048:
            print("[Error] Port 5000 is already in use. Try closing the other instance or use a different port:")
            print("       socketio.run(app, host='0.0.0.0', port=5050)")
        else:
            raise
