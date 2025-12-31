import os, json
import numpy as np
import matplotlib.pyplot as plt

def main():
    os.makedirs("outputs", exist_ok=True)

    t = np.arange(0, 100)
    pan = np.sin(t / 10)
    elevation = np.cos(t / 15)

    plt.figure(figsize=(8,4))
    plt.plot(t, pan, label="pan")
    plt.plot(t, elevation, label="elevation")
    plt.title("Apple AR Conducting — Hand Pose Over Time")
    plt.xlabel("Time")
    plt.ylabel("Spatial Parameter")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/pan_over_time.png")
    plt.close()

    hand_pose = {
        "frames": int(len(t)),
        "pan_mean": float(np.mean(pan)),
        "elevation_mean": float(np.mean(elevation))
    }

    with open("outputs/hand_pose.json", "w") as f:
        json.dump(hand_pose, f, indent=2)

    print("Apple artifacts written to outputs/")

if __name__ == "__main__":
    main()
