import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "outputs")
os.makedirs(OUT, exist_ok=True)

# Simple telemetry example: altitude + temperature
t = np.arange(0, 300)
alt_km = 400 + 15*np.sin(t/20)
temp_c = 22 + 3*np.cos(t/18)

df = pd.DataFrame({"t": t, "alt_km": alt_km, "temp_c": temp_c})
csv_path = os.path.join(OUT, "nasa_telemetry.csv")
df.to_csv(csv_path, index=False)

plt.figure()
plt.plot(df["t"], df["alt_km"])
plt.xlabel("t")
plt.ylabel("alt_km")
plt.title("Mirror 10 NASA — Telemetry Altitude")
png_path = os.path.join(OUT, "telemetry_altitude.png")
plt.savefig(png_path, dpi=160, bbox_inches="tight")

proof = {
    "mirror": "10_nasa",
    "artifacts": [os.path.basename(csv_path), os.path.basename(png_path)],
    "notes": "Synthetic telemetry to demonstrate artifact generation."
}
json_path = os.path.join(OUT, "nasa_proof.json")
with open(json_path, "w") as f:
    json.dump(proof, f, indent=2)

print("Wrote:", csv_path)
print("Wrote:", png_path)
print("Wrote:", json_path)
