import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

outdir = Path("outputs")
csv_path = outdir / "latency.csv"
png_path = outdir / "latency_hist.png"

df = pd.read_csv(csv_path)

# Pick a reasonable latency column automatically
lat_col = None
for c in df.columns:
    if "lat" in c.lower():
        lat_col = c
        break
if lat_col is None:
    # fallback: first numeric column
    num_cols = df.select_dtypes(include="number").columns.tolist()
    lat_col = num_cols[0] if num_cols else df.columns[0]

vals = pd.to_numeric(df[lat_col], errors="coerce").dropna()

plt.figure()
plt.hist(vals, bins=20)
plt.title("Netflix — Orchestration Pipeline Latency")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(png_path, dpi=200)
print(f"Wrote: {png_path}")
