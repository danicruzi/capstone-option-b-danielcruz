"""
Country statistical profile: Argentina
Pipeline: Analisis LatAm 2025 (Futuro Digital LatAm)

Reads data/latam_finanzas_clean.csv, filters rows where pais == "Argentina",
and computes the statistics required for the country profile Markdown section:

1. Sample size and age range
2. Income: median, mean, min, max, standard deviation (USD)
3. Housing burden: average gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: average % of income for each gasto_* column
5. Savings: average ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: average horas_herramientas_ia_semana and average satisfaccion_financiera

Output: prints the computed statistics and the assembled Markdown section
to stdout so it can be captured/redirected as needed.
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Argentina"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]

GASTO_LABELS = {
    "gasto_vivienda_usd": "Housing (vivienda)",
    "gasto_alimentacion_usd": "Food (alimentacion)",
    "gasto_transporte_usd": "Transport (transporte)",
    "gasto_entretenimiento_usd": "Entertainment (entretenimiento)",
    "gasto_educacion_usd": "Education (educacion)",
    "gasto_salud_usd": "Health (salud)",
}


def main():
    df = pd.read_csv(CSV_PATH)
    sub = df[df["pais"] == COUNTRY].copy()

    n = len(sub)
    age_min, age_max = sub["edad"].min(), sub["edad"].max()

    income = sub["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    # Housing burden as % of income, computed per-respondent then averaged
    housing_pct = (sub["gasto_vivienda_usd"] / income * 100)
    housing_pct_avg = housing_pct.mean()

    # Spending breakdown: average % of income per gasto_* column
    spending_pct = {}
    for col in GASTO_COLS:
        pct = (sub[col] / income * 100)
        spending_pct[col] = pct.mean()

    # Savings
    savings_avg = sub["ahorro_mensual_usd"].mean()
    neg_savings_pct = (sub["ahorro_mensual_usd"] < 0).mean() * 100

    # AI tools / satisfaction
    ia_hours_avg = sub["horas_herramientas_ia_semana"].mean()
    satisfaccion_avg = sub["satisfaccion_financiera"].mean()

    # --- print results ---
    print(f"Sample size: {n}")
    print(f"Age range: {age_min}-{age_max}")
    print(f"Income median: {income_median:.2f}")
    print(f"Income mean: {income_mean:.2f}")
    print(f"Income min: {income_min:.2f}")
    print(f"Income max: {income_max:.2f}")
    print(f"Income std: {income_std:.2f}")
    print(f"Housing burden avg % of income: {housing_pct_avg:.2f}")
    for col in GASTO_COLS:
        print(f"{GASTO_LABELS[col]} avg % of income: {spending_pct[col]:.2f}")
    print(f"Avg monthly savings (USD): {savings_avg:.2f}")
    print(f"% respondents with negative savings: {neg_savings_pct:.2f}")
    print(f"Avg hours/week using AI tools: {ia_hours_avg:.2f}")
    print(f"Avg financial satisfaction (1-5): {satisfaccion_avg:.2f}")

    # --- assemble markdown ---
    md = []
    md.append(f"## Pais: {COUNTRY}\n")
    md.append("### 1. Sample overview")
    md.append(f"- Sample size: {n} respondents")
    md.append(f"- Age range: {age_min}-{age_max} years\n")
    md.append("### 2. Income (USD)")
    md.append(f"- Median: ${income_median:,.2f}")
    md.append(f"- Mean: ${income_mean:,.2f}")
    md.append(f"- Minimum: ${income_min:,.2f}")
    md.append(f"- Maximum: ${income_max:,.2f}")
    md.append(f"- Standard deviation: ${income_std:,.2f}\n")
    md.append("### 3. Housing burden")
    md.append(f"- Average gasto_vivienda_usd as % of ingreso_mensual_usd: {housing_pct_avg:.1f}%\n")
    md.append("### 4. Spending breakdown (average % of income)")
    for col in GASTO_COLS:
        md.append(f"- {GASTO_LABELS[col]}: {spending_pct[col]:.1f}%")
    md.append("")
    md.append("### 5. Savings")
    md.append(f"- Average ahorro_mensual_usd: ${savings_avg:,.2f}")
    md.append(f"- % of respondents with negative savings: {neg_savings_pct:.1f}%\n")
    md.append("### 6. AI tools and financial satisfaction")
    md.append(f"- Average hours/week using AI financial tools: {ia_hours_avg:.2f}")
    md.append(f"- Average financial satisfaction (scale as recorded): {satisfaccion_avg:.2f}")

    markdown_section = "\n".join(md)
    print("\n\n----- MARKDOWN SECTION -----\n")
    print(markdown_section)


if __name__ == "__main__":
    main()
