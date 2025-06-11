# Autonomous Threat Detection and Response System


🛡️ Autonomous Threat Detection System

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/Powered%20By-LangChain-purple)](https://www.langchain.com/)
[![HuggingFace](https://img.shields.io/badge/API-HuggingFace-yellow.svg)](https://huggingface.co/inference-api)

An AI-powered end-to-end security analysis tool that:
- 📥 Collects network packet logs
- 🧠 Parses and indexes them using semantic search
- ⚠️ Classifies them as safe / suspicious / threat
- 🤖 Makes intelligent decisions with reinforcement learning
- 📊 Visualizes insights in a sleek dashboard



⚠️ Disclaimer: This project is a proof-of-concept designed to showcase autonomous multi-agent orchestration, Retrieval-Augmented Generation (RAG) querying, and reinforcement learning in a simulated cybersecurity workflow.
It is not a production-grade Intrusion Detection System (IDS) and should not be relied upon to accurately detect, classify, or respond to real-world security threats.
The goal is to demonstrate how various modern AI tools can interact, not to deliver hardened or verified threat detection.



## 📁 Project Structure

```bash
Autonomous-Threat-Detection/
│
├── agents/
│   ├── log_parser_agent.py      # QA over packet logs
│   ├── classifier_agent.py      # LLM-based log classifier
│   └── decision_agent.py        # RL decision-making agent
│
├── data/
│   └── faiss_index/             # Stored FAISS vector index
│
├── logs/
│   └── packets.json             # Collected packet data
│
├── utils/
│   └── log_collector.py         # Real-time packet sniffer
│
├── visualization/
│   ├── dashboard.py             # FastAPI dashboard backend
│   └── static/                  # HTML + CSS + JS for dashboard
│
├── .env                         # HuggingFace API key
└── README.md
```

---

## 🚀 How to Run

### 1. Setup the Environment

```bash
git clone https://github.com/yourusername/Autonomous-Threat-Detection.git
cd Autonomous-Threat-Detection
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your HuggingFace API key to `.env`

```ini
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

### 3. Step-by-Step Execution

```bash
# Step 1: Collect real-time logs (needs admin privileges)
sudo python utils/log_collector.py

# Step 2: Parse & index logs
python agents/log_parser_agent.py

# Step 3: Classify logs using LLM
python agents/classifier_agent.py

# Step 4: Use RL agent to make threat-handling decisions
python agents/decision_agent.py

# Step 5: Visualize everything in a dashboard
uvicorn visualization.dashboard:app --reload
```

---

## 💬 Sample Queries (Step 2)

```txt
🔍 Ask something about logs (or type 'exit'):
> What IP sent the most packets?
> Show all packets using TCP protocol
> Which destination port had suspicious activity?
```

---

## 📊 Dashboard Preview

Access: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Features:
- Realtime threat classification
- Top source IPs and destination ports
- Action log of RL agent decisions

---

## 🧠 Tech Stack

- **LangChain** – QA & semantic indexing
- **HuggingFace Inference API** – Language model access
- **FAISS** – Efficient vector similarity search
- **Stable-Baselines3** – Reinforcement learning agent
- **FastAPI + Uvicorn** – Web dashboard
- **Scapy** – Network packet sniffing

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---



## Screenshots 📷


Packet Logging:

![Screenshot (41)](https://github.com/user-attachments/assets/f3703e78-d194-4aa0-af73-bb87386bc85c)


Query System:

![Screenshot (45)](https://github.com/user-attachments/assets/2405723f-7731-4d7e-8e71-32ed5adc03d3)


Reinforcement Learning:

![Screenshot (51)](https://github.com/user-attachments/assets/c1f0dd23-f155-4c65-9020-efd0f0bffccb)
![Screenshot (52)](https://github.com/user-attachments/assets/1584ec24-790b-44b3-817b-4a176bd45dcd)
![Screenshot (53)](https://github.com/user-attachments/assets/0772cbbb-d808-4ec4-885a-677e56787056)

Dashboard:

![Screenshot (54)](https://github.com/user-attachments/assets/e1e33de6-995f-4070-8d9b-c7d5ea5f9c55)



## 🤝 Contribute

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change or improve.

---

## Author

👤 **Kandarp Joshi**

* Github: [@Kandarp Joshi](https://github.com/KandarpJoshi1112)
* LinkedIn: [@Kandarp Joshi](https://www.linkedin.com/in/kandarp-joshi-3451231bb/)


## ⭐ If you like this project...

Give it a star ⭐ and share it with other developers or students interested in network security & AI!

