# 10 — NASA · Telemetry → Orchestration

**Goal:** Convert telemetry signals into orchestration-ready outputs (plots + proof JSON).

## What this proves
- You can ingest structured telemetry (CSV)
- Transform signals into interpretable visual artifacts
- Emit machine-verifiable proof for reproducibility

## Run
```bash
python run.py

### 3) (Optional but recommended) Fix the company name spelling in Northrop mirror README too
```bash
# if the file exists, this will replace "Northrop" with "Northrop Grumman" in that README
perl -pi -e 's/\bNorthrop\b/Northrop Grumman/g' 09_northrop/README.md 2>/dev/null || true
git add 10_nasa/README.md 09_northrop/README.md
git commit -m "Add NASA README and standardize Northrop Grumman name"
git pull --rebase origin main
git push origin main
pwd
.../beethoven-ai-final-symphony
cat > 10_nasa/README.md <<'EOF'
# 10 — NASA · Telemetry → Orchestration

**Goal:** Convert telemetry signals into orchestration-ready outputs (plots + proof JSON).

## What this proves
- Ingest structured telemetry (CSV)
- Transform signals into interpretable visual artifacts
- Emit machine-verifiable proof for reproducibility

## Run
```bash
python run.py

---

## 2️⃣ Verify the file exists (important)
```bash
ls -l 10_nasa/README.md
git add 10_nasa/README.md
git commit -m "Add NASA mirror README"
git pull --rebase origin main
git push origin main
beethoven-ai-final-symphony / 10_nasa / README.md
(base) Priyas-MacBook-Pro:beethoven-ai-final-symphony$
cat > 10_nasa/README.md <<'EOF'
# 10 — NASA · Telemetry → Orchestration

**Goal:** Convert telemetry signals into orchestration-ready outputs (plots + proof JSON).

## What this proves
- Ingest structured telemetry (CSV)
- Transform signals into interpretable visual artifacts
- Emit machine-verifiable proof for reproducibility

## Run
```bash
python run.py

👉 **Important:**  
- Paste  
- Press **Enter**  
- You should return to a normal prompt  
If not, something went wrong — stop and tell me.

---

## 3️⃣ Verify (no guessing)
```bash
ls -l 10_nasa/README.md
git add 10_nasa/README.md
git commit -m "Add NASA mirror README"
git pull --rebase origin main
git push origin main
