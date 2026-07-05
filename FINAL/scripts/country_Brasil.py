"""
Country statistical profile: Brasil
Part of the Analisis LatAm 2025 pipeline (Futuro Digital LatAm).

Reads data/latam_finanzas_clean.csv (relative to project root),
filters to pais == "Brasil", and prints a full statistical profile:
  1. Sample size and age range
  2. Income stats (median, mean, min, max, std)
  3. Housing burden (% of income)
  4. Spending breakdown (% of income per gasto_* category)
  5. Savings (average and % with negative savings)
  6. AI tool usage and financial satisfaction
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Brasil"

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
    sub = df[df["pais"] == COUNTRY].copy()

    n = len(sub)
    age_min, age_max = sub["edad"].min(), sub["edad"].max()

    print(f"=== Country profile: {COUNTRY} ===\n")

    # 1. Sample size and age range
    print("1. Sample size and age range")
    print(f"   n = {n}")
    print(f"   age range = {age_min:.0f} - {age_max:.0f}\n")

    # 2. Income stats
    income = sub["ingreso_mensual_usd"]
    print("2. Income (USD)")
    print(f"   median = {income.median():.2f}")
    print(f"   mean   = {income.mean():.2f}")
    print(f"   min    = {income.min():.2f}")
    print(f"   max    = {income.max():.2f}")
    print(f"   std    = {income.std():.2f}\n")

    # 3. Housing burden (% of income)
    housing_pct = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"] * 100)
    print("3. Housing burden")
    print(f"   avg gasto_vivienda_usd as % of ingreso_mensual_usd = {housing_pct.mean():.2f}%\n")

    # 4. Spending breakdown (% of income per category)
    print("4. Spending breakdown (average % of income)")
    spending_pct = {}
    for col in GASTO_COLS:
        pct = (sub[col] / sub["ingreso_mensual_usd"] * 100).mean()
        spending_pct[col] = pct
        print(f"   {col} = {pct:.2f}%")
    print()

    # 5. Savings
    avg_savings = sub["ahorro_mensual_usd"].mean()
    # Check reliability of ahorro_negativo flag vs. computed from ahorro_mensual_usd
    computed_negative = (sub["ahorro_mensual_usd"] < 0)
    if "ahorro_negativo" in sub.columns:
        flag_negative = sub["ahorro_negativo"].astype(bool)
        mismatch = (flag_negative != computed_negative).sum()
        print("5. Savings")
        print(f"   [check] rows where ahorro_negativo flag disagrees with (ahorro_mensual_usd < 0): {mismatch} / {n}")
        if mismatch == 0:
            pct_negative = flag_negative.mean() * 100
            print("   using ahorro_negativo column (matches computed values exactly)")
        else:
            pct_negative = computed_negative.mean() * 100
            print("   using computed (ahorro_mensual_usd < 0) because flag disagreed with raw values")
    else:
        pct_negative = computed_negative.mean() * 100
        print("5. Savings")
        print("   ahorro_negativo column not present; using computed (ahorro_mensual_usd < 0)")

    print(f"   avg ahorro_mensual_usd = {avg_savings:.2f} USD")
    print(f"   % respondents with negative savings = {pct_negative:.2f}%\n")

    # 6. AI tools
    avg_ia_hours = sub["horas_herramientas_ia_semana"].mean()
    avg_satisfaction = sub["satisfaccion_financiera"].mean()
    print("6. AI tools and satisfaction")
    print(f"   avg horas_herramientas_ia_semana = {avg_ia_hours:.2f}")
    print(f"   avg satisfaccion_financiera      = {avg_satisfaction:.2f}")


if __name__ == "__main__":
    main()
