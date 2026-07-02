\# Working Notes



\## Phase 1 — Exploration Notes



\*\*Data cleanliness:\*\* Well, not really, but the "industria" column has inconsistent category labels for the same industry: "Tecnología" (47), "Tecnologia", "tech", "TECNOLOGÍA". All other columns seem to be fine. 



\*\*Missing values:\*\* Only gasto\_salud\_usd has missing data.



\*\*Min/max sanity check:\*\* ahorro\_mensual\_usd has a minimum of -160.02, meaning some

respondents spend more than they earn — this is a valid data point, not an error, and

will be flagged in Phase 2. deuda\_total\_usd ranges from 0 to 10,918.73

with a median of 0, meaning most respondents report no debt, while a smaller group of

debtors skews the average upward — expected, not an error.

