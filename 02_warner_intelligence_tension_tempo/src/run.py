import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

scenes = [
    ("Quiet opening", 0.2),
    ("Suspicion rises", 0.5),
    ("Conflict", 0.8),
    ("Climax", 1.0),
    ("Resolution", 0.3),
]

df = pd.DataFrame(scenes, columns=["scene", "tension"])
csv_path = os.path.join(OUT, "tempo_map.csv")
df.to_csv(csv_path, index=False)

plt.figure()
plt.plot(df["tension"], marker="o")
plt.title("Narrative Tension Curve")
plt.xlabel("Scene")
plt.ylabel("Tension")
png_path = os.path.join(OUT, "tension_curve.png")
plt.savefig(png_path)
plt.close()

print("WROTE:", csv_path)
print("WROTE:", png_path)
