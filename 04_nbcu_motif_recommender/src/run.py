import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)

motifs = ["Action", "Drama", "Suspense", "Romance"]
scores = [0.82, 0.67, 0.91, 0.55]

df = pd.DataFrame({"motif": motifs, "score": scores})
df.to_csv("outputs/motif_recommendations.csv", index=False)

plt.figure()
plt.bar(motifs, scores)
plt.title("NBCU Motif Recommendation Scores")
plt.ylabel("Engagement Score")
plt.savefig("outputs/motif_scores.png")
plt.close()

print("DONE")
