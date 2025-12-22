import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# Simple synthetic telemetry (stable + realistic enough for proof)
t = np.arange(0, 300)  # 300 seconds
altitude = 400 + 15*np.sin(t/20) + 2*np.sin(t/5)
velocity = 7.6 + 0.05*np.sin(t/18)
temperature = 22 + 0.8*np.sin(t/30)

df = pd.DataFrame({
    "t_sec": t,
    "altitude_km": altitude,
    "velocity_km_s": velocity,
    "temp_c": temperature
})

csv_path = os.path.join(OUT_DIR, "telemetry.csv")
df.to_csv(csv_path, index=False)

# Plot (this is the key artifact recruiters can see)
plt.figure()
plt.plot(df["t_sec"], df["altitude_km"])
plt.xlabel("Time (sec)")
plt.ylabel("Altitude (km)")
plt.title("NASA Telemetry: Altitude over Time")
png_path = os.path.join(OUT_DIR, "telemetry_plot.png")
plt.savefig(png_path, dpi=200, bbox_inches="tight")

print(f"Wrote: {csv_path}")
print(f"Wrote: {png_path}")
