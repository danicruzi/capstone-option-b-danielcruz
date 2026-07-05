"""
Country statistical profile: Peru
Pipeline: Analisis LatAm 2025 - Futuro Digital LatAm

Reads data/latam_finanzas_clean.csv, filters rows where pais == 'Peru'
(accented value in the source data), and computes the statistics required
for the country's Markdown profile section:

1. Sample size and age range
2. Income stats (median, mean, min, max, std) in USD
3. Housing burden: avg gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: avg % of income for each gasto_* column
5. Savings: avg ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: avg horas_herramientas_ia_semana and avg satisfaccion_financiera

Output: prints the computed values used to build the Markdown section.
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Perú"

def main():
    df = pd.read_csv(DATA_PATH)
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

    gasto_cols = [c for c in df.columns if c.startswith("gasto_")]

    housing_pct = (country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"] * 100).mean()

    spending_breakdown = {}
    for col in gasto_cols:
        pct = (country_df[col] / country_df["ingreso_mensual_usd"] * 100).mean()
        spending_breakdown[col] = pct

    ahorro_mean = country_df["ahorro_mensual_usd"].mean()
    pct_negative_savings = (country_df["ahorro_mensual_usd"] < 0).mean() * 100

    ia_hours_mean = country_df["horas_herramientas_ia_semana"].mean()
    satisfaccion_mean = country_df["satisfaccion_financiera"].mean()

    print(f"Country: {COUNTRY}")
    print(f"Sample size: {n}")
    print(f"Age range: {age_min} - {age_max}")
    print()
    print("Income (USD):")
    print(f"  Median: {income_median:.2f}")
    print(f"  Mean: {income_mean:.2f}")
    print(f"  Min: {income_min:.2f}")
    print(f"  Max: {income_max:.2f}")
    print(f"  Std Dev: {income_std:.2f}")
    print()
    print(f"Housing burden (avg gasto_vivienda_usd as % of income): {housing_pct:.2f}%")
    print()
    print("Spending breakdown (avg % of income):")
    for col, pct in spending_breakdown.items():
        print(f"  {col}: {pct:.2f}%")
    print()
    print(f"Avg ahorro_mensual_usd: {ahorro_mean:.2f}")
    print(f"% respondents with negative savings: {pct_negative_savings:.2f}%")
    print()
    print(f"Avg horas_herramientas_ia_semana: {ia_hours_mean:.2f}")
    print(f"Avg satisfaccion_financiera: {satisfaccion_mean:.2f}")

if __name__ == "__main__":
    main()
