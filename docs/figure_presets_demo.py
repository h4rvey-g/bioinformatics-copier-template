"""Before/after demo: free-form AI sizing vs. the wN_hM figure presets (bar chart)."""

import io
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "template" / "scripts"))
from plot_style import SUBPANEL_VERSIONS, apply_plot_style, mm_to_inch  # noqa: E402

PRESET = "w3_h2"  # 85 x 65 mm
W_MM, H_MM = (v * 25.4 for v in SUBPANEL_VERSIONS[PRESET])
groups = ["Control", "Drug A", "Drug B", "Drug A+B"]
reps = np.array([[1.17, 0.80, 1.04], [1.55, 1.82, 2.10], [1.20, 1.47, 1.37], [3.01, 3.16, 3.94]])  # 3 replicates per group
mean, sd = reps.mean(1), reps.std(1, ddof=1)


def to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, transparent=False, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return plt.imread(buf)


# --- Before: typical AI default -- big canvas, default 10 pt text, thin bars, wordy ---
mpl.rcdefaults()
big_w = 10  # inches; later squeezed into the 85 mm slot
fig, ax = plt.subplots(figsize=(big_w, big_w * H_MM / W_MM))
ax.bar(groups, mean, width=0.3, yerr=sd, capsize=4, color="C0", label="Mean ± SD")
for i, (m, s) in enumerate(zip(mean, sd)):
    ax.text(i, m + s + 0.1, f"{m:.2f} ± {s:.2f}", ha="center")
ax.set_ylim(0, mean.max() * 2.4)
ax.set_xlabel("Treatment condition")
ax.set_ylabel("Relative expression level (fold change vs. control)")
ax.set_title("Relative expression of Gene X across different treatment conditions", fontsize=12, pad=22)
ax.text(0.5, 1.02, "Bar height = mean of three biological replicates; error bars = SD", transform=ax.transAxes, ha="center", fontsize=9)
ax.grid(alpha=.3)
ax.legend(loc="upper left")
fig.text(0.5, 0.01, "Note: data are mean ± SD (n = 3). Significance by one-way ANOVA with Tukey's post hoc test; "
         "* p < 0.05, ** p < 0.01.", ha="center", fontsize=8)
before = to_img(fig)

# --- After: preset canvas + mandatory font sizes ---
apply_plot_style()
fig, ax = plt.subplots(figsize=SUBPANEL_VERSIONS[PRESET], layout="constrained")
colors = ["#999999", "#E69F00", "#56B4E9", "#009E73"]
ax.bar(groups, mean, width=0.5, color=colors, yerr=sd, capsize=3.5,
       error_kw={"lw": 1.0, "capthick": 1.0})
for i, r in enumerate(reps):
    ax.scatter(i + np.linspace(-.13, .13, 3), r, s=12, color="k", ec="white", lw=0.4, zorder=3)
for i, star in [(1, "*"), (2, "*"), (3, "**")]:
    ax.text(i, max(mean[i] + sd[i], reps[i].max()) + .1, star, ha="center", va="bottom")
ax.set_ylim(0, mean.max() * 1.25)
ax.set_ylabel("Relative expression")
ax.spines[["top", "right"]].set_visible(False)
after = to_img(fig)

# --- Composite: both panels shown at the same physical size (85 x 65 mm) ---
M, GAP, HEAD, FOOT = 6, 28, 12, 14  # mm
CW, CH = 2 * M + 2 * W_MM + GAP, HEAD + H_MM + FOOT + 2
comp = plt.figure(figsize=(mm_to_inch(CW), mm_to_inch(CH)), facecolor="white", layout="none")


def box(x_mm, img, head, foot, color):
    ax = comp.add_axes([x_mm / CW, FOOT / CH, W_MM / CW, H_MM / CH])
    ax.imshow(img, interpolation="lanczos", aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False, ec=color, lw=1.2, clip_on=False))
    for s in ax.spines.values():
        s.set_visible(False)
    cx = (x_mm + W_MM / 2) / CW
    comp.text(cx, (FOOT + H_MM + 3) / CH, head, ha="center", va="bottom", fontsize=9, fontweight="bold", color=color)
    comp.text(cx, (FOOT - 2) / CH, foot, ha="center", va="top", fontsize=7, color="#444444")


box(M, before, "Before: free-form size & text", f"10 in canvas, 10 pt text, squeezed to {W_MM:.0f} mm\n→ effective text ≈ {10 * W_MM / 254:.1f} pt, bars sparse", "#C0392B")
box(M + W_MM + GAP, after, f"After: preset {PRESET}", f"{W_MM:.0f} × {H_MM:.0f} mm canvas, 6.5 / 7 / 8 pt text\nno rescaling, bars fill the canvas", "#1E8449")

ay = (FOOT + H_MM / 2) / CH
comp.add_artist(FancyArrowPatch(((M + W_MM + 4) / CW, ay), ((M + W_MM + GAP - 4) / CW, ay), transform=comp.transFigure,
                                arrowstyle="simple,head_width=14,head_length=14,tail_width=6", color="#34495E", lw=0))
comp.text((M + W_MM + GAP / 2) / CW, ay + 8 / CH, "preset", ha="center", va="bottom", fontsize=8, color="#34495E")
comp.savefig(Path(__file__).with_name("figure_presets_demo.png"), dpi=300, transparent=False, facecolor="white")
print("ok", CW, CH)
