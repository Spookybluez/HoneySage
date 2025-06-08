import json
from datetime import datetime
import os

LOG_PATH = "../logs"

def log_attempt(ip, username, password):
    os.makedirs(LOG_PATH, exist_ok=True)
    now = datetime.now().isoformat()
    data = {
        "timestamp": now,
        "ip": ip,
        "username": username,
        "password": password
    }
    filename = f"{LOG_PATH}/interactions_{datetime.now().date()}.json"
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")
