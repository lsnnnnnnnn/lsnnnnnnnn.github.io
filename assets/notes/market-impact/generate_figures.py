"""Analytical illustrations for the market-impact blog; no market data used.

Run with Python, NumPy, and Matplotlib. Extrema are enclosed using exact
rational Bernstein subdivision, independently of the plotted sample grid.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import heapq
import json
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
PREVIEW = Path(tempfile.gettempdir()) / "market-impact-blog-previews"
PREVIEW.mkdir(parents=True, exist_ok=True)
BLUE, RED, GREEN, PURPLE = "#6FA7CA", "#E47173", "#75C077", "#B99CD3"
INK, MUTED, GRID = "#222222", "#626262", "#ECECEC"
plt.rcParams.update({
    "font.family": ["DejaVu Sans", "Arial", "sans-serif"], "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": "#888888", "axes.linewidth": .85,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.axisbelow": True,
    "svg.fonttype": "none", "figure.facecolor": "white",
    "axes.facecolor": "white",
})

A = (1, 2, 5, 6)
B = (1, 3, 4, 6)
POWER = (F(0), F(1, 16), F(-2, 16), F(-1, 16), F(2, 16))


def polynomial(z):
    return z * (1 - 2*z) * (1 - z*z) / 16


def quadratic_cost(slots, z):
    # Four equal normalized fills, including the identical diagonal term.
    return sum(z ** abs(t-s) for t in slots for s in slots) / F(32)


def half_split(b):
    rows = [b]
    while len(rows[-1]) > 1:
        rows.append(tuple((u+v)/2 for u, v in zip(rows[-1], rows[-1][1:])))
    return tuple(row[0] for row in rows), tuple(row[-1] for row in rows[::-1])


def exact_maximum(power, tolerance=F(1, 10**13)):
    """Bound a polynomial's maximum on [0,1] by rational Bernstein hulls."""
    n = len(power)-1
    b = tuple(sum(power[k]*F(comb(i, k), comb(n, k)) for k in range(i+1))
              for i in range(n+1))
    best, location = max((b[0], F(0)), (b[-1], F(1)))
    heap, serial = [], 0
    heapq.heappush(heap, (-max(b), serial, F(0), F(1), b))
    splits = 0
    while -heap[0][0] - best > tolerance:
        _, _, lo, hi, coeff = heapq.heappop(heap)
        left, right = half_split(coeff)
        mid = (lo+hi)/2
        if left[-1] > best:
            best, location = left[-1], mid
        for low, high, child in ((lo, mid, left), (mid, hi, right)):
            serial += 1
            if max(child) >= best:
                heapq.heappush(heap, (-max(child), serial, low, high, child))
        splits += 1
        if splits > 10000:
            raise RuntimeError("Exact subdivision did not reach the requested precision")
    upper = -heap[0][0]
    return best, upper, location, splits


def finish(fig, name, title, description):
    path = OUT / f"{name}.svg"
    fig.savefig(path, bbox_inches="tight", pad_inches=.18,
                metadata={"Date": "2026-11-17", "Title": title,
                          "Description": description,
                          "Creator": "Matplotlib; generate_figures.py"})
    raw = path.read_text()
    at = raw.index(">", raw.index("<svg "))
    raw = raw[:at] + ' role="img" aria-labelledby="figure-title figure-desc"' + raw[at:]
    at = raw.index(">", raw.index("<svg "))
    raw = (raw[:at+1] + f'\n<title id="figure-title">{escape(title)}</title>'
           + f'\n<desc id="figure-desc">{escape(description)}</desc>' + raw[at+1:])
    path.write_text(raw)
    ET.parse(path)
    fig.savefig(PREVIEW / f"{name}.png", dpi=160, bbox_inches="tight", pad_inches=.18)
    plt.close(fig)


def schedule_recovery():
    fig = plt.figure(figsize=(8, 6.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[.80, 1.15], hspace=.64)
    ax = fig.add_subplot(gs[0])
    ax.set_title("A. Same order size and deadline, different spacing", loc="left", fontsize=12.5, pad=15)
    for y, slots, color, label in ((1, A, BLUE, "Schedule A"), (0, B, PURPLE, "Schedule B")):
        ax.plot([1, 6], [y, y], color="#CFD5DA", lw=1.2, zorder=0)
        ax.scatter(range(1, 7), [y]*6, marker="s", s=300, facecolor="white", edgecolor="#CFD5DA", lw=1.1)
        ax.scatter(slots, [y]*4, marker="s", s=300, color=color, edgecolor=INK, lw=.5, zorder=3)
        ax.text(.55, y, label, ha="right", va="center", fontsize=11, color=INK)
    ax.set_xlim(.8, 6.2)
    ax.set_ylim(-.48, 1.48)
    ax.set_xticks(range(1, 7))
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_xlabel("Execution slot", labelpad=9)
    ax.text(.5, -.38, "Each filled square = 2,500 shares. Both schedules buy 10,000 shares.",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10.2)
    ax = fig.add_subplot(gs[1])
    k = np.linspace(0, 5, 301)
    for z, color, label in ((.25, GREEN, "Faster recovery: z = 0.25"), (.75, RED, "Slower recovery: z = 0.75")):
        ax.plot(k, z**k, color=color, lw=2.8, label=label)
        ax.scatter(np.arange(6), z**np.arange(6), color=color, s=30, zorder=4)
    ax.set_title("B. How much of one trade's effect remains?", loc="left", fontsize=12.5, pad=13)
    ax.set_xlabel("Time since the trade, in slot intervals")
    ax.set_ylabel("Fraction remaining, $z^k$")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.06)
    ax.set_xticks(range(6))
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.grid(color=GRID)
    ax.legend(frameon=False, loc="upper right", fontsize=10.6)
    ax.text(0, -.32, "Analytical example. Recovery rates are assumptions, not market estimates.",
            transform=ax.transAxes, color=MUTED, fontsize=10.2)
    fig.subplots_adjust(left=.17, right=.97)
    finish(fig, "schedule-recovery", "Equal-sized orders can differ in the timing of their fills",
           "Schedule A trades 2500 shares at slots 1, 2, 5, 6; schedule B at slots 1, 3, 4, 6. "
           "Both trade 10000 shares within six slots. The lower panel shows analytical residual "
           "impact fractions z to the power k for assumed retention factors 0.25 and 0.75.")


def ranking_reversal():
    fig, ax = plt.subplots(figsize=(8, 4.9))
    z = np.linspace(0, 1, 1001)
    d = polynomial(z)
    ax.fill_between(z, 0, d, where=d >= 0, color=PURPLE, alpha=.23)
    ax.fill_between(z, 0, d, where=d <= 0, color=BLUE, alpha=.23)
    ax.plot(z, d, color="#58536C", lw=2.6)
    ax.axhline(0, color="#888888", lw=1)
    ax.scatter([0, .5, 1], [0, 0, 0], s=43, facecolor="white", edgecolor=INK, zorder=6)
    for x, y, label, xytext, color in [
        (.25, 15/2048, "$15/2048$", (.10, .0114), PURPLE),
        (.75, -21/2048, "$-21/2048$", (.72, -.0144), BLUE),
    ]:
        ax.scatter([x], [y], color=color, edgecolor=INK, s=45, lw=.6, zorder=6)
        ax.annotate(label, (x, y), xytext=xytext, fontsize=11,
                    arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1})
    ax.text(.24, .0032, "B costs less", ha="center", color="#79618F", fontsize=11)
    ax.text(.77, -.0045, "A costs less", ha="center", color="#477E9C", fontsize=11)
    ax.set_title("The preferred schedule changes with recovery", loc="left", fontsize=12.5, pad=34)
    ax.set_xlabel("One-slot retention, z   (larger z means slower recovery)", labelpad=10)
    ax.set_ylabel("Normalized cost difference, A minus B")
    ax.set_xlim(0, 1)
    ax.set_ylim(-.016, .014)
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_yticks([-.01, 0, .01])
    ax.grid(color=GRID)
    ax.text(.5, 1.015, r"$d(z)=z(1-2z)(1-z^2)/16$", transform=ax.transAxes,
            ha="center", fontsize=12)
    ax.text(0, -.28, "At z = 0 and z = 1 the costs tie. Testing only those endpoints misses the reversal.",
            transform=ax.transAxes, color=MUTED, fontsize=10.2)
    fig.subplots_adjust(left=.16, right=.97, bottom=.24, top=.82)
    finish(fig, "ranking-reversal", "Recovery uncertainty can reverse the ranking of two schedules",
           "The exact normalized cost difference d(z) equals z times (1-2z) times (1-z squared), "
           "divided by 16. It is positive below one half, negative above one half, and zero at "
           "zero, one half, and one. Exact values at one quarter and three quarters are "
           "15/2048 and -21/2048. This is an analytical construction, not measured execution cost.")


def sensitivity_frontier(maxd, mind):
    M = np.linspace(0, 100, 501)
    upper = -.5+.1+M*maxd
    lower = -.5-.1+M*mind
    threshold = .4/maxd
    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.fill_between(M, lower, upper, color=BLUE, alpha=.18, label="Range over all recovery rates and residuals")
    ax.plot(M, upper, color=RED, lw=2.8, label="Upper bound on A minus B")
    ax.plot(M, lower, color=BLUE, lw=1.8, ls="--", label="Lower bound")
    ax.axhline(0, color="#888888", lw=1)
    ax.axvline(threshold, color=PURPLE, lw=1.3, ls=":")
    ax.scatter([threshold], [0], color=RED, edgecolor=INK, s=42, lw=.6, zorder=5)
    ax.annotate(f"Strict advantage ends at\nM = {threshold:.2f} bp", xy=(threshold, 0),
                xytext=(8, .37), fontsize=10.8,
                arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.1})
    ax.text(22, -.58, "A costs less throughout\nthe assumed range", ha="center", color="#477E9C", fontsize=10.4)
    ax.text(82, .34, "Either ranking is possible", ha="center", color=MUTED, fontsize=10.2)
    ax.set_title("How much impact uncertainty can the decision tolerate?", loc="left", fontsize=12.5, pad=15)
    ax.set_xlabel("Assumed impact amplitude, M (basis points)", labelpad=10)
    ax.set_ylabel("Cost difference, A minus B (basis points)")
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.77, .66)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(color=GRID)
    ax.legend(frameon=False, loc="lower left", fontsize=9.8)
    ax.text(0, -.23, "Assumed baseline advantage of A: 0.5 bp. Combined residual uncertainty: ±0.1 bp.",
            transform=ax.transAxes, color=MUTED, fontsize=10.1)
    ax.text(0, -.31, "Constructed sensitivity calculation; this is not a calibrated market confidence interval.",
            transform=ax.transAxes, color=MUTED, fontsize=10.1)
    fig.subplots_adjust(left=.16, right=.97, bottom=.26, top=.90)
    finish(fig, "sensitivity-frontier", "A conditional decision frontier under recovery uncertainty",
           "The assumed baseline cost difference is -0.5 basis points with combined residual "
           "uncertainty of plus or minus 0.1 basis points. Across retention z in [0,1], the upper "
           "cost difference is -0.4 plus M times max d(z), and the lower is -0.6 plus M times min d(z). "
           f"The upper bound crosses zero at approximately {threshold:.2f} basis points of amplitude. "
           "The shaded interval represents assumed model uncertainty, not a statistical confidence interval.")


def rational_record(x):
    return {"fraction": str(x), "decimal": float(x)}


if __name__ == "__main__":
    exact_points = {F(0): F(0), F(1,4): F(15,2048), F(1,2): F(0),
                    F(3,4): F(-21,2048), F(1): F(0)}
    for z, expected in exact_points.items():
        assert polynomial(z) == expected
        assert quadratic_cost(A, z)-quadratic_cost(B, z) == expected
    maximum_lo, maximum_hi, argmax, max_splits = exact_maximum(POWER)
    negative_lo, negative_hi, argmin, min_splits = exact_maximum(tuple(-p for p in POWER))
    minimum_lo, minimum_hi = -negative_hi, -negative_lo
    threshold_lo, threshold_hi = F(2,5)/maximum_hi, F(2,5)/maximum_lo
    verification = {
        "kind": "analytical construction; no market observations or account runs",
        "schedules": {"A": A, "B": B, "shares_per_child": 2500, "total_shares": 10000},
        "cost_definition": "half of x^T K_z x, x_i=1/4 at each scheduled slot; K_ij=z^abs(i-j)",
        "difference_power_coefficients": [str(p) for p in POWER],
        "exact_fraction_checks": {str(z):str(v) for z,v in exact_points.items()},
        "exact_method": "Bernstein convex-hull enclosure, recursive midpoint de Casteljau subdivision, Fraction arithmetic",
        "absolute_extremum_tolerance": "1/10000000000000",
        "maximum": {"lower": rational_record(maximum_lo), "upper": rational_record(maximum_hi),
                    "best_evaluated_z": rational_record(argmax), "subdivisions": max_splits},
        "minimum": {"lower": rational_record(minimum_lo), "upper": rational_record(minimum_hi),
                    "best_evaluated_z": rational_record(argmin), "subdivisions": min_splits},
        "sensitivity_assumptions_bp": {"baseline_A_minus_B": -.5, "combined_residual_radius": .1,
                                       "amplitude_range": [0,100]},
        "strict_advantage_threshold_bp": {"lower": rational_record(threshold_lo), "upper": rational_record(threshold_hi)},
        "upper_bound": "-0.4 + M * max d(z)",
        "lower_bound": "-0.6 + M * min d(z)",
    }
    (OUT / "verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    schedule_recovery()
    ranking_reversal()
    sensitivity_frontier(float(maximum_hi), float(minimum_lo))
    print(json.dumps({"maximum": [float(maximum_lo),float(maximum_hi)],
                      "minimum": [float(minimum_lo),float(minimum_hi)],
                      "threshold_bp": [float(threshold_lo),float(threshold_hi)],
                      "previews": str(PREVIEW)}, indent=2))
