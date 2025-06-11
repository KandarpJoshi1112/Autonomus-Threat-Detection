# 🚀 Step 2: Real-Time Log Collector
# Located at: utils/log_collector.py

# This module captures network packets using Scapy and saves logs in structured format (JSON + SQLite)

from scapy.all import sniff, IP, TCP
import json
import time
import sqlite3
import os

LOG_PATH = "logs/packets.json"
DB_PATH = "data/packets.db"

# Ensure log folder and DB exists
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Initialize SQLite DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS packets (
    timestamp TEXT,
    src_ip TEXT,
    dst_ip TEXT,
    src_port INTEGER,
    dst_port INTEGER,
    protocol TEXT
)''')
conn.commit()

def packet_handler(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        log_entry = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "src_ip": packet[IP].src,
            "dst_ip": packet[IP].dst,
            "src_port": packet[TCP].sport,
            "dst_port": packet[TCP].dport,
            "protocol": packet.proto
        }

        # Append to JSON log
        with open(LOG_PATH, 'a') as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

        # Insert into DB
        c.execute('''INSERT INTO packets VALUES (?, ?, ?, ?, ?, ?)''',
                  (log_entry["timestamp"], log_entry["src_ip"], log_entry["dst_ip"],
                   log_entry["src_port"], log_entry["dst_port"], log_entry["protocol"]))
        conn.commit()

        print(f"[+] Packet logged: {log_entry['src_ip']} -> {log_entry['dst_ip']}")

if __name__ == '__main__':
    print("🚦 Starting real-time packet sniffer (press Ctrl+C to stop)...")
    sniff(filter="ip", prn=packet_handler, store=False)
