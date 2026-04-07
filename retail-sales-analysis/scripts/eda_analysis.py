"""
Exploratory Data Analysis & Visualizations — Retail Sales Performance
Author: Yaradoni Prathapa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── SETUP ─────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.family"] = "DejaVu Sans"
os.makedirs("outputs", exist_ok=True)

# ── LOAD CLEANED DATA ─────────────────────────────────────────────────────────
df = pd.read_csv("data/cleaned_retail.csv", parse_dates=["InvoiceDate"])
print(f"Loaded cleaned data: {df.shape}")
print(df.head())

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1 — Monthly Revenue Trend
# ─────────────────────────────────────────────────────────────────────────────
monthly = (
    df.groupby(["Year", "Month", "MonthName"])["TotalRevenue"]
    .sum()
    .reset_index()
    .sort_values(["Year", "Month"])
)
monthly["Label"] = monthly["MonthName"] + " " + monthly["Year"].astype(str)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["Label"], monthly["TotalRevenue"] / 1000,
        marker="o", linewidth=2.5, color="#2563EB", markersize=6)
ax.fill_between(monthly["Label"], monthly["TotalRevenue"] / 1000,
                alpha=0.12, color="#2563EB")
ax.set_title("Monthly Revenue Trend (Dec 2010 – Dec 2011)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=10)
ax.set_ylabel("Revenue (£ Thousands)", fontsize=10)
plt.xticks(rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}K"))
plt.tight_layout()
plt.savefig("outputs/monthly_revenue_trend.png")
plt.close()
print("✅ Saved: monthly_revenue_trend.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2 — Top 10 Best-Selling Products by Revenue
# ─────────────────────────────────────────────────────────────────────────────
top_products = (
    df.groupby("Description")["TotalRevenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_products["Description"] = top_products["Description"].str[:40]  # truncate long names

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_products["Description"][::-1],
               top_products["TotalRevenue"][::-1] / 1000,
               color=sns.color_palette("Blues_d", 10))
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Revenue (£ Thousands)", fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}K"))
for bar in bars:
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            f"£{bar.get_width():,.1f}K", va="center", fontsize=8)
plt.tight_layout()
plt.savefig("outputs/top10_products.png")
plt.close()
print("✅ Saved: top10_products.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3 — Revenue by Country (Top 10)
# ─────────────────────────────────────────────────────────────────────────────
country_rev = (
    df.groupby("Country")["TotalRevenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
palette = ["#1E40AF" if c == "United Kingdom" else "#93C5FD" for c in country_rev["Country"]]
ax.bar(country_rev["Country"], country_rev["TotalRevenue"] / 1000, color=palette)
ax.set_title("Top 10 Countries by Revenue", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Country", fontsize=10)
ax.set_ylabel("Revenue (£ Thousands)", fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}K"))
plt.xticks(rotation=30, ha="right", fontsize=9)
plt.tight_layout()
plt.savefig("outputs/revenue_by_country.png")
plt.close()
print("✅ Saved: revenue_by_country.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4 — Sales Heatmap: Day of Week × Hour
# ─────────────────────────────────────────────────────────────────────────────
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]
heatmap_data = (
    df[df["DayOfWeek"].isin(day_order)]
    .groupby(["DayOfWeek", "Hour"])["TotalRevenue"]
    .sum()
    .unstack(fill_value=0)
)
heatmap_data = heatmap_data.reindex(day_order)

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(heatmap_data / 1000, cmap="YlOrRd", linewidths=0.3,
            ax=ax, fmt=".0f", annot=True, annot_kws={"size": 7},
            cbar_kws={"label": "Revenue (£K)"})
ax.set_title("Revenue Heatmap: Day of Week × Hour of Day", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Hour of Day", fontsize=10)
ax.set_ylabel("Day of Week", fontsize=10)
plt.tight_layout()
plt.savefig("outputs/sales_heatmap.png")
plt.close()
print("✅ Saved: sales_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5 — Revenue by Day of Week
# ─────────────────────────────────────────────────────────────────────────────
dow_rev = (
    df[df["DayOfWeek"].isin(day_order)]
    .groupby("DayOfWeek")["TotalRevenue"]
    .sum()
    .reindex(day_order)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(dow_rev["DayOfWeek"], dow_rev["TotalRevenue"] / 1000,
       color=sns.color_palette("muted", 6))
ax.set_title("Total Revenue by Day of Week", fontsize=13, fontweight="bold", pad=10)
ax.set_ylabel("Revenue (£ Thousands)", fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}K"))
plt.tight_layout()
plt.savefig("outputs/revenue_by_day.png")
plt.close()
print("✅ Saved: revenue_by_day.png")

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY STATS
# ─────────────────────────────────────────────────────────────────────────────
print("\n========== BUSINESS INSIGHTS SUMMARY ==========")
print(f"Total Revenue         : £{df['TotalRevenue'].sum():,.2f}")
print(f"Total Transactions    : {df['InvoiceNo'].nunique():,}")
print(f"Unique Customers      : {df['CustomerID'].nunique():,}")
print(f"Unique Products       : {df['Description'].nunique():,}")
print(f"Countries Served      : {df['Country'].nunique()}")
print(f"Avg Order Value       : £{df.groupby('InvoiceNo')['TotalRevenue'].sum().mean():.2f}")
print(f"Best Month            : {monthly.loc[monthly['TotalRevenue'].idxmax(), 'Label']}")
print(f"Top Country           : {country_rev.iloc[0]['Country']} "
      f"(£{country_rev.iloc[0]['TotalRevenue']:,.0f})")
print(f"Top Product           : {top_products.iloc[0]['Description']}")
print("================================================\n")
print("All charts saved to outputs/ folder.")
