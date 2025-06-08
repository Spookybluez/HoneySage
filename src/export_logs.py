# export_logs.py
import json
import csv
import os

INPUT_FILE = os.path.join("logs", "labeled_intrusions.json")
CSV_OUTPUT = os.path.join("exports", "intrusion_logs.csv")

os.makedirs("exports", exist_ok=True)

def export_logs_to_csv():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file '{INPUT_FILE}' not found. Please ensure the file exists.")
        return

    with open(INPUT_FILE, "r") as infile, open(CSV_OUTPUT, "w", newline="") as outfile:
        fieldnames = ["timestamp", "ip", "username", "password", "label"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in infile:
            try:
                log = json.loads(line.strip())
                writer.writerow({
                    "timestamp": log.get("timestamp", ""),
                    "ip": log.get("ip", ""),
                    "username": log.get("username", ""),
                    "password": log.get("password", ""),
                    "label": log.get("label", "")
                })
            except json.JSONDecodeError:
                print("Skipping invalid JSON entry")

    print(f"✅ Logs exported to {CSV_OUTPUT}")

if __name__ == "__main__":
    export_logs_to_csv()
