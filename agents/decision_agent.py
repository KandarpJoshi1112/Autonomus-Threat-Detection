
import numpy as np
import sqlite3
import os
import gym
from gym import Env, spaces
from stable_baselines3 import PPO

DB_PATH = "data/packets.db"
MODEL_PATH = "models/decision_agent.zip"

class ThreatDecisionEnv(Env):
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
        self.action_space = spaces.Discrete(3)  # 0: ignore, 1: alert, 2: quarantine
        self.data = self._load_data()
        self.idx = 0

    def _load_data(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT classification FROM packets WHERE classification IS NOT NULL")
        rows = c.fetchall()
        conn.close()
        mapping = {"SAFE":0, "SUSPICIOUS":1, "THREAT":2}
        data = []
        for row in rows:
            label = row[0]
            if label in mapping:
                onehot = np.zeros(3, dtype=np.float32)
                onehot[mapping[label]] = 1.0
                data.append((onehot, mapping[label]))
        return data

    def reset(self):
        self.idx = 0
        return self.data[self.idx][0]

    def step(self, action):
        obs, true = self.data[self.idx]
        reward = 1 if action == true else -1
        self.idx += 1
        done = self.idx >= len(self.data)
        next_obs = self.data[self.idx][0] if not done else np.zeros(3, dtype=np.float32)
        return next_obs, reward, done, {}

    def render(self, mode="human"):
        pass

if __name__ == "__main__":
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    env = ThreatDecisionEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save(MODEL_PATH)
    print("✅ Decision agent trained and saved.")

    # Example inference
    model = PPO.load(MODEL_PATH)
    obs = env.reset()
    total_reward = 0
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
    print(f"Total reward: {total_reward}")