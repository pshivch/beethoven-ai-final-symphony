import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 300)
y = np.sin(x) + 0.2*np.sin(3*x)

plt.figure()
plt.plot(x, y)
plt.title("Warner Mirror Proof: Tension Curve (Executable)")
plt.xlabel("time")
plt.ylabel("tension")
plt.tight_layout()
plt.savefig("outputs/warner_tension_curve.png", dpi=200)
print("Wrote outputs/warner_tension_curve.png")
