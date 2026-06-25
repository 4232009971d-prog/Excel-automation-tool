# 📦 Excel Automation Tool — Logistics & Supply Chain

A job-ready Python + Streamlit data automation project for logistics and supply chain analysis. Upload raw Excel order data, auto-clean it, explore interactive dashboards, and export polished reports — all in a browser.

---

## 🚀 Features

| Feature | Details |
|---|---|
| **File Upload** | `.xlsx` / `.xls` logistics/order files |
| **Auto Cleaning** | Removes duplicates, fills nulls, standardises status values & date formats |
| **KPI Cards** | Total orders, quantity, revenue, unique items & customers |
| **Charts** | Pie (status), bar (top items), line (orders over time), bar (revenue by region) |
| **Data Tables** | Filterable cleaned data + breakdown tables |
| **Export** | Cleaned Excel + multi-sheet summary report |
| **Demo Mode** | One-click sample data generation (no file needed) |
| **Tests** | Pytest unit tests for cleaner and analytics modules |

---

## 📁 Project Structure

```
excel_automation_tool/
├── app.py                  # Streamlit entry point
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── cleaner.py          # Data cleaning logic
│   ├── analytics.py        # KPIs & breakdowns
│   ├── exporter.py         # Excel export formatting
│   └── sample_data.py      # Demo data generator
└── tests/
    └── test_cleaner_analytics.py
```

---

## ⚙️ Setup

### 1. Clone / download the project
```bash
git clone https://github.com/yourname/excel-automation-tool.git
cd excel-automation-tool
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Expected Input Format

The tool auto-detects columns using common aliases. Recommended column names:

| Column | Aliases Accepted |
|---|---|
| `Order ID` | order_id, order_number, id |
| `Date` | order_date, shipment_date, ship_date |
| `Item` | product, sku, item_name, description |
| `Quantity` | qty, units, count |
| `Status` | order_status, shipment_status, state |
| `Customer` | customer_name, client, buyer |
| `Region` | area, zone, city, country |
| `Revenue` | price, total, value, cost |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Pandas** — data manipulation & cleaning
- **Streamlit** — interactive web dashboard
- **OpenPyXL** — Excel reading & styled exports
- **Matplotlib** — charts
- **Pytest** — unit testing

---

## ☁️ Deploy Online (Free)

### Streamlit Community Cloud
1. Push to a public GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` as entry point → Deploy

---

## 💼 Resume / Portfolio Description

> **Excel Automation Tool — Logistics & Supply Chain** | Python, Pandas, Streamlit, OpenPyXL
>
> Built a full-stack data automation web app that ingests raw logistics Excel files, performs automated data quality cleaning (deduplication, null handling, format standardisation), and renders an interactive KPI dashboard with status breakdowns, top-item analysis, and regional revenue charts. Implemented modular architecture (src/ package), unit-tested core logic with Pytest, and exported styled multi-sheet Excel reports using OpenPyXL.

---

## 📄 License

MIT
