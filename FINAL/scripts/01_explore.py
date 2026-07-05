"""Phase 1: Explore raw survey data before any cleaning."""
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

DATA_PATH = "data/latam_finanzas_2025.csv"

CATEGORICAL_COLS = [
    "pais",
    "industria",
    "ocupacion",
    "meta_financiera",
    "tiene_tarjeta_credito",
    "tiene_cuenta_ahorro",
    "tiene_deuda",
]


def main():
    df = pd.read_csv(DATA_PATH)

    print("=" * 70)
    print("1. SHAPE")
    print("=" * 70)
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n" + "=" * 70)
    print("2. COLUMNS AND DATA TYPES")
    print("=" * 70)
    print(df.dtypes)

    print("\n" + "=" * 70)
    print("3. MISSING VALUES (most to least)")
    print("=" * 70)
    missing = df.isna().sum().sort_values(ascending=False)
    print(missing)

    print("\n" + "=" * 70)
    print("4. NUMERIC COLUMN STATISTICS")
    print("=" * 70)
    numeric_df = df.select_dtypes(include="number")
    stats = pd.DataFrame({
        "min": numeric_df.min(),
        "max": numeric_df.max(),
        "mean": numeric_df.mean(),
        "median": numeric_df.median(),
        "std": numeric_df.std(),
    })
    print(stats)

    print("\n" + "=" * 70)
    print("5. CATEGORICAL COLUMN VALUE COUNTS")
    print("=" * 70)
    for col in CATEGORICAL_COLS:
        if col not in df.columns:
            print(f"\n--- {col} --- (column not found)")
            continue
        print(f"\n--- {col} ---")
        print(df[col].value_counts(dropna=False))


if __name__ == "__main__":
    main()
