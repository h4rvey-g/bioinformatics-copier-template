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


SUBPANEL_VERSIONS = {
    "v_quarter": (mm_to_inch(42), mm_to_inch(38)),
    "v_third": (mm_to_inch(56), mm_to_inch(48)),
    "v_half_or_single": (mm_to_inch(85), mm_to_inch(65)),
    "v_wide": (mm_to_inch(114), mm_to_inch(60)),
    "v_full": (mm_to_inch(174), mm_to_inch(85)),
    "v_half_tall": (mm_to_inch(85), mm_to_inch(110)),
    "v_full_tall": (mm_to_inch(174), mm_to_inch(150)),
}


def apply_plot_style() -> None:
    """Register bundled Arial and apply configuration after themes, before figures."""
    font_directory = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "arial"
    for filename in ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"):
        font_manager.fontManager.addfont(font_directory / filename)
    mpl.rcParams.update(PLOT_RC_PARAMS)
