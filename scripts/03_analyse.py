"""
Phase 3 — Core analyses for Datos que Hablan.

Reads the clean dataset and produces six analysis tables:
  1. Income by country
  2. Age vs. savings
  3. Spending breakdown (full sample)
  4. Credit card holders vs. non-holders
  5. AI tool usage vs. financial satisfaction
  6. Housing burden by country

Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm
"""

import sys

import pandas as pd
from scipy.stats import pearsonr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

DATA_PATH = "data/latam_finanzas_clean.csv"

SPENDING_COLS = {
    "gasto_vivienda_usd": "Housing",
    "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education",
    "gasto_salud_usd": "Healthcare",
}


def print_table(title, df):
    print(f"\n{title}")
    print("-" * len(title))
    print(df.to_string(index=False))


def analysis_1_income_by_country(df):
    summary = (
        df.groupby("pais")["ingreso_mensual_usd"]
        .agg(median="median", mean="mean", min="min", max="max", std="std")
        .sort_values("median", ascending=False)
        .reset_index()
        .rename(columns={"pais": "Country"})
    )
    print_table("1. INCOME BY COUNTRY (USD)", summary)
    return summary


def analysis_2_age_vs_savings(df):
    bins = [18, 22, 25, 28, 32]
    labels = ["18-22", "23-25", "26-28", "29-32"]
    df = df.copy()
    df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels, include_lowest=True)
    df["savings_rate_pct"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

    summary = (
        df.groupby("age_group", observed=True)
        .agg(
            avg_monthly_savings=("ahorro_mensual_usd", "mean"),
            avg_savings_rate_pct=("savings_rate_pct", "mean"),
        )
        .reset_index()
        .rename(columns={"age_group": "Age Group"})
    )
    print_table("2. AGE VS. SAVINGS", summary)
    return summary


def analysis_3_spending_breakdown(df):
    pct_df = pd.DataFrame(
        {
            label: df[col] / df["ingreso_mensual_usd"] * 100
            for col, label in SPENDING_COLS.items()
        }
    )
    summary = (
        pct_df.mean()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "Category", 0: "Avg % of Income"})
    )
    print_table("3. SPENDING BREAKDOWN (Full Sample, avg % of income)", summary)
    return summary


def analysis_4_credit_card_holders(df):
    metrics = {
        "ingreso_mensual_usd": "Avg Income",
        "gasto_alimentacion_usd": "Avg Food Spending",
        "gasto_entretenimiento_usd": "Avg Entertainment Spending",
        "ahorro_mensual_usd": "Avg Savings",
    }
    holders = df[df["tiene_tarjeta_credito"] == "Sí"]
    non_holders = df[df["tiene_tarjeta_credito"] == "No"]

    rows = []
    for col, label in metrics.items():
        h_mean = holders[col].mean()
        n_mean = non_holders[col].mean()
        pct_diff = (h_mean - n_mean) / n_mean * 100
        rows.append(
            {
                "Metric": label,
                "Holders": h_mean,
                "Non-Holders": n_mean,
                "% Difference": pct_diff,
            }
        )
    summary = pd.DataFrame(rows)
    print_table("4. CREDIT CARD HOLDERS VS. NON-HOLDERS", summary)
    return summary


def analysis_5_ai_usage_vs_satisfaction(df):
    bins = [0, 3, 10, float("inf")]
    labels = ["Low (0-3 hrs)", "Medium (4-10 hrs)", "High (11+ hrs)"]
    df = df.copy()
    df["ai_usage_group"] = pd.cut(
        df["horas_herramientas_ia_semana"], bins=bins, labels=labels, include_lowest=True
    )

    summary = (
        df.groupby("ai_usage_group", observed=True)
        .agg(
            count=("id", "count"),
            avg_satisfaction=("satisfaccion_financiera", "mean"),
            avg_income=("ingreso_mensual_usd", "mean"),
        )
        .reset_index()
        .rename(columns={"ai_usage_group": "AI Usage Group"})
    )
    print_table("5. AI TOOL USAGE VS. FINANCIAL SATISFACTION", summary)

    corr, p_value = pearsonr(
        df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"]
    )
    print(f"\nPearson correlation (AI hours/week vs. financial satisfaction): "
          f"r = {corr:.3f}, p = {p_value:.3f}")
    return summary, corr, p_value


def analysis_6_housing_burden_by_country(df):
    df = df.copy()
    df["housing_pct_income"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
    summary = (
        df.groupby("pais")["housing_pct_income"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"pais": "Country", "housing_pct_income": "Avg Housing % of Income"})
    )
    print_table("6. HOUSING BURDEN BY COUNTRY", summary)
    return summary


def main():
    df = pd.read_csv(DATA_PATH)

    analysis_1_income_by_country(df)
    analysis_2_age_vs_savings(df)
    analysis_3_spending_breakdown(df)
    analysis_4_credit_card_holders(df)
    analysis_5_ai_usage_vs_satisfaction(df)
    analysis_6_housing_burden_by_country(df)

    print("\nSource: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm")


if __name__ == "__main__":
    main()
