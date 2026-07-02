"""
Phase 1: Initial exploration of the raw survey data.
Datos que Hablan — Financial Wellness of Young Professionals in Latin America
"""

import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

RAW_DATA_PATH = "data/latam_finanzas_2025.csv"

CATEGORICAL_COLUMNS = [
    "pais",
    "industria",
    "ocupacion",
    "meta_financiera",
    "tiene_tarjeta_credito",
    "tiene_cuenta_ahorro",
    "tiene_deuda",
]


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    print("=" * 70)
    print("1. SHAPE")
    print("=" * 70)
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n" + "=" * 70)
    print("2. COLUMNS AND DATA TYPES")
    print("=" * 70)
    print(df.dtypes)

    print("\n" + "=" * 70)
    print("3. MISSING VALUES (most to least)")
    print("=" * 70)
    missing = df.isnull().sum().sort_values(ascending=False)
    print(missing)

    print("\n" + "=" * 70)
    print("4. BASIC STATISTICS — NUMERIC COLUMNS")
    print("=" * 70)
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.agg(["min", "max", "mean", "median", "std"]).T
    print(stats)

    print("\n" + "=" * 70)
    print("5. CATEGORICAL COLUMNS — VALUE COUNTS")
    print("=" * 70)
    for col in CATEGORICAL_COLUMNS:
        if col not in df.columns:
            print(f"\n[!] Column '{col}' not found in dataset — skipping.")
            continue
        print(f"\n--- {col} ---")
        print(df[col].value_counts(dropna=False))


if __name__ == "__main__":
    main()
