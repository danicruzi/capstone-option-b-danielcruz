\# Working Notes



\## Phase 1 — Exploration Notes



\*\*Data cleanliness:\*\* Well, not really, but the "industria" column has inconsistent category labels for the same industry: "Tecnología" (47), "Tecnologia", "tech", "TECNOLOGÍA". All other columns seem to be fine.



\*\*Missing values:\*\* Only gasto\_salud\_usd has missing data.



\*\*Min/max sanity check:\*\* ahorro\_mensual\_usd has a minimum of -160.02, meaning some

respondents spend more than they earn — this is a valid data point, not an error, and

will be flagged in Phase 2. deuda\_total\_usd ranges from 0 to 10,918.73

with a median of 0, meaning most respondents report no debt, while a smaller group of

debtors skews the average upward — expected, not an error.





\## Phase 2 — Cleaning Notes



\*\*Problem 1 — Inconsistent "industria" labels: The industria column had 13 unique

values, including 4 variants representing the same industry ("Tecnología,"

"Tecnologia," "tech," "TECNOLOGÍA"). Decision: standardized all variants to

"Tecnología," reducing the column to 10 unique values. This affects all rows

where industria contained any of the 3 non-standard variants.



\*\*Problem 2 — Missing values in "gasto\_salud\_usd":33 rows (6.6% of the dataset)

were missing healthcare spending data. Decision: filled with the column median

(45.66 USD) rather than dropping rows, to preserve sample size for downstream

aggregations and charts. A 6.6% gap was considered too significant to drop without

losing meaningful data.



\*\*Negative savings values:74 rows have negative ahorro\_mensual\_usd (spending

exceeds income). These are valid data points, not errors, and were kept as-is.

A new boolean column, ahorro\_negativo, was added to flag these rows for analysis.



\*\*Result:\*\* Clean dataset saved to data/latam\_finanzas\_clean.csv (500 rows, 22

columns). Original raw file (data/latam\_finanzas\_2025.csv) remains untouched.

