"""Reproduce the analytical illustrations for the structured-dependence note.

Run with Python 3, NumPy, and Matplotlib. SVGs are written beside this script;
PNG previews are written to the system temporary directory. No simulated data.
"""
from itertools import combinations
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.ticker import ScalarFormatter
import numpy as np

OUT = Path(__file__).resolve().parent
PREVIEW = Path(tempfile.gettempdir()) / "comet-figure-previews"
PREVIEW.mkdir(exist_ok=True)
BLUE = "#6FA7CA"
RED = "#E47173"
GREEN = "#75C077"
PURPLE = "#B99CD3"
INK = "#222222"
MUTED = "#626262"
BORDER = "#888888"
LIGHT = "#CFD5DA"
GRID = "#ECECEC"
NODE_STYLES = {
    BLUE: ("#E7F2F9", "#4F8CA7"),
    RED: ("#FBEAEB", "#B45F66"),
    GREEN: ("#EDF6EA", "#5A9258"),
    PURPLE: ("#F1EAF6", "#8B739F"),
}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": BORDER, "axes.linewidth": .85,
    "axes.spines.top": True, "axes.spines.right": True,
    "axes.titleweight": "semibold", "axes.axisbelow": True,
    "svg.fonttype": "none", "svg.hashsalt": "structured-dependence-20261116",
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def finish(fig, name, title, description):
    path = OUT / f"{name}.svg"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.18,
                metadata={"Date": "2026-11-16", "Title": title,
                          "Description": description,
                          "Creator": "Matplotlib; generate_figures.py"})
    # Keep SVG labels as text and expose a readable description to assistive tools.
    raw = path.read_text()
    root_start = raw.index("<svg ")
    root_end = raw.index(">", root_start)
    raw = (raw[:root_end] + ' role="img" aria-labelledby="figure-title figure-desc"'
           + raw[root_end:])
    root_end = raw.index(">", root_start)
    from xml.sax.saxutils import escape
    raw = (raw[:root_end + 1]
           + f'\n <title id="figure-title">{escape(title)}</title>'
           + f'\n <desc id="figure-desc">{escape(description)}</desc>'
           + raw[root_end + 1:])
    path.write_text(raw)
    ET.parse(path)
    fig.savefig(PREVIEW / f"{name}.png", dpi=180, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def node(ax, xy, label, color, radius=0.18):
    fill, edge = NODE_STYLES[color]
    ax.add_patch(Circle(xy, radius, facecolor=fill, edgecolor=edge, lw=1.35, zorder=3))
    ax.text(*xy, label, color=INK, ha="center", va="center", fontsize=10.5, zorder=4)


def panel_frame(ax, xpad=0):
    ax.add_patch(FancyBboxPatch(
        (-xpad, 0), 1 + 2*xpad, 1, transform=ax.transAxes,
        boxstyle="round,pad=0.025,rounding_size=0.025",
        facecolor="white", edgecolor=BORDER, linewidth=.85,
        clip_on=False, zorder=-1,
    ))


def xor_figure():
    fig = plt.figure(figsize=(8.0, 7.3))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=0.40, wspace=0.30)
    left, right = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    for ax in [left, right]:
        ax.set_aspect("equal")
        ax.axis("off")
    left.set_title("A. The input variables", loc="left", fontsize=12.3, pad=11)
    apos = [(0, y) for y in [2.4, 1.6, 0.8, 0]]
    bpos = [(1.8, y) for y in [2.4, 1.6, 0.8, 0]]
    for a in apos:
        for b in bpos:
            left.plot([a[0], b[0]], [a[1], b[1]], color=LIGHT, lw=1.1, zorder=1)
    for i, (a, b) in enumerate(zip(apos, bpos), 1):
        node(left, a, f"A{i}", BLUE)
        node(left, b, f"B{i}", GREEN)
    left.text(0, 2.95, "Independent\nwithin A", ha="center", va="center", color=NODE_STYLES[BLUE][1], fontsize=10.5)
    left.text(1.8, 2.95, "Independent\nwithin B", ha="center", va="center", color=NODE_STYLES[GREEN][1], fontsize=10.5)
    left.text(0.9, -0.52, r"$B_i=A_i\oplus Z$", ha="center", fontsize=12)
    left.text(0.9, -0.94, r"Strong dependency graph $K_{4,4}$", ha="center", fontsize=10.3)
    left.text(0.9, -1.27, r"Fractional chromatic number $=2$", ha="center", fontsize=10.3)
    left.set_xlim(-0.50, 2.30)
    left.set_ylim(-1.48, 3.25)
    panel_frame(left, xpad=.30)

    right.set_title("B. The terms being averaged", loc="left", fontsize=12.3, pad=11)
    ypos = [(0, 2.15), (1.7, 2.15), (0, 0.45), (1.7, 0.45)]
    for a, b in combinations(ypos, 2):
        right.plot([a[0], b[0]], [a[1], b[1]], color=RED, alpha=.8, lw=1.5)
    for i, a in enumerate(ypos, 1):
        node(right, a, f"Y{i}", RED, .20)
    right.text(.85, 2.95, "Every term equals\nthe same hidden bit Z", color=NODE_STYLES[RED][1],
               ha="center", va="center", fontsize=10.5)
    right.text(.85, -0.20, r"$Y_i=\mathbf{1}\{A_i\ne B_i\}=Z$", ha="center", fontsize=12)
    right.text(.85, -0.68, r"Term dependency graph $K_4$", ha="center", fontsize=10.3)
    right.text(.85, -1.03, r"Fractional chromatic number $=4$", ha="center", fontsize=10.3)
    right.set_xlim(-.55, 2.25)
    right.set_ylim(-1.48, 3.25)
    panel_frame(right, xpad=.30)

    ax = fig.add_subplot(gs[1, :])
    m = np.arange(1, 41)
    ax.plot(m, np.full_like(m, .5, dtype=float), color=BLUE, lw=2.7,
            label=r"Exact tail probability $1/2$")
    ax.plot(m, np.exp(-m / 8), color=RED, lw=2.4, ls="--",
            label=r"Invalid formula $e^{-m/8}$")
    ax.scatter([6], [np.exp(-6/8)], s=35, color=RED, edgecolor=NODE_STYLES[RED][1], linewidth=.8, zorder=5)
    ax.annotate("Already fails at m = 6", xy=(6, np.exp(-6/8)), xytext=(12, .74),
                fontsize=10.5, color=NODE_STYLES[RED][1],
                arrowprops={"arrowstyle": "->", "color": NODE_STYLES[RED][1], "lw": 1.2})
    ax.set_title(r"C. Can the average concentrate when $f=mZ$?", loc="left", fontsize=12.3, pad=10)
    ax.set_xlabel("Number of paired comparisons, m")
    ax.set_ylabel("Tail probability")
    ax.set_xlim(1, 40)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.grid(color=GRID, linewidth=.65, zorder=0)
    ax.legend(loc="upper right", frameon=False, fontsize=10.3)
    ax.text(0, -.37, r"Event: $f-\mathbb{E}f\geq m/2$. Analytical construction, not simulation.",
            transform=ax.transAxes, color=MUTED, fontsize=10)
    finish(fig, "xor-common-bit", "One hidden bit defeats a naive coloring bound",
           "The input vector has a valid complete bipartite dependency graph with two colors, "
           "but each pairwise comparison equals the same hidden bit. The comparison terms form "
           "a clique. For m comparisons the exact upper tail probability is one half, while "
           "the incorrectly applied coloring formula exp(-m/8) falls below it at m=6.")


def covers_figure():
    fig = plt.figure(figsize=(8.0, 5.8))
    gs = fig.add_gridspec(2, 1, height_ratios=[.95, 1.4], hspace=.45)
    ax = fig.add_subplot(gs[0])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("A. One triangle and six isolated vertices", loc="left", fontsize=12.4, pad=10)
    tri = [(0, 0), (.65, 1), (1.3, 0)]
    for a, b in combinations(tri, 2):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=BLUE, lw=2)
    for i, xy in enumerate(tri, 1):
        node(ax, xy, str(i), BLUE, .17)
    for i, x in enumerate(np.linspace(2.5, 7, 6), 4):
        node(ax, (x, .38), str(i), GREEN, .17)
    ax.text(3.5, -.40, "Node oscillations are all c = 1", ha="center", fontsize=10.6, color=MUTED)
    ax.set_xlim(-.3, 7.3)
    ax.set_ylim(-.7, 1.35)
    panel_frame(ax)
    ax = fig.add_subplot(gs[1])
    vals = [27, 81/4, (np.sqrt(11)+1)**2, 15]
    labels = ["Janson", "Zhang's example cover", "Alternative feasible cover", "Independent components"]
    bars = ax.barh(np.arange(4), vals, height=.56,
                   color=[BLUE, RED, GREEN, PURPLE],
                   edgecolor=[NODE_STYLES[c][1] for c in [BLUE, RED, GREEN, PURPLE]],
                   linewidth=1, zorder=2)
    ax.set_yticks(np.arange(4), labels, fontsize=10.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 30)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xlabel(r"Valid denominator $D$ in $\exp(-2t^2/D)$")
    ax.grid(axis="x", color=GRID, zorder=0)
    ax.tick_params(axis="y", length=0)
    ax.set_title("B. Smaller denominators give tighter bounds", loc="left", fontsize=12.4, pad=13)
    for bar, val, label in zip(bars, vals, ["27", "20.25", "18.63", "15"]):
        ax.text(val+.35, bar.get_y()+bar.get_height()/2, label, va="center", fontsize=10.6, color=INK)
    ax.text(0, -.37, "These are valid constructions, not claims of global optimality.",
            transform=ax.transAxes, fontsize=10, color=MUTED)
    fig.subplots_adjust(left=.30, right=.95)
    finish(fig, "cover-costs", "Different ways to use the same dependency graph",
           "For a triangle and six isolated vertices, with all coordinate oscillations one, "
           "the Janson denominator is 27. Zhang's Example 2.7 gives the feasible value 81/4, "
           "or 20.25. Another feasible forest cover gives (sqrt(11)+1)^2, about 18.63. "
           "Using independence between connected components gives 15. Smaller valid "
           "denominators yield tighter exponential tail bounds; no optimum is asserted.")


def cancellation_figure():
    fig = plt.figure(figsize=(8.0, 7.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.12], hspace=.56)
    ax = fig.add_subplot(gs[0])
    ax.axis("off")
    ax.set_title("A. Add four neighboring terms, then collect each source", loc="left", fontsize=12.4, pad=15)
    xs = np.arange(5) * 1.1
    for i, x in enumerate(xs):
        node(ax, (x, 2.0), f"Z{i}", PURPLE, .21)
    ax.text(-.52, 2.0, "Independent\nfair bits", ha="right", va="center", fontsize=10.5, color=NODE_STYLES[PURPLE][1])
    for y, coeff, color in [(1.05, [-1, 0, 0, 0, 1], BLUE), (.10, [1, 2, 2, 2, 1], RED)]:
        for x, value in zip(xs, coeff):
            active = value != 0
            ax.plot([x, x], [1.7, y+.23], lw=1.2,
                    color=color if active else LIGHT, zorder=0, alpha=.65)
            ax.add_patch(Circle((x, y), .22, facecolor=NODE_STYLES[color][0] if active else "#F6F6F6",
                                edgecolor=NODE_STYLES[color][1] if active else "#B8B8B8",
                                linestyle="-" if active else "--", lw=1.3, zorder=2))
            ax.text(x, y, f"{value:+d}" if value else "0", ha="center", va="center",
                    color=INK if active else MUTED, fontsize=11, zorder=3)
    ax.text(-.52, 1.05, "Signed differences\nnet source loads", ha="right", va="center", color=NODE_STYLES[BLUE][1], fontsize=10.5)
    ax.text(-.52, .1, "Centered sums\nnet source loads", ha="right", va="center", color=NODE_STYLES[RED][1], fontsize=10.5)
    ax.text(2.2, -.55, r"$\sum_{i=1}^{4}(Z_i-Z_{i-1})=Z_4-Z_0$", ha="center", fontsize=12, color=INK)
    ax.text(2.2, -.98, "For centered sums, loads act on Zj − 1/2.", ha="center", fontsize=10.3, color=MUTED)
    ax.set_xlim(-1.85, 4.9)
    ax.set_ylim(-1.18, 2.4)
    panel_frame(ax)

    ax = fig.add_subplot(gs[1])
    n = np.arange(2, 257)
    minus = 1/(2*n**2)
    plus = (4*n-2)/(4*n**2)
    ax.loglog(n, plus, color=RED, lw=2.7, label=r"Centered sums: $(4n-2)/(4n^2)$")
    ax.loglog(n, minus, color=BLUE, lw=2.7, ls="--", label=r"Differences: $1/(2n^2)$")
    ax.set_title("B. Same path graph and node marginals, different averaging", loc="left", fontsize=12.4, pad=12)
    ax.set_xlabel("Number of terms, n")
    ax.set_ylabel("Exact variance of the mean")
    ax.set_xlim(2, 256)
    ax.set_xticks([2, 4, 8, 16, 32, 64, 128, 256])
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(which="major", color=GRID)
    ax.legend(loc="upper right", frameon=False, fontsize=10.4)
    ax.text(0, -.33, "Both node laws: P(−1) = P(+1) = 1/4 and P(0) = 1/2. Analytical curves.",
            transform=ax.transAxes, fontsize=10, color=MUTED)
    finish(fig, "source-cancellation", "A dependency graph does not record source cancellation",
           "For four differences Zi-Z(i-1), collecting source coefficients leaves -1 on Z0, "
           "+1 on Z4, and zero on all internal sources. For four centered sums "
           "Zi+Z(i-1)-1, the internal source coefficients are two. Both processes have "
           "the same path dependency graph and node marginals. The exact variance of "
           "their means is respectively 1/(2n^2) and (4n-2)/(4n^2).")


if __name__ == "__main__":
    xor_figure()
    covers_figure()
    cancellation_figure()
    print(f"SVGs: {OUT}")
    print(f"PNG previews: {PREVIEW}")
