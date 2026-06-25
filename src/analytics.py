import pandas as pd

def compute_kpis(df):
    kpis = {
        "total_orders": len(df),
        "total_quantity": int(df["quantity"].sum()) if "quantity" in df.columns else 0,
        "total_revenue": round(float(df["revenue"].sum()), 2) if "revenue" in df.columns else 0.0,
        "unique_items": df["item"].nunique() if "item" in df.columns else 0,
        "unique_customers": df["customer"].nunique() if "customer" in df.columns else 0,
    }
    return kpis

def status_breakdown(df):
    if "status" not in df.columns:
        return pd.DataFrame()
    breakdown = (
        df.groupby("status")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    breakdown["pct"] = (breakdown["count"] / breakdown["count"].sum() * 100).round(1)
    return breakdown

def top_items(df, n=10):
    if "item" not in df.columns or "quantity" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("item")["quantity"]
        .sum()
        .reset_index()
        .rename(columns={"quantity": "total_quantity"})
        .sort_values("total_quantity", ascending=False)
        .head(n)
    )

def revenue_by_region(df):
    if "region" not in df.columns or "revenue" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("region")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
    )

def orders_over_time(df, freq="ME"):
    if "date" not in df.columns:
        return pd.DataFrame()
    ts = df.dropna(subset=["date"]).copy()
    ts["period"] = ts["date"].dt.to_period(freq).dt.to_timestamp()
    return (
        ts.groupby("period")
        .size()
        .reset_index(name="order_count")
        .sort_values("period")
    )
