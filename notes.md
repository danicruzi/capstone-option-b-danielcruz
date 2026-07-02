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





\## Phase 2.5 — Country Profiler Agent Notes



Created a custom country-profiler agent (.claude/agents/country-profiler.md) and

invoked it for all 6 countries in parallel. Results were combined into

scripts/country\_profiles.md.



Note: the agent file initially had a frontmatter formatting error (broken --- markers),

which caused Claude Code to fall back to a general-purpose agent for this run. The

file has since been corrected and should work as a proper custom agent going forward.



All 6 country sections were generated successfully with plausible income and housing

burden figures consistent with Phase 1 exploration.



\## Phase 3 — Analysis Notes



Income: Brasil highest ($1,458 median), Argentina lowest ($798).

Age vs. savings: Savings rate triples from 5.72% (18-22) to 15.52% (29-32).

Spending: Housing (28.54%) and food (23.83%) dominate.

Credit card holders: Spend more on food/entertainment, save slightly more than non-holders.

AI usage: Moderate correlation with satisfaction (r = 0.571), likely tied to income too.

Housing burden: Argentina highest (34.09%), Perú lowest (24.63%).



\## Phase 4 — Visualization Notes



\## Phase 4 — Visualization Notes



Generated all 5 required charts in charts/: income by country, age vs.

savings, spending breakdown, satisfaction by

AI usage, and housing burden by country. All charts include titles, labelled axes, and the required source note.

