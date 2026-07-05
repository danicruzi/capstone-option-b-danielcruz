"""
Country statistical profile: Colombia
Pipeline: Analisis LatAm 2025 — Futuro Digital LatAm

Reads data/latam_finanzas_clean.csv, filters rows where pais == "Colombia",
and computes the statistics required for the country profile section:

1. Sample size and age range
2. Income stats (median, mean, min, max, std) in USD
3. Housing burden (gasto_vivienda_usd as % of ingreso_mensual_usd)
4. Spending breakdown (average % of income for each gasto_* column)
5. Savings (average ahorro_mensual_usd, % respondents with negative savings)
6. AI tools usage (avg horas_herramientas_ia_semana, avg satisfaccion_financiera)

Output: prints a Markdown section ("## Pais: Colombia") to stdout.
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Colombia"

df = pd.read_csv(CSV_PATH)
sub = df[df["pais"] == COUNTRY].copy()

gasto_cols = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]

# 1. Sample size and age range
n = len(sub)
age_min, age_max = sub["edad"].min(), sub["edad"].max()

# 2. Income stats
income = sub["ingreso_mensual_usd"]
income_median = income.median()
income_mean = income.mean()
income_min = income.min()
income_max = income.max()
income_std = income.std()

# 3. Housing burden (% of income), computed per-respondent then averaged
housing_pct = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"]) * 100
housing_pct_avg = housing_pct.mean()

# 4. Spending breakdown: avg % of income for each gasto_* column
spending_breakdown = {}
for col in gasto_cols:
    pct = (sub[col] / sub["ingreso_mensual_usd"]) * 100
    spending_breakdown[col] = pct.mean()

# 5. Savings
ahorro_mean = sub["ahorro_mensual_usd"].mean()
pct_negative_savings = (sub["ahorro_mensual_usd"] < 0).mean() * 100

# 6. AI tools usage
avg_ia_hours = sub["horas_herramientas_ia_semana"].mean()
avg_satisfaccion = sub["satisfaccion_financiera"].mean()

# ---- Build Markdown output ----
lines = []
lines.append(f"## Pais: {COUNTRY}")
lines.append("")
lines.append("### 1. Sample size and age range")
lines.append(f"- Sample size: {n} respondents")
lines.append(f"- Age range: {age_min}-{age_max} years")
lines.append("")
lines.append("### 2. Income (USD)")
lines.append(f"- Median: ${income_median:,.2f}")
lines.append(f"- Mean: ${income_mean:,.2f}")
lines.append(f"- Min: ${income_min:,.2f}")
lines.append(f"- Max: ${income_max:,.2f}")
lines.append(f"- Standard deviation: ${income_std:,.2f}")
lines.append("")
lines.append("### 3. Housing burden")
lines.append(f"- Average gasto_vivienda_usd as % of ingreso_mensual_usd: {housing_pct_avg:.1f}%")
lines.append("")
lines.append("### 4. Spending breakdown (average % of income)")
for col in gasto_cols:
    label = col.replace("gasto_", "").replace("_usd", "").capitalize()
    lines.append(f"- {label}: {spending_breakdown[col]:.1f}%")
lines.append("")
lines.append("### 5. Savings")
lines.append(f"- Average ahorro_mensual_usd: ${ahorro_mean:,.2f}")
lines.append(f"- % of respondents with negative savings: {pct_negative_savings:.1f}%")
lines.append("")
lines.append("### 6. AI tools and financial satisfaction")
lines.append(f"- Average horas_herramientas_ia_semana: {avg_ia_hours:.2f} hours/week")
lines.append(f"- Average satisfaccion_financiera: {avg_satisfaccion:.2f}")
lines.append("")

output = "\n".join(lines)
print(output)
