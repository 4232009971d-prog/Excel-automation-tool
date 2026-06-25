import logging
import pandas as pd

logger = logging.getLogger(__name__)

COLUMN_ALIASES = {
    "order_id": ["order id", "orderid", "order_number", "order no", "id"],
    "date": ["order_date", "date", "shipment_date", "ship_date", "delivery_date"],
    "item": ["item", "product", "product_name", "sku", "item_name", "description"],
    "quantity": ["quantity", "qty", "units", "amount", "count"],
    "status": ["status", "order_status", "shipment_status", "state"],
    "customer": ["customer", "customer_name", "client", "buyer"],
    "region": ["region", "area", "zone", "location", "city", "country"],
    "revenue": ["revenue", "price", "total", "value", "cost", "amount"],
}

STATUS_MAP = {
    "pend": "Pending",
    "ship": "Shipped",
    "deliv": "Delivered",
    "cancel": "Cancelled",
    "return": "Returned",
    "transit": "Shipped",
    "in transit": "Shipped",
    "complete": "Delivered",
    "done": "Delivered",
}

def normalize_columns(df):
    col_map = {}
    lower_cols = {c.lower().strip().replace(" ", "_"): c for c in df.columns}
    for standard, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            normalized = alias.lower().replace(" ", "_")
            if normalized in lower_cols:
                col_map[lower_cols[normalized]] = standard
                break
    df = df.rename(columns=col_map)
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    return df

def clean_data(df):
    report = {}
    original_rows = len(df)
    df = normalize_columns(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = original_rows - len(df)
    df = df.dropna(how="all")
    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue
        if col in ("quantity", "revenue"):
            df[col] = df[col].fillna(0)
        elif col == "status":
            df[col] = df[col].fillna("Unknown")
        elif col == "date":
            df[col] = df[col].fillna(pd.NaT)
        else:
            df[col] = df[col].fillna("N/A")
    report["nulls_filled"] = int(df.isna().sum().sum())
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "status" in df.columns:
        df["status"] = df["status"].astype(str).str.strip().str.lower()
        def map_status(val):
            for key, label in STATUS_MAP.items():
                if key in val:
                    return label
            return val.title()
        df["status"] = df["status"].apply(map_status)
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    if "revenue" in df.columns:
        df["revenue"] = df["revenue"].astype(str).str.replace(r"[^\d.\-]", "", regex=True)
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
    report["final_rows"] = len(df)
    report["original_rows"] = original_rows
    return df, report
