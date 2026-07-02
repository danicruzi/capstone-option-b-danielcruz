"""
Country profile: Mexico
Generates a statistical profile for Mexico from the clean survey dataset.

Project: Datos que Hablan - Financial Wellness of Young Professionals in Latin America
Source data: data/latam_finanzas_clean.csv
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


def main():
    df = pd.read_csv(CSV_PATH)

    # Confirm the exact label used for Mexico in the "pais" column
    print("Distinct values in 'pais':", sorted(df["pais"].unique()))

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

    ahorro_mean = sub["ahorro_mensual_usd"].mean()
    pct_negative_savings = (sub["ahorro_mensual_usd"] < 0).mean() * 100

    ia_hours_avg = sub["horas_herramientas_ia_semana"].mean()
    satisfaccion_avg = sub["satisfaccion_financiera"].mean()

    print(f"\n=== Country profile: {COUNTRY} ===")
    print(f"Sample size: {n}")
    print(f"Age range: {age_min}-{age_max}")
    print(f"Income (USD) - median: {income_median:.2f}, mean: {income_mean:.2f}, "
          f"min: {income_min:.2f}, max: {income_max:.2f}, std: {income_std:.2f}")
    print(f"Housing burden (avg % of income): {housing_pct_avg:.2f}%")
    print("Spending breakdown (avg % of income):")
    for col, pct in spending_breakdown.items():
        print(f"  {col}: {pct:.2f}%")
    print(f"Avg monthly savings (USD): {ahorro_mean:.2f}")
    print(f"% with negative savings: {pct_negative_savings:.2f}%")
    print(f"Avg AI tool hours/week: {ia_hours_avg:.2f}")
    print(f"Avg financial satisfaction: {satisfaccion_avg:.2f}")


if __name__ == "__main__":
    main()
