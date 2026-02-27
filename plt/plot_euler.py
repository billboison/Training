import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLT_DIR = os.path.join(BASE_DIR, "plt")

def analytical(t):
    return np.exp(-3.0 * t)

def rms_error(t_num, x_num):
    x_exact = analytical(t_num)
    return math.sqrt(np.mean((x_num - x_exact) **2))

datasets = {}
for z in range(7):
    path = os.path.join(DATA_DIR, f"run_z{z}", "output.dat")
    if not os.path.exists(path):
        print(f"Skipping {path}")
        continue
    data = np.loadtxt(path, comments="#")
    t, x_num = data[:, 0], data[:, 1]
    datasets[z] = (t, x_num)

fig1, ax1 = plt.subplots(figsize=(9, 5))

t_fine = np.linspace(0, 9, 2000)
ax1.plot(t_fine, analytical(t_fine),
         "k-", linewidth=2.5, label="Analytical")

for z in sorted(datasets):
    t, x_num = datasets[z]
    stride = max(1, len(t) // 800)
    ax1.plot(t[::stride], x_num[::stride],
             label=f"dt = 10^{-z}")

ax1.set_xlabel("t")
ax1.set_ylabel("x(t)")
ax1.set_title("Explicit Euler: dx/dt = -3x")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()
fig1.savefig(os.path.join(PLT_DIR, "solutions.png"), dpi=150)
print("Saved solutions.png")

dts = []
errors = []
for z in sorted(datasets):
    t, x_num = datasets[z]
    dts.append(10**(-z))
    errors.append(rms_error(t, x_num))

fig2, ax2 = plt.subplots(figsize=(7, 5))
ax2.loglog(dts, errors, "o-", linewidth=2, markersize=7)
ax2.set_xlabel("dt")
ax2.set_ylabel("RMS Error")
ax2.set_title("Convergence of Explicit Euler")
ax2.grid(True)
fig2.tight_layout()
fig2.savefig(os.path.join(PLT_DIR, "convergence.png"), dpi=150)
print("Saved convergence.png")
