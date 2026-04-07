"""
Data Cleaning Script — Retail Sales Performance Analysis
Author: Yaradoni Prathapa
Dataset: UCI Online Retail Dataset
"""

import pandas as pd
import numpy as np
import os

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
print("Loading dataset...")

# If you have the Excel file:
# df = pd.read_excel("data/Online Retail.xlsx")

# If you have the CSV file:
df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")

print(f"Raw shape: {df.shape}")
print(f"\nColumn names: {df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ── 2. INITIAL INSPECTION ─────────────────────────────────────────────────────
print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Basic Stats ---")
print(df.describe())

# ── 3. DATA CLEANING STEPS ───────────────────────────────────────────────────

# Step 1: Drop rows with missing CustomerID (cannot track customer behaviour)
before = len(df)
df.dropna(subset=["CustomerID"], inplace=True)
print(f"\nStep 1 — Dropped {before - len(df)} rows with missing CustomerID")

# Step 2: Remove cancelled orders (InvoiceNo starting with 'C')
cancelled = df[df["InvoiceNo"].astype(str).str.startswith("C")]
print(f"Step 2 — Identified {len(cancelled)} cancelled transactions")
df_clean = df[~df["InvoiceNo"].astype(str).str.startswith("C")].copy()

# Step 3: Remove rows with Quantity <= 0 or UnitPrice <= 0
before = len(df_clean)
df_clean = df_clean[(df_clean["Quantity"] > 0) & (df_clean["UnitPrice"] > 0)]
print(f"Step 3 — Removed {before - len(df_clean)} rows with invalid Quantity/Price")

# Step 4: Remove duplicate rows
before = len(df_clean)
df_clean.drop_duplicates(inplace=True)
print(f"Step 4 — Removed {before - len(df_clean)} duplicate rows")

# Step 5: Fix data types
df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"])
df_clean["CustomerID"] = df_clean["CustomerID"].astype(int).astype(str)
print("Step 5 — Fixed data types (InvoiceDate → datetime, CustomerID → str)")

# Step 6: Feature engineering — add TotalRevenue column
df_clean["TotalRevenue"] = df_clean["Quantity"] * df_clean["UnitPrice"]
print("Step 6 — Created TotalRevenue column (Quantity × UnitPrice)")

# Step 7: Extract date/time features
df_clean["Year"]       = df_clean["InvoiceDate"].dt.year
df_clean["Month"]      = df_clean["InvoiceDate"].dt.month
df_clean["MonthName"]  = df_clean["InvoiceDate"].dt.strftime("%b")
df_clean["DayOfWeek"]  = df_clean["InvoiceDate"].dt.day_name()
df_clean["Hour"]       = df_clean["InvoiceDate"].dt.hour
print("Step 7 — Extracted Year, Month, DayOfWeek, Hour features")

# ── 4. SAVE CLEANED DATA ──────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df_clean.to_csv("data/cleaned_retail.csv", index=False)

print(f"\n✅ Cleaning complete. Final shape: {df_clean.shape}")
print(f"Cleaned file saved to: data/cleaned_retail.csv")
print(f"\nSample of cleaned data:\n{df_clean.head()}")
