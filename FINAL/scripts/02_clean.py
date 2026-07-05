"""Phase 2: Clean raw survey data and save the analysis-ready dataset."""
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

RAW_PATH = "data/latam_finanzas_2025.csv"
CLEAN_PATH = "data/latam_finanzas_clean.csv"

# Maps every raw spelling/casing/abbreviation variant of 'industria' to one
# canonical label. Keys are matched case-insensitively after stripping accents.
INDUSTRIA_CANONICAL = {
    "educacion": "Educación",
    "tecnologia": "Tecnología",
    "tech": "Tecnología",
    "diseno": "Diseño",
    "recursos humanos": "Recursos Humanos",
    "salud": "Salud",
    "ingenieria": "Ingeniería",
    "retail": "Retail",
    "finanzas": "Finanzas",
    "marketing": "Marketing",
    "ventas": "Ventas",
}


def strip_accents(text):
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "ñ": "n", "Ñ": "n",
    }
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    return text


def standardize_industria(value):
    key = strip_accents(str(value).strip()).lower()
    return INDUSTRIA_CANONICAL.get(key, value)


def main():
    df = pd.read_csv(RAW_PATH)
    rows_before = df.shape[0]
    changes = []

    print("=" * 70)
    print("1. STANDARDIZE 'industria'")
    print("=" * 70)
    print("Unique values BEFORE:")
    print(sorted(df["industria"].unique()))

    n_changed = (df["industria"].apply(standardize_industria) != df["industria"]).sum()
    df["industria"] = df["industria"].apply(standardize_industria)

    print("\nUnique values AFTER:")
    print(sorted(df["industria"].unique()))
    changes.append(f"Standardized 'industria': {n_changed} rows normalized to canonical categories "
                    f"(e.g. 'Tecnologia'/'tech'/'TECNOLOGÍA' -> 'Tecnología')")

    print("\n" + "=" * 70)
    print("2. MISSING VALUES IN NUMERIC COLUMNS")
    print("=" * 70)
    numeric_cols = df.select_dtypes(include="number").columns
    missing_pct = (df[numeric_cols].isna().sum() / len(df) * 100).sort_values(ascending=False)
    print(missing_pct[missing_pct > 0])

    for col in numeric_cols:
        pct = missing_pct.get(col, 0)
        if pct == 0:
            continue
        # Recommendation: fill with median. Percentage missing is small (<10%),
        # so dropping rows would discard otherwise-good survey responses, and
        # the median is robust to the outliers typical of expense data.
        median_val = df[col].median()
        n_missing = df[col].isna().sum()
        print(f"\n{col}: {pct:.1f}% missing ({n_missing} rows) "
              f"-> recommendation: fill with median ({median_val:.2f})")
        df[col] = df[col].fillna(median_val)
        changes.append(f"Filled {n_missing} missing '{col}' values ({pct:.1f}%) with median ({median_val:.2f})")

    print("\n" + "=" * 70)
    print("3. NEGATIVE VALUES IN 'ahorro_mensual_usd'")
    print("=" * 70)
    n_negative = (df["ahorro_mensual_usd"] < 0).sum()
    print(f"Negative values found: {n_negative}")
    df["ahorro_negativo"] = df["ahorro_mensual_usd"] < 0
    changes.append(f"Flagged {n_negative} negative 'ahorro_mensual_usd' rows in new column "
                    f"'ahorro_negativo' (values NOT removed)")

    df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")
    rows_after = df.shape[0]

    print("\n" + "=" * 70)
    print("4. SUMMARY")
    print("=" * 70)
    print(f"Rows before: {rows_before}")
    print(f"Rows after:  {rows_after}")
    print("\nChanges made:")
    for change in changes:
        print(f"- {change}")
    print(f"\nClean dataset saved to: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
