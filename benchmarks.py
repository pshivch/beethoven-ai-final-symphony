import time, numpy as np, json
from orchestrate import disney_emotion_to_motif
import rust_core as rust

N = 50
motifA = disney_emotion_to_motif(1).tolist()
motifB = disney_emotion_to_motif(2).tolist()
t0 = time.perf_counter()
for _ in range(N):
    rust.tempo_align(motifA, motifB)
t1 = time.perf_counter()
lat_ms = (t1 - t0) * 1000 / N
print(f"DTW-lite mean latency: {lat_ms:.3f} ms")

out = {"rust_dtw_ms": round(lat_ms, 3), "runs": N}
import os; os.makedirs("artifacts", exist_ok=True)
with open("artifacts/metrics.json","w") as f: json.dump(out, f, indent=2)
print("Wrote artifacts/metrics.json")
