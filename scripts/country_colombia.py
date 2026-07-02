"""
Country profile script — Colombia
Datos que Hablan — Financial Wellness of Young Professionals in Latin America

Reads data/latam_finanzas_clean.csv and computes the statistics needed to
populate the "## País: Colombia" section of the executive report:

1. Sample size and age range
2. Income statistics (median, mean, min, max, std) in USD
3. Housing burden: avg gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: avg % of income for each gasto_* column
5. Savings: avg ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: avg horas_herramientas_ia_semana and avg satisfaccion_financiera
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Colombia"

df = pd.read_csv(DATA_PATH)
country_df = df[df["pais"] == COUNTRY].copy()

# 1. Sample size and age range
n = len(country_df)
age_min = country_df["edad"].min()
age_max = country_df["edad"].max()

# 2. Income statistics (USD)
income = country_df["ingreso_mensual_usd"]
income_median = income.median()
income_mean = income.mean()
income_min = income.min()
income_max = income.max()
income_std = income.std()

# 3. Housing burden: avg gasto_vivienda_usd as % of ingreso_mensual_usd
housing_pct = (country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"]) * 100
housing_pct_avg = housing_pct.mean()

# 4. Spending breakdown: avg % of income for each gasto_* column
gasto_cols = [c for c in country_df.columns if c.startswith("gasto_")]
spending_breakdown = {}
for col in gasto_cols:
    pct = (country_df[col] / country_df["ingreso_mensual_usd"]) * 100
    spending_breakdown[col] = pct.mean()

# 5. Savings: avg ahorro_mensual_usd and % of respondents with negative savings
ahorro_avg = country_df["ahorro_mensual_usd"].mean()
pct_negative_savings = (country_df["ahorro_mensual_usd"] < 0).mean() * 100

# 6. AI tools: avg horas_herramientas_ia_semana and avg satisfaccion_financiera
ia_hours_avg = country_df["horas_herramientas_ia_semana"].mean()
satisfaccion_avg = country_df["satisfaccion_financiera"].mean()

if __name__ == "__main__":
    print(f"## País: {COUNTRY}\n")
    print(f"Sample size: {n}")
    print(f"Age range: {age_min}-{age_max}")
    print(f"Income median: {income_median:.2f}")
    print(f"Income mean: {income_mean:.2f}")
    print(f"Income min: {income_min:.2f}")
    print(f"Income max: {income_max:.2f}")
    print(f"Income std: {income_std:.2f}")
    print(f"Housing burden avg %: {housing_pct_avg:.2f}")
    for col, pct in spending_breakdown.items():
        print(f"  {col}: {pct:.2f}%")
    print(f"Avg monthly savings: {ahorro_avg:.2f}")
    print(f"% with negative savings: {pct_negative_savings:.2f}")
    print(f"Avg AI tool hours/week: {ia_hours_avg:.2f}")
    print(f"Avg financial satisfaction: {satisfaccion_avg:.2f}")
