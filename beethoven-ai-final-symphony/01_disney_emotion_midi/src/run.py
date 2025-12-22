import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# Simulated emotion signal (Disney-style emotional arc)
t = np.arange(0, 240)  # 4 minutes
emotion_intensity = 0.5 + 0.4 * np.sin(t / 30)

# Map emotion -> tempo (simple orchestration rule)
tempo = 80 + 60 * emotion_intensity

df = pd.DataFrame({
    "time_sec": t,
    "emotion_intensity": emotion_intensity,
    "tempo_bpm": tempo
})

csv_path = os.path.join(OUT_DIR, "emotion_to_tempo.csv")
df.to_csv(csv_path, index=False)

# Plot
plt.figure()
plt.plot(df["time_sec"], df["tempo_bpm"])
plt.xlabel("Time (sec)")
plt.ylabel("Tempo (BPM)")
plt.title("Disney Emotion → Tempo Orchestration")
png_path = os.path.join(OUT_DIR, "emotion_tempo_curve.png")
plt.savefig(png_path, dpi=200, bbox_inches="tight")

print(f"Wrote: {csv_path}")
print(f"Wrote: {png_path}")
