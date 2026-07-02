"""
Country profile: Brasil
Generates a statistical summary for Brasil from the clean LatAm financial
wellness dataset (data/latam_finanzas_clean.csv).

Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm
"""

import pandas as pd

CLEAN_DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Brasil"

GASTO_COLUMNS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(CLEAN_DATA_PATH)
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

    # 3. Housing burden: gasto_vivienda_usd as % of ingreso_mensual_usd
    housing_pct = (country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"]) * 100
    housing_pct_avg = housing_pct.mean()

    # 4. Spending breakdown: average % of income for each gasto_* column
    spending_breakdown = {}
    for col in GASTO_COLUMNS:
        pct = (country_df[col] / country_df["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    # 5. Savings
    savings_avg = country_df["ahorro_mensual_usd"].mean()
    negative_savings_pct = (country_df["ahorro_mensual_usd"] < 0).mean() * 100

    # 6. AI tools
    ai_hours_avg = country_df["horas_herramientas_ia_semana"].mean()
    satisfaction_avg = country_df["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}")
    print()
    print(f"- Sample size: {n}")
    print(f"- Age range: {age_min}-{age_max}")
    print()
    print("Income (USD):")
    print(f"  median={income_median:.2f}, mean={income_mean:.2f}, "
          f"min={income_min:.2f}, max={income_max:.2f}, std={income_std:.2f}")
    print()
    print(f"Housing burden (avg gasto_vivienda_usd as % of income): {housing_pct_avg:.2f}%")
    print()
    print("Spending breakdown (avg % of income):")
    for col, pct in spending_breakdown.items():
        print(f"  {col}: {pct:.2f}%")
    print()
    print(f"Savings: avg ahorro_mensual_usd = {savings_avg:.2f} USD, "
          f"% with negative savings = {negative_savings_pct:.2f}%")
    print()
    print(f"AI tools: avg horas_herramientas_ia_semana = {ai_hours_avg:.2f}, "
          f"avg satisfaccion_financiera = {satisfaction_avg:.2f}")


if __name__ == "__main__":
    main()
