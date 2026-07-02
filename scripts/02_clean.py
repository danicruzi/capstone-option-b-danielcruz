"""
Phase 2: Clean the raw survey data.
Datos que Hablan — Financial Wellness of Young Professionals in Latin America
"""

import sys
import unicodedata

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

RAW_DATA_PATH = "data/latam_finanzas_2025.csv"
CLEAN_DATA_PATH = "data/latam_finanzas_clean.csv"

# Canonical industria values (already consistent in the raw data).
CANONICAL_INDUSTRIAS = [
    "Finanzas",
    "Ingeniería",
    "Ventas",
    "Marketing",
    "Salud",
    "Tecnología",
    "Educación",
    "Diseño",
    "Recursos Humanos",
    "Retail",
]

# Aliases that don't reduce to a canonical name just by stripping accents/case
# (e.g. English abbreviations).
MANUAL_ALIASES = {
    "tech": "Tecnología",
}


def strip_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def build_industria_map(values):
    canonical_lookup = {strip_accents(c).lower(): c for c in CANONICAL_INDUSTRIAS}
    mapping = {}
    for value in values:
        key = strip_accents(value).strip().lower()
        if key in canonical_lookup:
            mapping[value] = canonical_lookup[key]
        elif key in MANUAL_ALIASES:
            mapping[value] = MANUAL_ALIASES[key]
        else:
            mapping[value] = value
    return mapping


def clean_industria(df):
    print("\n" + "=" * 70)
    print("1. INDUSTRIA — STANDARDIZATION")
    print("=" * 70)

    print("\nUnique values BEFORE:")
    print(sorted(df["industria"].unique()))

    mapping = build_industria_map(df["industria"].unique())
    changed = {k: v for k, v in mapping.items() if k != v}
    df["industria"] = df["industria"].map(mapping)

    print("\nValues remapped:")
    for old, new in changed.items():
        print(f"  '{old}' -> '{new}'")

    print("\nUnique values AFTER:")
    print(sorted(df["industria"].unique()))

    return df, changed


def handle_missing_numeric(df):
    print("\n" + "=" * 70)
    print("2. MISSING VALUES — NUMERIC COLUMNS")
    print("=" * 70)

    numeric_cols = df.select_dtypes(include="number").columns
    missing_pct = (df[numeric_cols].isnull().mean() * 100).sort_values(ascending=False)

    filled_cols = []
    for col, pct in missing_pct.items():
        if pct == 0:
            continue
        # Moderate missingness on a spend column: fill with the median
        # (robust to outliers) rather than dropping ~6% of rows or
        # leaving gaps that would break downstream aggregations/charts.
        recommendation = "fill with median" if pct < 15 else "review manually"
        print(f"  {col}: {pct:.2f}% missing -> {recommendation}")
        if pct < 15:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            filled_cols.append((col, median_value))

    if not filled_cols:
        print("  No missing values found in numeric columns.")
    else:
        print("\nApplied fills:")
        for col, median_value in filled_cols:
            print(f"  {col}: filled {missing_pct[col]:.2f}% of rows with median ({median_value:.2f})")

    return df, filled_cols


def flag_negative_savings(df):
    print("\n" + "=" * 70)
    print("3. AHORRO_MENSUAL_USD — NEGATIVE VALUES")
    print("=" * 70)

    negative_count = (df["ahorro_mensual_usd"] < 0).sum()
    print(f"Negative values found: {negative_count} (kept as-is, not removed)")

    df["ahorro_negativo"] = df["ahorro_mensual_usd"] < 0
    print("Added boolean column 'ahorro_negativo'.")

    return df, negative_count


def main():
    df = pd.read_csv(RAW_DATA_PATH)
    rows_before = df.shape[0]
    cols_before = df.shape[1]

    df, industria_changes = clean_industria(df)
    df, filled_cols = handle_missing_numeric(df)
    df, negative_count = flag_negative_savings(df)

    df.to_csv(CLEAN_DATA_PATH, index=False)

    print("\n" + "=" * 70)
    print("4. SUMMARY")
    print("=" * 70)
    print(f"Rows before: {rows_before}")
    print(f"Rows after:  {df.shape[0]}")
    print(f"Columns before: {cols_before}")
    print(f"Columns after:  {df.shape[1]} (+ahorro_negativo)")
    print(f"\nIndustria values standardized: {len(industria_changes)} variant(s) remapped")
    for col, median_value in filled_cols:
        print(f"Missing '{col}' filled with median ({median_value:.2f})")
    print(f"Negative savings flagged: {negative_count} rows (ahorro_negativo=True)")
    print(f"\nClean file saved to: {CLEAN_DATA_PATH}")


if __name__ == "__main__":
    main()
