\# Data Quality Log — Phase 2



This log documents the data cleaning decisions made in `scripts/02\_clean.py`,

applied to `data/latam\_finanzas\_2025.csv` (raw) → `data/latam\_finanzas\_clean.csv` (clean).



\## 1. Inconsistencies in `industria`

The `industria` column contained 13 raw spelling and capitalization variants

(e.g., "Tecnologia," "tech," "TECNOLOGÍA") that were standardized into

10 canonical categories (e.g., all normalized to "Tecnología").



\## 2. Missing Values — `gasto\_salud\_usd`

Only `gasto\_salud\_usd` had missing values, affecting 33 rows (6.6% of the dataset).

Since the share was small and health expense data tends to be skewed, missing

values were filled with the median (45.66 USD) rather than the mean, to avoid

distortion from outliers.



\## 3. Negative Savings

74 respondents had negative values in `ahorro\_mensual\_usd`. These were flagged

(not removed) using a new boolean column, `ahorro\_negativo`, preserving the

original data for further analysis.



\## Summary

\- Rows before cleaning: 500

\- Rows after cleaning: 500 (no rows dropped)

\- Columns before: 21

\- Columns after: 22 (added `ahorro\_negativo`)

