import os
import random
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

# Simulated duel: two agents competing over rounds
rounds = list(range(1, 11))
agent_a = [random.randint(60, 100) for _ in rounds]
agent_b = [random.randint(60, 100) for _ in rounds]

df = pd.DataFrame({
    "round": rounds,
    "agent_a_score": agent_a,
    "agent_b_score": agent_b,
})

csv_path = os.path.join(OUT, "duel_scores.csv")
df.to_csv(csv_path, index=False)

plt.figure()
plt.plot(rounds, agent_a, marker="o", label="Agent A")
plt.plot(rounds, agent_b, marker="o", label="Agent B")
plt.title("Multi-Agent Duel Scores")
plt.xlabel("Round")
plt.ylabel("Score")
plt.legend()
png_path = os.path.join(OUT, "duel_scores.png")
plt.savefig(png_path)
plt.close()

print("WROTE:", csv_path)
print("WROTE:", png_path)
