import io
import random
from datetime import datetime, timedelta
import pandas as pd

ITEMS = [
    "Industrial Valve", "Steel Pipe 2in", "Safety Helmet", "Forklift Battery",
    "Conveyor Belt", "Pallet Jack", "Hydraulic Pump", "Electric Motor 5HP",
    "PVC Tubing", "Pressure Gauge", "Cable Reel 50m", "Warehouse Racking",
    "LED Flood Light", "Air Compressor", "Diesel Generator",
]
CUSTOMERS = [
    "AcmeCorp", "GlobalTrans", "FastFreight", "PrimeParts", "MetroSupply",
    "NorthStar Logistics", "Omega Industries", "BlueLine Shipping",
]
REGIONS = ["North", "South", "East", "West", "Central"]
STATUSES = ["Pending", "Shipped", "Delivered", "Delivered", "Delivered", "Cancelled"]

def generate_sample(n_rows=200, introduce_issues=True):
    random.seed(42)
    base_date = datetime(2024, 1, 1)
    rows = []
    for i in range(1, n_rows + 1):
        date = base_date + timedelta(days=random.randint(0, 364))
        item = random.choice(ITEMS)
        qty = random.randint(1, 150)
        price_per_unit = round(random.uniform(10, 500), 2)
        revenue = round(qty * price_per_unit, 2)
        rows.append({
            "Order ID": f"ORD-{i:04d}",
            "Date": date.strftime("%Y-%m-%d"),
            "Item": item,
            "Quantity": qty,
            "Revenue": revenue,
            "Status": random.choice(STATUSES),
            "Customer": random.choice(CUSTOMERS),
            "Region": random.choice(REGIONS),
        })
    df = pd.DataFrame(rows)
    if introduce_issues:
        dup_idx = random.sample(range(len(df)), k=int(n_rows * 0.05))
        df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)
        for col in ["Status", "Quantity", "Customer"]:
            null_idx = random.sample(range(len(df)), k=int(len(df) * 0.03))
            df.loc[null_idx, col] = None
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()
