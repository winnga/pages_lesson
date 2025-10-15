---
title: "Workshop Exercise: Emissions Data - Table, Map, and Chart"
format: html
---

# Introduction

In this exercise, you will work with a CO2 emissions dataset downloaded from Gapminder and produce a report with three tabs: a data table, a line chart, and a choropleth map. 

The goal is to roughly replicate the [Our World in Data visualization page on consumption-based CO2 emissions](https://ourworldindata.org/grapher/consumption-co2-emissions?tab=table&time=2000..2022).

# Setup

- Fork and clone this repository to your local machine.
- Create and select a virtual environment in VSCode.
- Install the following packages: pandas, plotly, itables, ipykernel, jupyter, country_converter
- Download the CO2 emissions CSV from Gapminder into a `data` folder.

# Data Import

```{python}
import pandas as pd
import numpy as np
import plotly.express as px
from itables import show
import country_converter as coco
```

```{python}
# Load the CSV
df = pd.read_csv(r"C:\Users\LENOVO\Documents\GitHub\pages_lesson\owid-co2-data.csv")

# Select relevant columns
df_co2 = df[["country", "year", "co2"]]

# Pivot the table: countries as rows, years as columns, CO2 as values
df_pivot = df_co2.pivot(index="country", columns="year", values="co2")

# Convert column names to integers
df_pivot.columns = df_pivot.columns.astype(int)

# Keep for future use
emissions_df = df_pivot.copy()

print(df_pivot.head())
```

# Table Section

```{python}
# Reset index to make 'country' a column
table_df = df_pivot.reset_index()[["country", 2000, 2022]].copy()

# Absolute change
table_df["Absolute Change"] = table_df[2022] - table_df[2000]

# Relative change
table_df["Relative Change"] = (table_df["Absolute Change"] / table_df[2000]) * 100

# Format
table_df["Relative Change"] = table_df["Relative Change"].round(0).astype(str) + "%"

print(table_df.head())
```

```{python}
show(table_df)
```

# Chart Section

```{python}
# Melt dataframe for plotting
emissions_long = df_pivot.reset_index().melt(
    id_vars="country", var_name="year", value_name="emissions"
)

# Convert to numeric
emissions_long["year"] = pd.to_numeric(emissions_long["year"], errors="coerce")
emissions_long["emissions"] = pd.to_numeric(
    emissions_long["emissions"].astype(str).str.replace("−", "-"), errors="coerce"
)

# Filter 1990-2022
emissions_long_1990_2022 = emissions_long.query("year >= 1990 & year <= 2022")

# Select 5 countries
selected_countries = ["China", "United States", "India", "Germany", "Brazil"]
emissions_long_subset = emissions_long_1990_2022.query("country in @selected_countries")

# Plot line chart
fig_chart = px.line(
    emissions_long_subset,
    x="year",
    y="emissions",
    color="country",
    markers=True,
    title="CO2 Emissions (1990–2022) for Selected Countries"
)

fig_chart.show()
```

# Mapping Section

```{python}
# Convert country names to ISO3 codes
emissions_long_1990_2022["country_code"] = coco.convert(
    emissions_long_1990_2022["country"], to="ISO3"
)

# Plot choropleth map
fig_map = px.choropleth(
    emissions_long_1990_2022,
    locations="country_code",
    color="emissions",
    hover_name="country",
    animation_frame="year",
    title="Global CO2 Emissions (1990-2022)"
)

fig_map.show()
```

# Final Tabset

::: {.panel-tabset}

## Table

```{python}
show(table_df)
```

## Chart

```{python}
fig_chart.show()
```

## Map

```{python}
fig_map.show()
```

:::

# Deploying to GitHub Pages

Follow the prework steps to deploy your report to GitHub Pages.
