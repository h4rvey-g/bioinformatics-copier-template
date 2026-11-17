# scripts/

Put small helper scripts and project utilities here if your workflow needs them.

## Plotting

Use `plot_style.py` for all new or updated plots. It contains the shared
Matplotlib configuration and 16 panel sizes in inches, converted from millimetres.

For scripts executed by path (for example, `python scripts/my_plot.py`):

```python
import matplotlib.pyplot as plt
from plot_style import SUBPANEL_VERSIONS, apply_plot_style

# Apply after any other theme/style setup, before creating figures.
apply_plot_style()
fig, ax = plt.subplots(figsize=SUBPANEL_VERSIONS["w3_h2"], layout="constrained")
ax.plot([0, 1], [0, 1])
fig.savefig("figure.pdf")
plt.close(fig)
```

For notebooks or modules launched from the project root, import from
`scripts.plot_style` instead.

`PLOT_RC_PARAMS` is the authoritative plotting configuration. It enables
constrained layout globally; also specify `layout="constrained"` explicitly
when creating figures. Use this engine instead of `tight_layout()` or
`subplots_adjust()`.

**Font sizes are strict requirements, not adjustable defaults.** Inherit the
configured sizes for body text, axes/figure titles and labels, ticks, and
legends; do not override or scale them locally unless the user explicitly
requests a typography change. Overlap or clipping indicates a layout/design
problem or redundant content. Rearrange panels, split pages, reduce panel
density, or remove redundant wording while preserving required information.
Keep the configured sizes and selected physical figure dimensions, then
inspect the rendered output; `bbox_inches="tight"` changes those dimensions
and is not a substitute for fixing the layout.

Presets are named `wN_hM` where N is the width level (1–4) and M is the height
level (1–4). Higher numbers mean larger dimensions.

| Level | Width (mm) | Height (mm) |
| --- | --- | --- |
| 1 | 42 (4 per row) | 40 |
| 2 | 56 (3 per row) | 65 |
| 3 | 85 (2 per row) | 110 |
| 4 | 174 (full width) | 150 |

All 16 combinations are available, e.g. `w3_h2` (85 × 65 mm) or `w4_h3`
(174 × 110 mm). Start with the smallest preset that fits the content. Use
taller height levels (h3, h4) for heatmaps, dot plots, or multirow layouts.
Dimensions describe the whole canvas, including labels and legends. Check the
target journal's figure requirements before submission.

Exports default to transparent PDF. PDF/PS use TrueType fonts, SVG keeps text
as text, and rasterized layers export at 600 dpi. Use `rasterized=True` on
dense artists when needed; the defaults do not rasterize artists automatically.
The valid Matplotlib key is `savefig.transparent` (lowercase).
The generated Pixi environment includes Matplotlib. `apply_plot_style()`
registers the bundled Arial regular, bold, italic, and bold italic files from
`assets/fonts/arial/` for the current Python process. Keep that directory with
the project; no system font installation is needed. The fonts are copied
unchanged from `mscorefonts` and retain their license in
`assets/fonts/arial/LICENSE`.

For Nextflow plotting tasks, pass the helper and font directory as declared
inputs and retain the relative paths `scripts/plot_style.py` and
`assets/fonts/arial/` in the task directory.
