"""
Country statistical profile: México
Reads data/latam_finanzas_clean.csv and computes the required statistics
for the country "México" only.

Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "México"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]

GASTO_LABELS = {
    "gasto_vivienda_usd": "Vivienda (Housing)",
    "gasto_alimentacion_usd": "Alimentación (Food)",
    "gasto_transporte_usd": "Transporte (Transport)",
    "gasto_entretenimiento_usd": "Entretenimiento (Entertainment)",
    "gasto_educacion_usd": "Educación (Education)",
    "gasto_salud_usd": "Salud (Health)",
}


def main():
    df = pd.read_csv(CSV_PATH)
    d = df[df["pais"] == COUNTRY].copy()

    n = len(d)
    age_min, age_max = d["edad"].min(), d["edad"].max()

    # Income stats
    income = d["ingreso_mensual_usd"]
    income_stats = {
        "median": income.median(),
        "mean": income.mean(),
        "min": income.min(),
        "max": income.max(),
        "std": income.std(),
    }

    # Housing burden: gasto_vivienda_usd as % of ingreso_mensual_usd, averaged per respondent
    housing_pct = (d["gasto_vivienda_usd"] / d["ingreso_mensual_usd"]) * 100
    housing_burden_avg = housing_pct.mean()

    # Spending breakdown: average % of income for each gasto_* column
    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (d[col] / d["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    # Savings
    avg_savings = d["ahorro_mensual_usd"].mean()
    pct_negative_savings = (d["ahorro_mensual_usd"] < 0).mean() * 100

    # AI tools & satisfaction
    avg_ia_hours = d["horas_herramientas_ia_semana"].mean()
    avg_satisfaction = d["satisfaccion_financiera"].mean()

    # ---- Print results ----
    print(f"## País: {COUNTRY}\n")

    print("### 1. Sample size and age range")
    print(f"- Sample size: {n} respondents")
    print(f"- Age range: {age_min}–{age_max} years\n")

    print("### 2. Income (USD)")
    print(f"- Median: {income_stats['median']:.2f}")
    print(f"- Mean: {income_stats['mean']:.2f}")
    print(f"- Min: {income_stats['min']:.2f}")
    print(f"- Max: {income_stats['max']:.2f}")
    print(f"- Std Dev: {income_stats['std']:.2f}\n")

    print("### 3. Housing burden")
    print(f"- Average gasto_vivienda_usd as % of ingreso_mensual_usd: {housing_burden_avg:.2f}%\n")

    print("### 4. Spending breakdown (average % of income)")
    for col in GASTO_COLS:
        print(f"- {GASTO_LABELS[col]}: {spending_breakdown[col]:.2f}%")
    print()

    print("### 5. Savings")
    print(f"- Average ahorro_mensual_usd: {avg_savings:.2f}")
    print(f"- % of respondents with negative savings: {pct_negative_savings:.2f}%\n")

    print("### 6. AI tools & satisfaction")
    print(f"- Average horas_herramientas_ia_semana: {avg_ia_hours:.2f}")
    print(f"- Average satisfaccion_financiera: {avg_satisfaction:.2f}")


if __name__ == "__main__":
    main()
