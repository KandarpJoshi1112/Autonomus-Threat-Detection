# 🚀 Step 1: Project Folder Structure with venv Setup
# This Python script initializes the folder structure for Project #1

import os
import subprocess
import sys

folders = [
    "agents",
    "data",
    "models",
    "utils",
    "logs",
    "configs",
    "tests",
    "visualization",
]

files = [
    "main.py",
    "README.md",
    ".env.example",
    "requirements.txt",
    ".gitignore"
]

def create_project_structure():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    for file in files:
        with open(file, 'w') as f:
            if file == "README.md":
                f.write("# Autonomous Threat Detection and Response System\n")
            elif file == ".env.example":
                f.write("# Example environment variables\nAPI_KEY=your_api_key_here\n")
            elif file == "requirements.txt":
                f.write("fastapi\nscapy\nstable-baselines3\nlangchain\ngpt4all\nfaiss-cpu\nsqlite-utils\nnetworkx\n")
            elif file == ".gitignore":
                f.write("""# Python
__pycache__/
*.py[cod]
*.egg-info/
.env
venv/
.env.*
.DS_Store

# VSCode (optional)
.vscode/
""")
            else:
                f.write("# Entry point\n")
            print(f"Created file: {file}")

    # Create virtual environment
    print("Creating virtual environment 'venv'...")
    subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    print("✅ Virtual environment 'venv' created. Activate it using:")
    print("- Windows: venv\\Scripts\\activate")
    print("- macOS/Linux: source venv/bin/activate")

if __name__ == "__main__":
    create_project_structure()
