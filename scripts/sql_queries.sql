-- ============================================================
-- SQL Business Queries — Retail Sales Performance Analysis
-- Author: Yaradoni Prathapa
-- Database: SQLite (run via Python or DB Browser for SQLite)
-- ============================================================

-- ── 1. TOTAL REVENUE & TRANSACTIONS ──────────────────────────────────────────
SELECT
    COUNT(DISTINCT InvoiceNo)                        AS total_transactions,
    COUNT(DISTINCT CustomerID)                       AS unique_customers,
    COUNT(DISTINCT Description)                      AS unique_products,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS total_revenue,
    ROUND(AVG(Quantity * UnitPrice), 2)              AS avg_order_value
FROM retail_sales;

-- ── 2. MONTHLY REVENUE TREND ──────────────────────────────────────────────────
SELECT
    strftime('%Y', InvoiceDate)                      AS year,
    strftime('%m', InvoiceDate)                      AS month,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS monthly_revenue,
    COUNT(DISTINCT InvoiceNo)                        AS orders
FROM retail_sales
GROUP BY year, month
ORDER BY year, month;

-- ── 3. TOP 10 PRODUCTS BY REVENUE ─────────────────────────────────────────────
SELECT
    Description                                      AS product,
    SUM(Quantity)                                    AS total_qty_sold,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS total_revenue
FROM retail_sales
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;

-- ── 4. REVENUE BY COUNTRY ─────────────────────────────────────────────────────
SELECT
    Country,
    COUNT(DISTINCT InvoiceNo)                        AS orders,
    COUNT(DISTINCT CustomerID)                       AS customers,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS revenue,
    ROUND(SUM(Quantity * UnitPrice) * 100.0 /
        SUM(SUM(Quantity * UnitPrice)) OVER (), 2)  AS revenue_pct
FROM retail_sales
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;

-- ── 5. TOP 10 CUSTOMERS BY REVENUE (CUSTOMER VALUE) ──────────────────────────
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo)                        AS orders,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS lifetime_value,
    ROUND(AVG(Quantity * UnitPrice), 2)              AS avg_order_value
FROM retail_sales
GROUP BY CustomerID
ORDER BY lifetime_value DESC
LIMIT 10;

-- ── 6. CANCELLATION RATE ──────────────────────────────────────────────────────
SELECT
    SUM(CASE WHEN InvoiceNo LIKE 'C%' THEN 1 ELSE 0 END) AS cancelled_orders,
    COUNT(*)                                              AS total_orders,
    ROUND(
        100.0 * SUM(CASE WHEN InvoiceNo LIKE 'C%' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                     AS cancellation_rate_pct
FROM retail_sales;

-- ── 7. REVENUE BY HOUR OF DAY ─────────────────────────────────────────────────
SELECT
    CAST(strftime('%H', InvoiceDate) AS INTEGER)     AS hour_of_day,
    ROUND(SUM(Quantity * UnitPrice), 2)              AS revenue,
    COUNT(DISTINCT InvoiceNo)                        AS orders
FROM retail_sales
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- ── 8. MONTH-OVER-MONTH REVENUE GROWTH ───────────────────────────────────────
WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate)               AS month,
        ROUND(SUM(Quantity * UnitPrice), 2)          AS revenue
    FROM retail_sales
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month)              AS prev_month_revenue,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) /
        LAG(revenue) OVER (ORDER BY month),
        2
    )                                               AS mom_growth_pct
FROM monthly
ORDER BY month;

-- ── 9. PRODUCTS WITH HIGH RETURN/CANCELLATION RATE ───────────────────────────
SELECT
    Description,
    SUM(CASE WHEN InvoiceNo LIKE 'C%' THEN ABS(Quantity) ELSE 0 END) AS returned_qty,
    SUM(CASE WHEN InvoiceNo NOT LIKE 'C%' THEN Quantity ELSE 0 END)   AS sold_qty,
    ROUND(
        100.0 * SUM(CASE WHEN InvoiceNo LIKE 'C%' THEN ABS(Quantity) ELSE 0 END) /
        NULLIF(SUM(CASE WHEN InvoiceNo NOT LIKE 'C%' THEN Quantity ELSE 0 END), 0),
        2
    )                                                                  AS return_rate_pct
FROM retail_sales
GROUP BY Description
HAVING sold_qty > 100
ORDER BY return_rate_pct DESC
LIMIT 10;
