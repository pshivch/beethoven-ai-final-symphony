import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "outputs")
os.makedirs(OUT, exist_ok=True)

# Simple "flight health" synthetic example: altitude + vibration over time
t = np.arange(0, 300)
altitude = 35000 + 800*np.sin(t/25) + 200*np.cos(t/9)
vibration = 0.2 + 0.05*np.sin(t/7) + 0.02*np.random.RandomState(0).randn(len(t))

df = pd.DataFrame({"t": t, "altitude_ft": altitude, "vibration_g": vibration})
csv_path = os.path.join(OUT, "boeing_flight_signals.csv")
df.to_csv(csv_path, index=False)

plt.figure()
plt.plot(df["t"], df["altitude_ft"])
plt.xlabel("t")
plt.ylabel("altitude_ft")
plt.title("Mirror 08 Boeing — Synthetic Altitude Trace")
png_path = os.path.join(OUT, "altitude_trace.png")
plt.savefig(png_path, dpi=160, bbox_inches="tight")

proof = {
    "mirror": "08_boeing",
    "artifacts": [os.path.basename(csv_path), os.path.basename(png_path)],
    "notes": "Synthetic signals to demonstrate pipeline + artifact generation."
}
json_path = os.path.join(OUT, "boeing_proof.json")
with open(json_path, "w") as f:
    json.dump(proof, f, indent=2)

print("Wrote:", csv_path)
print("Wrote:", png_path)
print("Wrote:", json_path)
