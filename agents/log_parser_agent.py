# 🚀 Step 3: Log Parser Agent with Free LLM and Embeddings
# Located at: agents/log_parser_agent.py

import json
import os
import sqlite3
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

LOG_PATH = "logs/packets.json"
INDEX_DIR = "data/faiss_index"

# Load logs from JSON file
def load_logs(log_path=LOG_PATH):
    with open(log_path, 'r') as f:
        logs = [json.loads(line.strip()) for line in f.readlines()]
    return [f"{log['timestamp']} | {log['src_ip']}->{log['dst_ip']} | Port: {log['src_port']}->{log['dst_port']} | Protocol: {log['protocol']}" for log in logs]

# Build FAISS vector index from logs
def build_vector_index(log_texts):
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=10)
    docs = splitter.create_documents(log_texts)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(INDEX_DIR)
    return db

# Load FAISS vector index
def load_index():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)

# Query logs: retrieve only the top-1 most relevant document
# and return a concise answer

def query_logs(question: str):
    db = load_index()
    # Limit retrieval to top 1 result
    retriever = db.as_retriever(search_kwargs={"k": 1})
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        temperature=0.1,
        max_new_tokens=512,
    )
    # Create a QA chain that omits source documents in output
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    # Invoke the chain with the user question
    result = qa_chain.invoke({"query": question})
    return result

if __name__ == "__main__":
    print("📦 Checking for existing FAISS index...")
    if not os.path.exists(INDEX_DIR) or not os.listdir(INDEX_DIR):
        print("🔧 No index found. Building it now...")
        logs = load_logs()
        build_vector_index(logs)
        print("✅ FAISS index built.")
    else:
        print("✅ Found existing FAISS index. Skipping rebuild.")

    while True:
        q = input("\n🔍 Ask something about logs (or type 'exit'): ")
        if q.lower() == "exit":
            break
        answer = query_logs(q)
        print(f"🧠 Answer: {answer}")
