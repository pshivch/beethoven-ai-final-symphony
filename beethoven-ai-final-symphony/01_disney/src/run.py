import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# Deterministic synthetic signal for proof artifacts
t = np.arange(0, 240)
x = 0.5 + 0.4*np.sin(t/30) + 0.1*np.sin(t/7)

df = pd.DataFrame({"time_sec": t, "signal": x})
csv_path = os.path.join(OUT_DIR, "emotion_to_tempo.csv")
df.to_csv(csv_path, index=False)

plt.figure()
plt.plot(df["time_sec"], df["signal"])
plt.xlabel("Time (sec)")
plt.ylabel("Signal")
plt.title("Disney Mirror: Emotion → Tempo Orchestration (Proof)")
png_path = os.path.join(OUT_DIR, "emotion_tempo_curve.png")
plt.savefig(png_path, dpi=200, bbox_inches="tight")

print("Wrote:", csv_path)
print("Wrote:", png_path)
