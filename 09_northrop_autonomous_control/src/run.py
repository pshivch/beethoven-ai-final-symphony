import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def main():
    os.makedirs("outputs", exist_ok=True)

    np.random.seed(42)
    frames = np.arange(1, 101)
    latency_ms = np.random.normal(loc=45, scale=8, size=len(frames))

    with open("artifacts/plots/latency.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "latency_ms"])
        for fnum, lat in zip(frames, latency_ms):
            writer.writerow([int(fnum), float(lat)])

    plt.figure(figsize=(8,4))
    plt.hist(latency_ms, bins=20)
    plt.title("Northrop — Vision Pipeline Latency")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("artifacts/plots/latency_hist.png")
    plt.close()

    print("Northrop artifacts written to outputs/")

if __name__ == "__main__":
    main()
