"""
Country profile: Argentina
Datos que Hablan — Financial Wellness of Young Professionals in Latin America

Reads data/latam_finanzas_clean.csv, filters to Argentina, and prints the
statistics needed to build the "## País: Argentina" Markdown section:

1. Sample size and age range
2. Income: median, mean, min, max, std (USD)
3. Housing burden: avg gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: avg % of income for each gasto_* column
5. Savings: avg ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: avg horas_herramientas_ia_semana and avg satisfaccion_financiera
"""

import pandas as pd

COUNTRY = "Argentina"
DATA_PATH = "data/latam_finanzas_clean.csv"

df = pd.read_csv(DATA_PATH)
country_df = df[df["pais"] == COUNTRY].copy()

# 1. Sample size and age range
n = len(country_df)
age_min = country_df["edad"].min()
age_max = country_df["edad"].max()

# 2. Income stats (USD)
income = country_df["ingreso_mensual_usd"]
income_median = income.median()
income_mean = income.mean()
income_min = income.min()
income_max = income.max()
income_std = income.std()

# 3. Housing burden: gasto_vivienda_usd as % of ingreso_mensual_usd (per-row, then averaged)
housing_pct = (country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"]) * 100
housing_pct_avg = housing_pct.mean()

# 4. Spending breakdown: avg % of income for each gasto_* column
gasto_cols = [c for c in country_df.columns if c.startswith("gasto_")]
spending_breakdown = {}
for col in gasto_cols:
    pct = (country_df[col] / country_df["ingreso_mensual_usd"]) * 100
    spending_breakdown[col] = pct.mean()

# 5. Savings
ahorro_mean = country_df["ahorro_mensual_usd"].mean()
pct_negative_savings = (country_df["ahorro_mensual_usd"] < 0).mean() * 100

# 6. AI tools
avg_ia_hours = country_df["horas_herramientas_ia_semana"].mean()
avg_satisfaccion = country_df["satisfaccion_financiera"].mean()

if __name__ == "__main__":
    print(f"=== {COUNTRY} ===")
    print(f"Sample size: {n}")
    print(f"Age range: {age_min}-{age_max}")
    print()
    print("Income (USD):")
    print(f"  Median: {income_median:.2f}")
    print(f"  Mean:   {income_mean:.2f}")
    print(f"  Min:    {income_min:.2f}")
    print(f"  Max:    {income_max:.2f}")
    print(f"  Std:    {income_std:.2f}")
    print()
    print(f"Housing burden (avg gasto_vivienda_usd as % of income): {housing_pct_avg:.2f}%")
    print()
    print("Spending breakdown (avg % of income):")
    for col, pct in spending_breakdown.items():
        print(f"  {col}: {pct:.2f}%")
    print()
    print(f"Avg monthly savings (ahorro_mensual_usd): {ahorro_mean:.2f} USD")
    print(f"% with negative savings: {pct_negative_savings:.2f}%")
    print()
    print(f"Avg AI tool hours/week: {avg_ia_hours:.2f}")
    print(f"Avg financial satisfaction: {avg_satisfaccion:.2f}")
