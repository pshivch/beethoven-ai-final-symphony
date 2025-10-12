# Polyglot Orchestration Proof (Rust + C++ + Julia + Python)

**What it proves**
- Low-latency kernels in **Rust** (DTW-lite + variance)
- Performance-critical harmonic metric in **C++** (pybind11)
- Algorithmic composition primitive in **Julia**
- Thin **Python** layer orchestrating all 3 + emitting benchmarks & charts

**Run**
```bash
python -m pip install -r requirements.txt
# build Rust and C++ (see repo instructions below)
python orchestrate.py && python benchmarks.py
```

Artifacts: `artifacts/motifs.png`, `artifacts/metrics.json`

**CI**: GitHub Actions builds Rust/C++ modules, runs Julia via PyJulia, executes the pipeline, and publishes artifacts.
