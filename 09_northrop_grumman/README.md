## 09 northrop grumman

**Proof:** This mirror contains real artifacts committed to `outputs/`.

### How to run (proof)

```bash
cd 09_northrop_grumman
python run.py

---

## 🔧 FIX 10 — NASA (MAKE IT MATCH APPLE)

```bash
cat > 10_nasa/README.md << 'EOF'
## 10 nasa

**Proof:** This mirror contains real artifacts committed to `outputs/`.

### How to run (proof)

```bash
cd 10_nasa
python run.py

---

## ✅ VERIFY (must look the same as Apple)

Run:

```bash
sed -n '1,40p' 09_northrop_grumman/README.md
sed -n '1,40p' 10_nasa/README.md
git add 09_northrop_grumman/README.md 10_nasa/README.md
git commit -m "Align NG and NASA READMEs to standard proof template"
git push
git status
git add 09_northrop_grumman/README.md 10_nasa/README.md
git commit -m "Align NG and NASA READMEs to standard proof template"
git push
cat > 10_nasa/README.md << 'EOF'
