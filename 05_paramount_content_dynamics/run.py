import os, csv, json, random
from datetime import datetime, timedelta

OUTDIR = "outputs"
os.makedirs(OUTDIR, exist_ok=True)

# Generate a realistic-ish "engagement" time series (synthetic but valid proof artifact)
random.seed(5)
start = datetime.now() - timedelta(days=29)

rows = []
base = 120
for i in range(30):
    day = start + timedelta(days=i)
    # weekly seasonality + noise + small trend
    weekly = 18 * (1 if day.weekday() in (4,5,6) else -0.3)
    trend = i * 0.8
    noise = random.randint(-12, 12)
    plays = max(0, int(base + weekly + trend + noise))
    likes = max(0, int(plays * random.uniform(0.08, 0.18)))
    shares = max(0, int(plays * random.uniform(0.01, 0.05)))
    completion_rate = round(random.uniform(0.62, 0.93), 3)
    rows.append([day.strftime("%Y-%m-%d"), plays, likes, shares, completion_rate])

csv_path = os.path.join(OUTDIR, "engagement_summary.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "plays", "likes", "shares", "completion_rate"])
    w.writerows(rows)

# Simple summary JSON (second artifact)
plays_vals = [r[1] for r in rows]
summary = {
    "days": len(rows),
    "plays_total": sum(plays_vals),
    "plays_avg": round(sum(plays_vals) / len(plays_vals), 2),
    "plays_min": min(plays_vals),
    "plays_max": max(plays_vals),
}
json_path = os.path.join(OUTDIR, "engagement_summary.json")
with open(json_path, "w") as f:
    json.dump(summary, f, indent=2)

# Optional plot PNG (third artifact)
try:
    import matplotlib.pyplot as plt
    dates = [r[0] for r in rows]
    plays = [r[1] for r in rows]
    plt.figure(figsize=(10,4))
    plt.plot(dates, plays)
    plt.xticks(rotation=45, ha="right")
    plt.title("Mirror 05 — Paramount: Engagement Over Time (Synthetic Proof)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, "engagement_over_time.png"), dpi=160)
    plt.close()
except Exception as e:
    # If matplotlib isn't available, we still have CSV+JSON proof
    with open(os.path.join(OUTDIR, "plot_warning.txt"), "w") as f:
        f.write(str(e))

print("Mirror 05 executed: outputs/engagement_summary.csv + .json (+ png if available)")
