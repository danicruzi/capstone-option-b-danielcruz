"""
Country statistical profile: Chile
Part of the Análisis LatAm 2025 pipeline (Futuro Digital LatAm).

Reads data/latam_finanzas_clean.csv, filters rows where pais == "Chile",
and prints a Markdown section (## País: Chile) with:
  1. Sample size and age range
  2. Income statistics (USD)
  3. Housing burden (% of income)
  4. Spending breakdown (% of income per gasto_* category)
  5. Savings (average + % negative savers)
  6. AI tool usage and financial satisfaction
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
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
    df = pd.read_csv(DATA_PATH)
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
    housing_pct_mean = housing_pct.mean()

    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (sub[col] / sub["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    ahorro_mean = sub["ahorro_mensual_usd"].mean()
    pct_negative = (sub["ahorro_mensual_usd"] < 0).mean() * 100

    ia_hours_mean = sub["horas_herramientas_ia_semana"].mean()
    satisfaccion_mean = sub["satisfaccion_financiera"].mean()

    md = []
    md.append(f"## País: {COUNTRY}\n")

    md.append("### 1. Sample size and age range")
    md.append(f"- Sample size: {n} respondents")
    md.append(f"- Age range: {age_min}–{age_max} years\n")

    md.append("### 2. Income (USD)")
    md.append(f"- Median: ${income_median:,.2f}")
    md.append(f"- Mean: ${income_mean:,.2f}")
    md.append(f"- Min: ${income_min:,.2f}")
    md.append(f"- Max: ${income_max:,.2f}")
    md.append(f"- Standard deviation: ${income_std:,.2f}\n")

    md.append("### 3. Housing burden")
    md.append(f"- Average gasto_vivienda_usd as % of ingreso_mensual_usd: {housing_pct_mean:.1f}%\n")

    md.append("### 4. Spending breakdown (average % of income)")
    for col, pct in spending_breakdown.items():
        label = col.replace("gasto_", "").replace("_usd", "")
        md.append(f"- {label.capitalize()}: {pct:.1f}%")
    md.append("")

    md.append("### 5. Savings")
    md.append(f"- Average ahorro_mensual_usd: ${ahorro_mean:,.2f}")
    md.append(f"- % of respondents with negative savings: {pct_negative:.1f}%\n")

    md.append("### 6. AI tools and financial satisfaction")
    md.append(f"- Average horas_herramientas_ia_semana: {ia_hours_mean:.2f} hours/week")
    md.append(f"- Average satisfaccion_financiera: {satisfaccion_mean:.2f}\n")

    output = "\n".join(md)
    print(output)

    return output


if __name__ == "__main__":
    main()
