import json
import random
import time
import requests
from datetime import datetime

labels = ["Brute Force", "Credential Stuffing", "SQL Injection"]
ip_pool = ["192.168.1.10", "172.16.0.5", "10.0.0.3", "203.0.113.99"]
usernames = ["admin", "root", "guest", "user"]
passwords = ["123456", "password", "admin", "letmein"]

url = "http://localhost:5000/logs/labeled_intrusions.json"

while True:
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": random.choice(ip_pool),
        "username": random.choice(usernames),
        "password": random.choice(passwords),
        "label": random.choice(labels)
    }
    try:
        print(f"Sending log: {log_entry}")
        response = requests.post(url, json=log_entry)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Failed to send log:", e)
    time.sleep(5)
