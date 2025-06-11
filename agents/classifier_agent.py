# 🚀 Step 4: Classifier Agent for Log Entries
# Located at: agents/classifier_agent.py

import os
import sqlite3
import argparse
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables (if needed)
load_dotenv()

# Constants and thresholds
DB_PATH = "data/packets.db"
CANDIDATE_LABELS = ["SAFE", "SUSPICIOUS", "THREAT"]
MODEL_NAME = "typeform/distilbert-base-uncased-mnli"
THREAT_THRESHOLD = 0.7
SAFE_THRESHOLD = 0.7

# Fetch logs and ensure classification column exists

def fetch_logs(limit):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(packets)")
    cols = [row[1] for row in c.fetchall()]
    if "classification" not in cols:
        c.execute("ALTER TABLE packets ADD COLUMN classification TEXT")
    c.execute(
        "SELECT rowid, timestamp, src_ip, dst_ip, src_port, dst_port, protocol FROM packets LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    logs = []
    for row in rows:
        rowid, timestamp, src_ip, dst_ip, src_port, dst_port, protocol = row
        entry_text = f"{timestamp} | {src_ip} -> {dst_ip} | Port: {dst_port} | Protocol: {protocol}"
        logs.append((rowid, entry_text))
    return logs

# Save classification results back to the database

def save_classification(results):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for rowid, label in results:
        c.execute(
            "UPDATE packets SET classification = ? WHERE rowid = ?",
            (label, rowid)
        )
    conn.commit()
    conn.close()

# Main classification logic with multi-label and rule-based heuristics

def classify_logs(limit):
    logs = fetch_logs(limit)
    total = len(logs)
    if total == 0:
        print("No logs found to classify.")
        return
    print(f"🛠 Classifying {total} logs using model '{MODEL_NAME}' with multi-label zero-shot...")

    # Initialize zero-shot pipeline once
    classifier = pipeline(
        "zero-shot-classification",
        model=MODEL_NAME,
        device=-1,
        hypothesis_template="This network log entry is {}."
    )

    results = []
    batch_size = 16
    for i in range(0, total, batch_size):
        batch = logs[i : i + batch_size]
        texts = [entry for _, entry in batch]
        outputs = classifier(
            texts,
            candidate_labels=CANDIDATE_LABELS,
            multi_label=True
        )
        for j, out in enumerate(outputs):
            scores = dict(zip(out["labels"], out["scores"]))
            rowid, entry_text = batch[j]
            # Rule-based override for common web ports
            if "Port: 80" in entry_text or "Port: 443" in entry_text:
                label = "SAFE"
            # Otherwise apply threshold logic
            elif scores.get("THREAT", 0) > THREAT_THRESHOLD:
                label = "THREAT"
            elif scores.get("SAFE", 0) > SAFE_THRESHOLD:
                label = "SAFE"
            else:
                label = "SUSPICIOUS"
            results.append((rowid, label))
            print(f"  {i + j + 1}/{total}: Entry {rowid} labeled as {label}")

    save_classification(results)
    print(f"✅ Classified {total} log entries with enhanced logic.")

# Entry point with configurable limit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify network log entries.")
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Number of log entries to classify (default: 100)"
    )
    args = parser.parse_args()
    classify_logs(args.limit)