import numpy as np
import importlib
import subprocess, sys, os
import matplotlib.pyplot as plt

# Ensure compiled extensions are importable
sys.path.append(os.path.abspath("rust_core/target/release"))
sys.path.append(os.path.abspath("cpp_dsp/build"))

# Rust kernel
rust = importlib.import_module("rust_core")
# C++ DSP
cpp  = importlib.import_module("cpp_dsp")

# Julia bridge
from julia.api import Julia
jl = Julia(compiled_modules=False)
from julia import Main
Main.include("julia/Harmony.jl")
cadence_score = Main.Harmony.cadence_score

def disney_emotion_to_motif(seed=42):
    rng = np.random.default_rng(seed)
    return (rng.normal(0, 1, 64).cumsum() * 0.02).astype(np.float32)

def nasa_telemetry_to_freqs(seed=7):
    rng = np.random.default_rng(seed)
    base = 220.0
    return list((base * (2 ** (rng.integers(-12, 12, 5)/12.0))).astype(float))

if __name__ == "__main__":
    motifA = disney_emotion_to_motif(1)
    motifB = disney_emotion_to_motif(2)

    # Rust low-latency metrics
    varA = rust.motif_variance(motifA.tolist())
    dtw  = rust.tempo_align(motifA.tolist(), motifB.tolist())

    # C++ harmonic score
    freqs = nasa_telemetry_to_freqs()
    dissonance = cpp.polyphony_score(freqs)

    # Julia cadence plausibility (using pitch classes mod 12)
    pcs = [int(round(f)) % 12 for f in np.linspace(60, 72, 16)]
    cadence = float(cadence_score(pcs))

    print(f"[Rust] variance={{varA:.6f}}  dtw={{dtw:.6f}}")
    print(f"[C++]  dissonance={{dissonance:.6f}}")
    print(f"[Julia] cadence_score={{cadence:.3f}}")

    # Quick visual artifact
    plt.plot(motifA, label="motif A")
    plt.plot(motifB, label="motif B")
    plt.legend(); plt.title("Motif trajectories (Disney)")
    os.makedirs("artifacts", exist_ok=True)
    plt.savefig("artifacts/motifs.png", dpi=110)
    print("Saved artifacts/motifs.png")
