# Entry point
# 🚀 Step 6: Orchestrator – Integrate All Agents
# Located at: main.py

"""
Orchestrates the full pipeline:
1. Collect live packets (Step 2)
2. Index and query logs (Step 3)
3. Classify entries (Step 4)
4. Decide actions (Step 5)
5. Apply mitigation or log actions
"""
import subprocess
import argparse
import os
from agents.log_parser_agent import build_vector_index, load_index, query_logs,load_logs
from agents.classifier_agent import classify_logs
from agents.decision_agent import ThreatDecisionEnv
from stable_baselines3 import PPO

# Configuration
COLLECT_TIME = 60  # seconds to run packet collector
DB_PATH = "data/packets.db"
MODEL_PATH = "models/decision_agent.zip"


def collect_logs(duration):
    # Run log collector for a fixed duration
    print(f"🔄 Collecting packets for {duration} seconds...")
    proc = subprocess.Popen(["sudo", "python", "utils/log_collector.py"] if os.name!="nt" else ["python", "utils/log_collector.py"])
    proc.wait(timeout=duration)
    proc.terminate()
    print("✅ Packet collection complete.")


def ensure_index():
    print("📦 Ensuring FAISS index...")
    if not os.path.exists("data/faiss_index") or not os.listdir("data/faiss_index"):
        texts = load_logs()
        build_vector_index(texts)
        print("✅ Index built.")
    else:
        print("✅ Index already exists.")


def orchestrate(limit):
    ensure_index()
    print("🔍 Performing classification...")
    classify_logs(limit)
    print("🤖 Making decisions on classified entries...")
    env = ThreatDecisionEnv()
    model = PPO.load(MODEL_PATH)
    obs = env.reset()
    total = len(env.data)
    correct = 0
    for i in range(total):
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        if reward > 0:
            correct += 1
    print(f"🎯 Decision accuracy: {correct}/{total} = {correct/total:.2%}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Full pipeline orchestration")
    parser.add_argument("--limit", type=int, default=100, help="Max log entries to classify")
    parser.add_argument("--collect", type=int, default=0, help="Seconds to run log collector (0 to skip)")
    args = parser.parse_args()
    if args.collect > 0:
        collect_logs(args.collect)
    orchestrate(args.limit)

# End of orchestrator
