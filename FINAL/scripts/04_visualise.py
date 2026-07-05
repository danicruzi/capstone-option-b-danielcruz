"""Phase 4: Generate the five report charts from the cleaned survey data."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy import stats

CLEAN_PATH = "data/latam_finanzas_clean.csv"
CHARTS_DIR = "charts"
SOURCE_NOTE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

# Categorical palette (fixed order, from the dataviz skill's validated default palette).
COUNTRY_COLORS = {
    "México": "#2a78d6",     # blue
    "Colombia": "#1baf7a",   # aqua
    "Argentina": "#eda100",  # yellow
    "Chile": "#008300",      # green
    "Perú": "#4a3aa7",       # violet
    "Brasil": "#e34948",     # red
}

INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
SURFACE = "#fcfcfb"

SPENDING_COLS = {
    "gasto_vivienda_usd": "Vivienda",
    "gasto_alimentacion_usd": "Alimentación",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educación",
    "gasto_salud_usd": "Salud",
}


def style_axes(ax, x_grid=False, y_grid=False):
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(INK_MUTED)
    ax.tick_params(colors=INK_SECONDARY, labelsize=9)
    if x_grid:
        ax.xaxis.grid(True, color=GRIDLINE, linewidth=0.8, zorder=0)
    if y_grid:
        ax.yaxis.grid(True, color=GRIDLINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def add_source_note(fig):
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=8, color=INK_MUTED, ha="left")


def save(fig, filename):
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    path = f"{CHARTS_DIR}/{filename}"
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def chart_1_income_by_country(df):
    order = (
        df.groupby("pais")["ingreso_mensual_usd"].median().sort_values(ascending=True).index.tolist()
    )
    data = [df.loc[df["pais"] == pais, "ingreso_mensual_usd"].values for pais in order]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bp = ax.boxplot(
        data,
        vert=False,
        tick_labels=order,
        patch_artist=True,
        widths=0.6,
        medianprops={"color": INK_PRIMARY, "linewidth": 1.5},
        whiskerprops={"color": INK_SECONDARY},
        capprops={"color": INK_SECONDARY},
        flierprops={"markeredgecolor": INK_MUTED, "markersize": 4},
    )
    for patch, pais in zip(bp["boxes"], order):
        patch.set_facecolor(COUNTRY_COLORS[pais])
        patch.set_alpha(0.85)
        patch.set_edgecolor(INK_PRIMARY)
        patch.set_linewidth(0.8)

    style_axes(ax, x_grid=True)
    ax.set_xlabel("Monthly income (USD)", color=INK_SECONDARY, fontsize=10)
    ax.set_ylabel("")
    ax.set_title("Monthly Income Distribution by Country", color=INK_PRIMARY, fontsize=14, weight="bold", pad=12)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))

    add_source_note(fig)
    save(fig, "01_income_by_country.png")


def chart_2_age_vs_savings(df):
    fig, ax = plt.subplots(figsize=(9, 6))

    for pais, color in COUNTRY_COLORS.items():
        subset = df[df["pais"] == pais]
        ax.scatter(
            subset["edad"], subset["ahorro_mensual_usd"],
            color=color, alpha=0.7, s=35, edgecolor="white", linewidth=0.4,
            label=pais, zorder=3,
        )

    slope, intercept, r_value, p_value, std_err = stats.linregress(df["edad"], df["ahorro_mensual_usd"])
    x_line = np.linspace(df["edad"].min(), df["edad"].max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(
        x_line, y_line, color=INK_PRIMARY, linewidth=2, linestyle="--",
        label=f"Trend (r = {r_value:.2f})", zorder=4,
    )

    style_axes(ax, x_grid=True, y_grid=True)
    ax.set_xlabel("Age (years)", color=INK_SECONDARY, fontsize=10)
    ax.set_ylabel("Monthly savings (USD)", color=INK_SECONDARY, fontsize=10)
    ax.set_title("Age vs. Monthly Savings", color=INK_PRIMARY, fontsize=14, weight="bold", pad=12)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    legend = ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
    for text in legend.get_texts():
        text.set_color(INK_SECONDARY)

    add_source_note(fig)
    fig.tight_layout(rect=(0, 0.03, 0.85, 1))
    path = f"{CHARTS_DIR}/02_age_vs_savings.png"
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {path}")


def chart_3_spending_breakdown(df):
    pct_of_income = pd.DataFrame({
        label: df[col] / df["ingreso_mensual_usd"] * 100
        for col, label in SPENDING_COLS.items()
    })
    avg_pct = pct_of_income.mean().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(avg_pct.index, avg_pct.values, color="#2a78d6", edgecolor=INK_PRIMARY, linewidth=0.5, zorder=3)

    for i, value in enumerate(avg_pct.values):
        ax.text(value + 0.3, i, f"{value:.1f}%", va="center", fontsize=9, color=INK_PRIMARY)

    style_axes(ax, x_grid=True)
    ax.set_xlabel("Average % of monthly income", color=INK_SECONDARY, fontsize=10)
    ax.set_ylabel("")
    ax.set_title("Spending Breakdown by Category", color=INK_PRIMARY, fontsize=14, weight="bold", pad=12)
    ax.set_xlim(0, avg_pct.values.max() * 1.15)

    add_source_note(fig)
    save(fig, "03_spending_breakdown.png")


def chart_4_satisfaction_by_ai_usage(df):
    def usage_group(hours):
        if hours <= 3:
            return "Low (0-3h)"
        elif hours <= 10:
            return "Medium (4-10h)"
        else:
            return "High (11h+)"

    df = df.copy()
    df["usage_group"] = df["horas_herramientas_ia_semana"].apply(usage_group)
    order = ["Low (0-3h)", "Medium (4-10h)", "High (11h+)"]
    avg_satisfaction = df.groupby("usage_group")["satisfaccion_financiera"].mean().reindex(order)

    # Ordinal blue ramp - lightest for Low, darkest for High.
    ramp = ["#86b6ef", "#2a78d6", "#184f95"]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    bars = ax.bar(order, avg_satisfaction.values, color=ramp, edgecolor=INK_PRIMARY, linewidth=0.5, zorder=3)

    for bar, value in zip(bars, avg_satisfaction.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2, value + 0.05, f"{value:.2f}",
            ha="center", fontsize=10, color=INK_PRIMARY, weight="bold",
        )

    style_axes(ax, y_grid=True)
    ax.set_xlabel("AI tool usage (hours/week)", color=INK_SECONDARY, fontsize=10)
    ax.set_ylabel("Average financial satisfaction (1-5)", color=INK_SECONDARY, fontsize=10)
    ax.set_title("Financial Satisfaction by AI Tool Usage", color=INK_PRIMARY, fontsize=14, weight="bold", pad=12)
    ax.set_ylim(0, 5.5)

    add_source_note(fig)
    save(fig, "04_satisfaction_by_ai_usage.png")


def chart_5_housing_burden_by_country(df):
    housing_pct = (
        (df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100).groupby(df["pais"]).mean()
        .sort_values(ascending=True)
    )

    # Diverging red-to-green gradient (status palette poles: critical -> good).
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
        "housing_burden", ["#0ca30c", "#fab219", "#d03b3b"]
    )
    norm = plt.matplotlib.colors.Normalize(vmin=housing_pct.min(), vmax=housing_pct.max())
    colors = [cmap(norm(v)) for v in housing_pct.values]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(housing_pct.index, housing_pct.values, color=colors, edgecolor=INK_PRIMARY, linewidth=0.5, zorder=3)

    for i, value in enumerate(housing_pct.values):
        ax.text(value + 0.4, i, f"{value:.1f}%", va="center", fontsize=9, color=INK_PRIMARY)

    style_axes(ax, x_grid=True)
    ax.set_xlabel("Average housing cost (% of monthly income)", color=INK_SECONDARY, fontsize=10)
    ax.set_ylabel("")
    ax.set_title("Housing Cost Burden by Country", color=INK_PRIMARY, fontsize=14, weight="bold", pad=12)
    ax.set_xlim(0, housing_pct.values.max() * 1.15)

    add_source_note(fig)
    save(fig, "05_housing_burden_by_country.png")


def main():
    df = pd.read_csv(CLEAN_PATH, encoding="utf-8")

    chart_1_income_by_country(df)
    chart_2_age_vs_savings(df)
    chart_3_spending_breakdown(df)
    chart_4_satisfaction_by_ai_usage(df)
    chart_5_housing_burden_by_country(df)


if __name__ == "__main__":
    main()
