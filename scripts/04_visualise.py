"""
Phase 4 — Visualisations for Datos que Hablan.

Reads the clean dataset and produces five charts:
  1. Income distribution by country (box plot)
  2. Age vs. monthly savings (scatter + trend line)
  3. Spending breakdown by category (bar)
  4. Financial satisfaction by AI tool usage (bar)
  5. Housing burden by country (bar)

Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

DATA_PATH = "data/latam_finanzas_clean.csv"
CHARTS_DIR = "charts"
SOURCE_NOTE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

# --- Palette (validated categorical / sequential / status slots) ---
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

CATEGORICAL = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948"]
COUNTRY_ORDER = ["Argentina", "Brasil", "Chile", "Colombia", "México", "Perú"]
COUNTRY_COLOR = dict(zip(COUNTRY_ORDER, CATEGORICAL))

SEQ_BLUE_LOW, SEQ_BLUE_MID, SEQ_BLUE_HIGH = "#6da7ec", "#2a78d6", "#184f95"
STATUS_GOOD = "#0ca30c"
STATUS_CRITICAL = "#d03b3b"

SPENDING_COLS = {
    "gasto_vivienda_usd": "Housing",
    "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education",
    "gasto_salud_usd": "Healthcare",
}

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK_SECONDARY,
        "text.color": INK_PRIMARY,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "font.family": "sans-serif",
        "axes.grid": False,
    }
)


def _style_axes(ax, value_axis):
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(AXIS)
        ax.spines[spine].set_linewidth(0.8)
    ax.grid(axis=value_axis, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def _add_source_note(fig):
    fig.text(0.99, 0.01, SOURCE_NOTE, ha="right", va="bottom", fontsize=8, color=INK_MUTED)


def _save(fig, filename):
    fig.subplots_adjust(bottom=0.16)
    fig.savefig(f"{CHARTS_DIR}/{filename}", dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"Saved {CHARTS_DIR}/{filename}")


def chart_1_income_by_country(df):
    order = (
        df.groupby("pais")["ingreso_mensual_usd"].median().sort_values(ascending=False).index.tolist()
    )
    plot_order = list(reversed(order))  # last item plots at the top
    data = [df.loc[df["pais"] == c, "ingreso_mensual_usd"].values for c in plot_order]
    colors = [COUNTRY_COLOR[c] for c in plot_order]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bp = ax.boxplot(
        data,
        vert=False,
        patch_artist=True,
        widths=0.6,
        medianprops=dict(color=INK_PRIMARY, linewidth=1.5),
        whiskerprops=dict(color=INK_SECONDARY, linewidth=1),
        capprops=dict(color=INK_SECONDARY, linewidth=1),
        flierprops=dict(marker="o", markersize=4, markerfacecolor=INK_MUTED, markeredgecolor="none", alpha=0.6),
        zorder=3,
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)
        patch.set_edgecolor(color)

    ax.set_yticks(range(1, len(plot_order) + 1))
    ax.set_yticklabels(plot_order)
    ax.set_xlabel("Monthly Income (USD)")
    ax.set_title("Income Distribution by Country", fontsize=14, fontweight="bold", color=INK_PRIMARY, pad=14)
    _style_axes(ax, value_axis="x")
    _add_source_note(fig)
    _save(fig, "01_income_by_country.png")


def chart_2_age_vs_savings(df):
    fig, ax = plt.subplots(figsize=(9, 6))
    for country in COUNTRY_ORDER:
        sub = df[df["pais"] == country]
        ax.scatter(
            sub["edad"],
            sub["ahorro_mensual_usd"],
            s=32,
            color=COUNTRY_COLOR[country],
            alpha=0.75,
            edgecolors=SURFACE,
            linewidths=0.6,
            label=country,
            zorder=3,
        )

    x = df["edad"].to_numpy()
    y = df["ahorro_mensual_usd"].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(
        x_line,
        slope * x_line + intercept,
        color=INK_PRIMARY,
        linewidth=2,
        zorder=4,
        label="Trend (linear fit)",
    )

    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Monthly Savings (USD)")
    ax.set_title("Age vs. Monthly Savings, by Country", fontsize=14, fontweight="bold", color=INK_PRIMARY, pad=14)
    _style_axes(ax, value_axis="y")
    ax.legend(frameon=False, loc="upper left", fontsize=9, labelcolor=INK_SECONDARY)
    _add_source_note(fig)
    _save(fig, "02_age_vs_savings.png")


def chart_3_spending_breakdown(df):
    pct = {label: (df[col] / df["ingreso_mensual_usd"] * 100).mean() for col, label in SPENDING_COLS.items()}
    series = pd.Series(pct).sort_values(ascending=True)  # last item plots at the top

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(series.index, series.to_numpy(), color=CATEGORICAL[0], height=0.6, zorder=3)
    for bar, value in zip(bars, series.to_numpy()):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            ha="left",
            fontsize=9,
            color=INK_SECONDARY,
        )

    ax.set_xlabel("Average % of Income")
    ax.set_title("Spending Breakdown by Category", fontsize=14, fontweight="bold", color=INK_PRIMARY, pad=14)
    ax.set_xlim(0, series.max() * 1.18)
    _style_axes(ax, value_axis="x")
    _add_source_note(fig)
    _save(fig, "03_spending_breakdown.png")


def chart_4_satisfaction_by_ai_usage(df):
    bins = [0, 3, 10, float("inf")]
    labels = ["Low\n(0-3 hrs/wk)", "Medium\n(4-10 hrs/wk)", "High\n(11+ hrs/wk)"]
    groups = pd.cut(df["horas_herramientas_ia_semana"], bins=bins, labels=labels, include_lowest=True)
    avg = df.groupby(groups, observed=True)["satisfaccion_financiera"].mean().reindex(labels)

    colors = [SEQ_BLUE_LOW, SEQ_BLUE_MID, SEQ_BLUE_HIGH]
    fig, ax = plt.subplots(figsize=(7, 5.5))
    bars = ax.bar(avg.index, avg.to_numpy(), color=colors, width=0.55, zorder=3)
    for bar, value in zip(bars, avg.to_numpy()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color=INK_PRIMARY,
            fontweight="bold",
        )

    ax.set_ylabel("Avg. Financial Satisfaction (1-5)")
    ax.set_xlabel("Weekly AI Tool Usage")
    ax.set_ylim(0, 5.5)
    ax.set_title("Financial Satisfaction by AI Tool Usage", fontsize=14, fontweight="bold", color=INK_PRIMARY, pad=14)
    _style_axes(ax, value_axis="y")
    _add_source_note(fig)
    _save(fig, "04_satisfaction_by_ai_usage.png")


def chart_5_housing_burden_by_country(df):
    df = df.copy()
    df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
    series = df.groupby("pais")["housing_pct"].mean().sort_values(ascending=True)  # last item plots at the top

    cmap = LinearSegmentedColormap.from_list("burden", [STATUS_GOOD, STATUS_CRITICAL])
    norm = plt.Normalize(series.min(), series.max())
    colors = [cmap(norm(v)) for v in series.to_numpy()]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(series.index, series.to_numpy(), color=colors, height=0.6, zorder=3)
    for bar, value in zip(bars, series.to_numpy()):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            ha="left",
            fontsize=9,
            color=INK_SECONDARY,
        )

    ax.set_xlabel("Avg. Housing Cost (% of Income)")
    ax.set_title("Housing Burden by Country", fontsize=14, fontweight="bold", color=INK_PRIMARY, pad=14)
    ax.set_xlim(0, series.max() * 1.18)
    _style_axes(ax, value_axis="x")
    _add_source_note(fig)
    _save(fig, "05_housing_burden_by_country.png")


def main():
    df = pd.read_csv(DATA_PATH)

    chart_1_income_by_country(df)
    chart_2_age_vs_savings(df)
    chart_3_spending_breakdown(df)
    chart_4_satisfaction_by_ai_usage(df)
    chart_5_housing_burden_by_country(df)


if __name__ == "__main__":
    main()
