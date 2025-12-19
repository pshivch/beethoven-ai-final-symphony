# Mirror 05 — Paramount (Restoration Proof)

This run generates:
- `data/clean.wav` (synthetic clean signal)
- `data/degraded.wav` (noise + dropouts)
- `outputs/degraded_spectrogram.png`
- `outputs/restored_spectrogram.png`

**What this proves:** an end-to-end restoration pipeline exists:
signal generation → degradation → analysis (spectral magnitude) → restoration (smoothing) → artifacts on disk.
