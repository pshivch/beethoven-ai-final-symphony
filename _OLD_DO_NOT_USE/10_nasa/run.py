from pathlib import Path

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

# Count "artifact-like" outputs
exts = {".png", ".csv", ".json", ".wav", ".mid", ".midi", ".html", ".mp4"}
files = sorted([p for p in OUT.iterdir() if p.is_file() and p.suffix.lower() in exts])

print("✅ mirror runner")
print(f"Outputs folder: {OUT.resolve()}")
print(f"Artifacts ({len(files)}):")
for f in files:
    print(" -", f.name)

if len(files) == 0:
    raise SystemExit("❌ No artifacts found in outputs/. Generate or copy proof artifacts into outputs/ first.")
