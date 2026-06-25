"""
Excel Automation Tool — Logistics & Supply Chain
Streamlit dashboard entry point.
"""
import io
import logging
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Logistics Excel Automation Tool",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import after page config
from src import (
    clean_data, compute_kpis, status_breakdown, top_items,
    revenue_by_region, orders_over_time,
    export_cleaned_excel, export_summary_excel, generate_sample,
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; }
.kpi-card { background: #f0f6ff; border-radius: 10px; padding: 1rem; margin: 0.3rem; }
.section-title { color: #1F4E79; font-size: 1.1rem; font-weight: 700; margin-top: 1.5rem; }
div[data-testid="column"] > div { gap: 0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/delivery.png", width=64)
    st.title("📦 Logistics Tool")
    st.markdown("---")

    st.subheader("1. Upload Data")
    uploaded = st.file_uploader(
        "Upload Excel file (.xlsx / .xls)", type=["xlsx", "xls"],
        help="Expects columns: Order ID, Date, Item, Quantity, Status, Customer, Region, Revenue"
    )

    st.markdown("---")
    if st.button("🎲 Load Demo Data", use_container_width=True):
        sample_bytes = generate_sample(n_rows=300)
        st.session_state["raw_bytes"] = sample_bytes
        st.session_state["filename"] = "demo_logistics_data.xlsx"
        st.success("Demo data loaded!")

    st.markdown("---")
    st.caption("**Supported columns** (auto-detected):\nOrder ID, Date, Item, Quantity, Status, Customer, Region, Revenue")

# ── Load data ─────────────────────────────────────────────────────────────────
raw_bytes = None
filename = "upload.xlsx"

if uploaded:
    raw_bytes = uploaded.read()
    filename = uploaded.name
elif "raw_bytes" in st.session_state:
    raw_bytes = st.session_state["raw_bytes"]
    filename = st.session_state.get("filename", "demo.xlsx")

if raw_bytes is None:
    st.markdown("""
    ## Welcome to the Logistics Excel Automation Tool 🚚

    **What this tool does:**
    - ✅ Uploads logistics / order Excel files
    - 🧹 Auto-cleans data (duplicates, nulls, format standardisation)
    - 📊 Computes KPIs, status breakdowns, top items & regional revenue
    - 📥 Exports cleaned Excel + multi-sheet summary report

    **To get started**, upload an Excel file in the sidebar or click **Load Demo Data**.
    """)
    st.stop()

# ── Parse & clean ─────────────────────────────────────────────────────────────
try:
    raw_df = pd.read_excel(io.BytesIO(raw_bytes))
except Exception as e:
    st.error(f"❌ Could not read file: {e}")
    st.stop()

with st.spinner("🧹 Cleaning data…"):
    try:
        clean_df, clean_report = clean_data(raw_df.copy())
    except Exception as e:
        st.error(f"❌ Error during cleaning: {e}")
        st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📦 Logistics Excel Automation Tool")
st.caption(f"File: **{filename}** · {clean_report['original_rows']} rows uploaded → **{clean_report['final_rows']} rows** after cleaning")

# ── Cleaning report banner ────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.info(f"🔁 **{clean_report['duplicates_removed']}** duplicate rows removed")
c2.info(f"🩹 **{clean_report['nulls_filled']}** null values filled")
c3.info(f"✅ **{clean_report['final_rows']}** clean rows ready")

st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
kpis = compute_kpis(clean_df)
st.markdown('<p class="section-title">📌 Key Performance Indicators</p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Orders", f"{kpis['total_orders']:,}")
k2.metric("Total Quantity", f"{kpis['total_quantity']:,}")
k3.metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
k4.metric("Unique Items", kpis["unique_items"])
k5.metric("Unique Customers", kpis["unique_customers"])

st.markdown("---")

# ── Charts row ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Analytics Dashboard</p>', unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1])

# Status pie chart
with col_left:
    st.subheader("Order Status Distribution")
    s_df = status_breakdown(clean_df)
    if not s_df.empty:
        fig, ax = plt.subplots(figsize=(5, 4))
        colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"]
        wedges, texts, autotexts = ax.pie(
            s_df["count"], labels=s_df["status"],
            autopct="%1.1f%%", colors=colors[:len(s_df)],
            startangle=140, pctdistance=0.82,
        )
        for t in autotexts:
            t.set_fontsize(9)
        ax.set_title("Status Breakdown", fontsize=11, fontweight="bold", pad=10)
        fig.patch.set_facecolor("#f8fafc")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No status column found.")

# Top items bar chart
with col_right:
    st.subheader("Top 10 Items by Quantity")
    t_df = top_items(clean_df, n=10)
    if not t_df.empty:
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.barh(t_df["item"][::-1], t_df["total_quantity"][::-1], color="#2E86AB", edgecolor="white")
        ax.set_xlabel("Total Quantity", fontsize=9)
        ax.tick_params(axis="y", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.patch.set_facecolor("#f8fafc")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No item/quantity columns found.")

st.markdown("---")

# ── Orders over time ──────────────────────────────────────────────────────────
ot_df = orders_over_time(clean_df)
if not ot_df.empty:
    st.subheader("📅 Orders Over Time")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.fill_between(ot_df["period"], ot_df["order_count"], alpha=0.25, color="#2E86AB")
    ax.plot(ot_df["period"], ot_df["order_count"], color="#1F4E79", linewidth=2, marker="o", markersize=4)
    ax.set_ylabel("Orders", fontsize=9)
    ax.set_xlabel("Month", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.patch.set_facecolor("#f8fafc")
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

# ── Revenue by region ─────────────────────────────────────────────────────────
rev_df = revenue_by_region(clean_df)
if not rev_df.empty:
    st.subheader("🌍 Revenue by Region")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(rev_df["region"], rev_df["total_revenue"], color="#A23B72", edgecolor="white")
    ax.set_ylabel("Revenue ($)", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.patch.set_facecolor("#f8fafc")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

# ── Data tables ───────────────────────────────────────────────────────────────
with st.expander("🔍 View Cleaned Data Table", expanded=False):
    st.dataframe(clean_df, use_container_width=True, height=350)

with st.expander("📋 Status Breakdown Table", expanded=False):
    s_df = status_breakdown(clean_df)
    if not s_df.empty:
        st.dataframe(s_df, use_container_width=True)

with st.expander("🏆 Top Items Table", expanded=False):
    t_df = top_items(clean_df, n=15)
    if not t_df.empty:
        st.dataframe(t_df, use_container_width=True)

# ── Exports ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-title">📥 Export Reports</p>', unsafe_allow_html=True)

exp1, exp2 = st.columns(2)

with exp1:
    cleaned_bytes = export_cleaned_excel(clean_df)
    st.download_button(
        label="⬇️ Download Cleaned Excel",
        data=cleaned_bytes,
        file_name="cleaned_logistics_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

with exp2:
    s_df = status_breakdown(clean_df)
    t_df = top_items(clean_df, n=10)
    summary_bytes = export_summary_excel(clean_df, kpis, s_df, t_df)
    st.download_button(
        label="⬇️ Download Summary Report (Excel)",
        data=summary_bytes,
        file_name="logistics_summary_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.markdown("---")
st.caption("Built with Python · Pandas · Streamlit · OpenPyXL | Logistics Excel Automation Tool")
