import os
import json
from flask import Flask, send_file, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="templates", static_folder="static")

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

LOG_FILE = os.path.join("logs", "labeled_intrusions.json")

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/logs/labeled_intrusions.json", methods=["GET", "POST"])
def log_handler():
    if request.method == "POST":
        data = request.get_json()
        if data:
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(data) + "\n")
            socketio.emit("new_log", data)
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "no data"}), 400

    # ✅ Return JSON list for frontend consumption
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        entries = [json.loads(line) for line in lines if line.strip()]
    return jsonify(entries)


@socketio.on('connect')
def on_connect():
    print("⚡ Client connected")

@socketio.on('new_log')
def handle_new_log(data):
    print("🔴 New intrusion detected:", data)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    emit("new_log", data, broadcast=True)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    open(LOG_FILE, "a").close()
    socketio.run(app, host="127.0.0.1", port=5000)
