"""Shared publication plotting configuration; font sizes are mandatory."""

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager


PLOT_RC_PARAMS = {
    # Keep vector-export text editable in Adobe Illustrator.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica"],
    "font.size": 7,
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5,
    "legend.title_fontsize": 6.5,
    "figure.titlesize": 8,
    "figure.labelsize": 8,
    "axes.linewidth": 0.6,
    "grid.linewidth": 0.4,
    "lines.linewidth": 1.0,
    "lines.markersize": 4.0,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "figure.autolayout": False,
    "figure.constrained_layout.use": True,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.format": "pdf",
    "savefig.transparent": True,
}


def mm_to_inch(mm: float) -> float:
    """Convert millimetres to Matplotlib's figure-size units."""
    return mm / 25.4


_W = {1: 42, 2: 56, 3: 85, 4: 174}   # mm; wN = width level N
_H = {1: 40, 2: 65, 3: 110, 4: 150}  # mm; hN = height level N
SUBPANEL_VERSIONS = {
    f"w{w}_h{h}": (mm_to_inch(_W[w]), mm_to_inch(_H[h]))
    for w in range(1, 5)
    for h in range(1, 5)
}


def apply_plot_style() -> None:
    """Register bundled Arial and apply configuration after themes, before figures."""
    font_directory = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "arial"
    for filename in ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"):
        font_manager.fontManager.addfont(font_directory / filename)
    mpl.rcParams.update(PLOT_RC_PARAMS)
