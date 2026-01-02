# 05 — Paramount: Content Dynamics → Engagement Signals

**Proof:** This mirror contains real artifacts committed in `outputs/`.

## What this proves
- **Signal:** content interaction + engagement time-series
- **Model:** aggregation, normalization, simple dynamics modeling
- **Output:** structured engagement signals for downstream decision systems

## How to run
```bash
cd 05_paramount_content_dynamics
python run.py

### D) Remove `__pycache__` and stop it coming back
From repo root:
```bash
cd ~/beethoven-ai-final-symphony
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
grep -q "__pycache__/" .gitignore || echo "__pycache__/" >> .gitignore
grep -q "*.pyc" .gitignore || echo "*.pyc" >> .gitignore
git status
git add 05_paramount_content_dynamics/ .gitignore
git commit -m "Clean Mirror 05 README + fix run script"
git push
cd ..
ls
cd ~/beethoven-ai-final-symphony && git status
cd ~/beethoven-ai-final-symphony
pwd
cat > 05_paramount_content_dynamics/README.md <<'EOF'
# 05 — Paramount: Content Dynamics → Engagement Signals

**Proof:** This mirror contains real artifacts committed to `outputs/`.

**What this proves:**
- **Signal →** content interaction & engagement time-series  
- **Model →** aggregation, normalization, and simple dynamics modeling  
- **Output →** structured engagement signals for downstream decision systems  

## How to run (proof)
```bash
cd 05_paramount_content_dynamics
python run.py

### C) Commit + push the README fix
```bash
git add 05_paramount_content_dynamics/README.md
git commit -m "Fix Mirror 05 README formatting"
git push
printf "\n__pycache__/\n*.pyc\n" >> .gitignore
git add .gitignore
git commit -m "Ignore pycache"
git push
ls 05_paramount_content_dynamics/outputs
ls 06_netflix_orchestral_storytelling
ls 06_netflix_orchestral_storytelling
cd ~/beethoven-ai-final-symphony
pwd
…/beethoven-ai-final-symphony
cat > 05_paramount_content_dynamics/README.md <<'EOF'
# 05 — Paramount: Content Dynamics → Engagement Signals

**Proof:** This mirror contains real artifacts committed to `outputs/`.

**What this proves:**
- **Signal →** content interaction & engagement time-series
- **Model →** aggregation, normalization, and simple dynamics modeling
- **Output →** structured engagement signals for downstream decision systems

## How to run (proof)
```bash
cd 05_paramount_content_dynamics
python run.py

When you press Enter after `EOF`, **you will return to the prompt**.  
That means it worked.

---

## ✅ STEP 3 — Commit & push (real commands)

```bash
git add 05_paramount_content_dynamics/README.md
git commit -m "Fix Mirror 05 README formatting"
git push
ls 05_paramount_content_dynamics/outputs
ls 06_netflix_orchestral_storytelling
cd ~/beethoven-ai-final-symphony
cat > 05_paramount_content_dynamics/README.md <<'EOF'
# 05 — Paramount: Content Dynamics → Engagement Signals

**Proof:** This mirror contains real artifacts committed to `outputs/`.

**What this proves:**
- **Signal →** content interaction & engagement time-series
- **Model →** aggregation, normalization, and simple dynamics modeling
- **Output →** structured engagement signals for downstream decision systems

## How to run (proof)
```bash
cd 05_paramount_content_dynamics
python run.py

After you press Enter on the `EOF` line, you should immediately return to the normal `$` prompt.

### 4) Commit + push
```bash
git add 05_paramount_content_dynamics/README.md
git commit -m "Fix Mirror 05 README formatting"
git push
