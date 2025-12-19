import os
import numpy as np
import matplotlib.pyplot as plt

OUT_DIR = "outputs"
DATA_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def save_wav(path, sr, x):
    # 16-bit PCM minimal WAV writer (no extra deps)
    import wave, struct
    x = np.clip(x, -1.0, 1.0)
    x_i16 = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(x_i16.tobytes())

def stft_mag(x, n_fft=1024, hop=256):
    # simple magnitude STFT
    win = np.hanning(n_fft)
    frames = []
    for i in range(0, max(1, len(x)-n_fft), hop):
        seg = x[i:i+n_fft]
        if len(seg) < n_fft:
            seg = np.pad(seg, (0, n_fft-len(seg)))
        X = np.fft.rfft(seg * win)
        frames.append(np.abs(X))
    return np.array(frames).T  # (freq, time)

def main():
    sr = 22050
    dur = 6.0
    t = np.linspace(0, dur, int(sr*dur), endpoint=False)

    # "clean" motif-like signal (stacked tones)
    clean = (
        0.35*np.sin(2*np.pi*220*t) +
        0.22*np.sin(2*np.pi*330*t) +
        0.18*np.sin(2*np.pi*440*t) +
        0.10*np.sin(2*np.pi*660*t)
    )

    # degrade: noise + dropouts
    rng = np.random.default_rng(7)
    noise = 0.18*rng.standard_normal(len(t))
    degraded = clean + noise
    # dropout bursts
    for _ in range(8):
        start = rng.integers(0, len(t)-sr//8)
        degraded[start:start+sr//20] *= 0.15

    # "restoration": simple spectral-gate-ish smoothing (time median on mag)
    mag = stft_mag(degraded)
    mag_smooth = np.copy(mag)
    # median filter over time (no scipy)
    k = 5
    for ti in range(mag.shape[1]):
        lo = max(0, ti-k)
        hi = min(mag.shape[1], ti+k+1)
        mag_smooth[:, ti] = np.median(mag[:, lo:hi], axis=1)

    # plot spectrogram-like mags
    def save_mag_plot(M, path, title):
        plt.figure()
        plt.imshow(20*np.log10(M + 1e-6), aspect="auto", origin="lower")
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Frequency bin")
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(path, dpi=180)
        plt.close()

    save_mag_plot(mag, os.path.join(OUT_DIR, "degraded_spectrogram.png"), "Degraded (magnitude)")
    save_mag_plot(mag_smooth, os.path.join(OUT_DIR, "restored_spectrogram.png"), "Restored (smoothed magnitude)")

    # save audio artifacts
    save_wav(os.path.join(DATA_DIR, "clean.wav"), sr, clean)
    save_wav(os.path.join(DATA_DIR, "degraded.wav"), sr, degraded)

    # write report
    report = f"""# Mirror 05 — Paramount (Restoration Proof)

This run generates:
- `data/clean.wav` (synthetic clean signal)
- `data/degraded.wav` (noise + dropouts)
- `outputs/degraded_spectrogram.png`
- `outputs/restored_spectrogram.png`

**What this proves:** an end-to-end restoration pipeline exists:
signal generation → degradation → analysis (spectral magnitude) → restoration (smoothing) → artifacts on disk.
"""
    with open(os.path.join(OUT_DIR, "restoration_report.md"), "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
