"""Phase 3: Core analyses on the cleaned survey data, shown as formatted tables."""
import sys
import io
import pandas as pd
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

CLEAN_PATH = "data/latam_finanzas_clean.csv"

SPENDING_COLS = {
    "gasto_vivienda_usd": "Vivienda",
    "gasto_alimentacion_usd": "Alimentación",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educación",
    "gasto_salud_usd": "Salud",
}

# Values confirmed from scripts/country_profiles.md (Phase 2.5).
COUNTRY_PROFILE_INCOME = {
    "México":     {"median": 1066.99, "mean": 1042.05, "min": 300.00, "max": 1693.16, "std": 286.61},
    "Colombia":   {"median": 856.62,  "mean": 848.78,  "min": 405.15, "max": 1362.79, "std": 188.70},
    "Argentina":  {"median": 798.49,  "mean": 766.38,  "min": 372.85, "max": 1342.56, "std": 203.94},
    "Chile":      {"median": 1246.01, "mean": 1245.29, "min": 575.20, "max": 1861.10, "std": 289.66},
    "Perú":       {"median": 821.59,  "mean": 817.76,  "min": 361.89, "max": 1341.50, "std": 207.91},
    "Brasil":     {"median": 1458.03, "mean": 1387.97, "min": 300.00, "max": 2874.49, "std": 592.18},
}

COUNTRY_PROFILE_HOUSING_PCT = {
    "México": 28.15,
    "Colombia": 25.4,
    "Argentina": 34.1,
    "Chile": 32.6,
    "Perú": 24.63,
    "Brasil": 26.90,
}


def print_table(df, title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(df.to_string(index=False))


def analysis_1_income_by_country(df):
    computed = df.groupby("pais")["ingreso_mensual_usd"].agg(
        median="median", mean="mean", min="min", max="max", std="std"
    )

    rows = []
    for pais, profile in COUNTRY_PROFILE_INCOME.items():
        c = computed.loc[pais]
        matches = (
            abs(c["median"] - profile["median"]) < 0.01
            and abs(c["mean"] - profile["mean"]) < 0.01
            and abs(c["min"] - profile["min"]) < 0.01
            and abs(c["max"] - profile["max"]) < 0.01
            and abs(c["std"] - profile["std"]) < 0.01
        )
        rows.append({
            "País": pais,
            "Median (USD)": profile["median"],
            "Mean (USD)": profile["mean"],
            "Min (USD)": profile["min"],
            "Max (USD)": profile["max"],
            "Std Dev (USD)": profile["std"],
            "Matches profile": "Yes" if matches else "NO - MISMATCH",
        })

    result = pd.DataFrame(rows).sort_values("Median (USD)", ascending=False)
    print_table(result, "1. INCOME BY COUNTRY (sorted by median, high to low)")
    return result


def analysis_2_age_vs_savings(df):
    bins = [17, 22, 25, 28, 32]
    labels = ["18-22", "23-25", "26-28", "29-32"]
    df = df.copy()
    df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels, include_lowest=True)

    grouped = df.groupby("age_group", observed=True).apply(
        lambda g: pd.Series({
            "n": len(g),
            "Avg monthly savings (USD)": g["ahorro_mensual_usd"].mean(),
            "Avg monthly income (USD)": g["ingreso_mensual_usd"].mean(),
        }),
        include_groups=False,
    )
    grouped["Savings rate (%)"] = (
        grouped["Avg monthly savings (USD)"] / grouped["Avg monthly income (USD)"] * 100
    )
    grouped = grouped.reset_index().rename(columns={"age_group": "Age group"})
    grouped["n"] = grouped["n"].astype(int)
    grouped = grouped[["Age group", "n", "Avg monthly savings (USD)", "Avg monthly income (USD)", "Savings rate (%)"]]

    print_table(grouped, "2. AGE VS. SAVINGS")
    return grouped


def analysis_3_spending_breakdown(df):
    pct_of_income = pd.DataFrame({
        label: df[col] / df["ingreso_mensual_usd"] * 100
        for col, label in SPENDING_COLS.items()
    })
    result = pct_of_income.mean().sort_values(ascending=False).reset_index()
    result.columns = ["Category", "Avg % of income"]

    print_table(result, "3. SPENDING BREAKDOWN (full sample, sorted high to low)")
    return result


def analysis_4_credit_card(df):
    metrics = {
        "Avg income (USD)": "ingreso_mensual_usd",
        "Avg food spending (USD)": "gasto_alimentacion_usd",
        "Avg entertainment spending (USD)": "gasto_entretenimiento_usd",
        "Avg savings (USD)": "ahorro_mensual_usd",
    }
    has_card = df[df["tiene_tarjeta_credito"] == "Sí"]
    no_card = df[df["tiene_tarjeta_credito"] == "No"]

    rows = []
    for label, col in metrics.items():
        with_val = has_card[col].mean()
        without_val = no_card[col].mean()
        pct_diff = (with_val - without_val) / without_val * 100
        rows.append({
            "Metric": label,
            "Credit card holders": with_val,
            "Non-holders": without_val,
            "% difference": pct_diff,
        })

    result = pd.DataFrame(rows)
    print_table(result, "4. CREDIT CARD HOLDERS VS NON-HOLDERS "
                         f"(n={len(has_card)} holders, n={len(no_card)} non-holders)")
    return result


def analysis_5_ai_usage_vs_satisfaction(df):
    def usage_group(hours):
        if hours <= 3:
            return "Low (0-3h)"
        elif hours <= 10:
            return "Medium (4-10h)"
        else:
            return "High (11h+)"

    df = df.copy()
    df["usage_group"] = df["horas_herramientas_ia_semana"].apply(usage_group)
    order = ["Low (0-3h)", "Medium (4-10h)", "High (11h+)"]

    grouped = df.groupby("usage_group", observed=True).agg(
        n=("id", "count"),
        avg_satisfaction=("satisfaccion_financiera", "mean"),
        avg_income=("ingreso_mensual_usd", "mean"),
    ).reindex(order).reset_index()
    grouped.columns = ["AI usage group", "n", "Avg satisfaction", "Avg income (USD)"]

    print_table(grouped, "5. AI TOOL USAGE VS FINANCIAL SATISFACTION")

    corr, p_value = stats.pearsonr(df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"])
    print(f"\nPearson correlation (hours AI tools/week vs. financial satisfaction): "
          f"r = {corr:.4f}, p = {p_value:.4f}")
    return grouped, corr, p_value


def analysis_6_housing_burden(df):
    computed = (df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100).groupby(df["pais"]).mean()

    rows = []
    for pais, pct in COUNTRY_PROFILE_HOUSING_PCT.items():
        matches = abs(computed.loc[pais] - pct) < 0.1
        rows.append({
            "País": pais,
            "Housing burden (% of income)": pct,
            "Matches profile": "Yes" if matches else "NO - MISMATCH",
        })

    result = pd.DataFrame(rows).sort_values("Housing burden (% of income)", ascending=False)
    print_table(result, "6. HOUSING BURDEN BY COUNTRY (sorted high to low)")
    return result


def main():
    df = pd.read_csv(CLEAN_PATH, encoding="utf-8")

    analysis_1_income_by_country(df)
    analysis_2_age_vs_savings(df)
    analysis_3_spending_breakdown(df)
    analysis_4_credit_card(df)
    analysis_5_ai_usage_vs_satisfaction(df)
    analysis_6_housing_burden(df)

    print("\n" + "=" * 70)
    print("Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm")
    print("=" * 70)


if __name__ == "__main__":
    main()
