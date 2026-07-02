"""
Country profile: Chile
Datos que Hablan — Financial Wellness of Young Professionals in Latin America

Reads data/latam_finanzas_clean.csv, filters to Chile, and prints a Markdown
section with sample size/age range, income stats, housing burden, spending
breakdown, savings, and AI tool usage.
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Chile"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(CSV_PATH)
    country_df = df[df["pais"] == COUNTRY].copy()

    n = len(country_df)
    age_min = country_df["edad"].min()
    age_max = country_df["edad"].max()

    income = country_df["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    housing_pct = (
        country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"] * 100
    )
    housing_avg_pct = housing_pct.mean()

    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (country_df[col] / country_df["ingreso_mensual_usd"] * 100).mean()
        spending_breakdown[col] = pct

    savings_avg = country_df["ahorro_mensual_usd"].mean()
    negative_savings_pct = (country_df["ahorro_mensual_usd"] < 0).mean() * 100

    ai_hours_avg = country_df["horas_herramientas_ia_semana"].mean()
    satisfaction_avg = country_df["satisfaccion_financiera"].mean()

    # ---- Print Markdown section ----
    print(f"## País: {COUNTRY}\n")

    print("### Sample")
    print(f"- Sample size: {n} respondents")
    print(f"- Age range: {age_min}–{age_max} years\n")

    print("### Income (USD)")
    print(f"- Median: ${income_median:,.2f}")
    print(f"- Mean: ${income_mean:,.2f}")
    print(f"- Min: ${income_min:,.2f}")
    print(f"- Max: ${income_max:,.2f}")
    print(f"- Standard deviation: ${income_std:,.2f}\n")

    print("### Housing Burden")
    print(
        f"- Average housing expense (gasto_vivienda_usd) as % of monthly income: "
        f"{housing_avg_pct:.1f}%\n"
    )

    print("### Spending Breakdown (average % of monthly income)")
    for col, pct in spending_breakdown.items():
        print(f"- {col}: {pct:.1f}%")
    print()

    print("### Savings")
    print(f"- Average monthly savings (ahorro_mensual_usd): ${savings_avg:,.2f}")
    print(f"- % of respondents with negative savings: {negative_savings_pct:.1f}%\n")

    print("### AI Tools")
    print(f"- Average hours/week using AI tools (horas_herramientas_ia_semana): {ai_hours_avg:.1f}")
    print(f"- Average financial satisfaction (satisfaccion_financiera): {satisfaction_avg:.1f}\n")

    print(
        "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
    )


if __name__ == "__main__":
    main()
