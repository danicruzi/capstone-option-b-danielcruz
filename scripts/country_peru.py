"""
Country profile: Peru
Datos que Hablan - Financial Wellness of Young Professionals in Latin America

Reads the clean dataset and prints a statistical profile for Peru
(sample size, age range, income stats, housing burden, spending breakdown,
savings, and AI tool usage), formatted as a Markdown section.
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Perú"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    sub = df[df["pais"] == COUNTRY].copy()

    n = len(sub)
    age_min, age_max = sub["edad"].min(), sub["edad"].max()

    income = sub["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    housing_pct = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"]) * 100
    housing_pct_avg = housing_pct.mean()

    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (sub[col] / sub["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    savings_avg = sub["ahorro_mensual_usd"].mean()
    negative_savings_pct = (sub["ahorro_mensual_usd"] < 0).mean() * 100

    ia_hours_avg = sub["horas_herramientas_ia_semana"].mean()
    satisfaction_avg = sub["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}\n")
    print(f"- Sample size: {n} respondents")
    print(f"- Age range: {age_min}-{age_max} years\n")

    print("### Income (USD)")
    print(f"- Median: {income_median:,.2f}")
    print(f"- Mean: {income_mean:,.2f}")
    print(f"- Min: {income_min:,.2f}")
    print(f"- Max: {income_max:,.2f}")
    print(f"- Std. deviation: {income_std:,.2f}\n")

    print("### Housing burden")
    print(f"- Average gasto_vivienda_usd as % of ingreso_mensual_usd: {housing_pct_avg:.1f}%\n")

    print("### Spending breakdown (average % of income)")
    for col, pct in spending_breakdown.items():
        print(f"- {col}: {pct:.1f}%")
    print()

    print("### Savings")
    print(f"- Average ahorro_mensual_usd: {savings_avg:,.2f}")
    print(f"- % of respondents with negative savings: {negative_savings_pct:.1f}%\n")

    print("### AI tools")
    print(f"- Average horas_herramientas_ia_semana: {ia_hours_avg:.2f}")
    print(f"- Average satisfaccion_financiera: {satisfaction_avg:.2f}")

    print("\nSource: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm")


if __name__ == "__main__":
    main()
