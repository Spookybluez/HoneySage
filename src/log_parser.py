import os
import json
import pandas as pd

LOG_DIR = "../logs"

def load_logs():
    data = []
    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(LOG_DIR, filename)
            with open(filepath, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        data.append(entry)
                    except json.JSONDecodeError:
                        continue
    return pd.DataFrame(data)

def preprocess(df):
    # Combine username and password fields for NLP analysis
    df['combined'] = df['username'].fillna('') + ' ' + df['password'].fillna('')
    df['ip'] = df['ip'].fillna('unknown')
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df

if __name__ == "__main__":
    df = load_logs()
    df = preprocess(df)
    print(df.head())
