import json
import os
import pickle
from datetime import datetime
from log_parser import load_logs, preprocess

MODEL_PATH = "../model/classifier.pkl"
LOG_DIR = "../logs"
OUTPUT_PATH = "../logs/labeled_intrusions.json"

def classify_and_log():
    # Load model
    with open(MODEL_PATH, "rb") as f:
        vectorizer, clf = pickle.load(f)

    # Load and preprocess logs
    df = load_logs()
    df = preprocess(df)

    # Predict and append labels
    X = vectorizer.transform(df["combined"])
    df["predicted_label"] = clf.predict(X)

    # Write labeled entries to a file
    with open(OUTPUT_PATH, "w") as out:
        for _, row in df.iterrows():
            output_data = {
                "timestamp": str(row["timestamp"]),
                "ip": row["ip"],
                "username": row["username"],
                "password": row["password"],
                "label": row["predicted_label"]
            }
            out.write(json.dumps(output_data) + "\n")

    print(f"Labeled output written to {OUTPUT_PATH}")

if __name__ == "__main__":
    classify_and_log()
