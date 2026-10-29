"""BizScope AI — Streamlit dashboard entry point."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from bizscope.data_loader import load_csv
from bizscope.validation import validate, prepare
from bizscope import metrics, insights, charts

SAMPLE_DATA_PATH = Path(__file__).parent / "data" / "sample_sales.csv"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BizScope AI",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS for a polished look
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* KPI cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 16px 20px;
        color: #f8fafc;
    }
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 0.85rem;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 700;
    }
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📊 BizScope AI")
st.caption(
    "AI-ready Business Intelligence & Decision Support Platform — Day 1 MVP"
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Sidebar — data source
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("📁 Data Source")
    uploaded_file = st.file_uploader(
        "Upload a sales CSV file",
        type=["csv"],
        help="The file must contain: order_id, order_date, product, category, quantity, unit_price, region",
    )
    use_sample = st.button(
        "Load sample dataset",
        help="Use the bundled synthetic sales data for a quick demo",
    )

# ---------------------------------------------------------------------------
# Determine data source
# ---------------------------------------------------------------------------
df_raw = None

if uploaded_file is not None:
    try:
        df_raw = load_csv(uploaded_file)
    except ValueError as exc:
        st.error(f"⚠️ {exc}")

elif use_sample or st.session_state.get("_sample_loaded"):
    try:
        df_raw = load_csv(SAMPLE_DATA_PATH)
        st.session_state["_sample_loaded"] = True
    except ValueError as exc:
        st.error(f"⚠️ {exc}")

# ---------------------------------------------------------------------------
# No data yet — show onboarding
# ---------------------------------------------------------------------------
if df_raw is None:
    st.info(
        "👈 Upload a CSV file or click **Load sample dataset** in the sidebar to get started."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------
errors = validate(df_raw)
if errors:
    st.error("### Validation errors")
    for err in errors:
        st.warning(f"• {err}")
    st.stop()

df = prepare(df_raw)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
st.subheader("Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${metrics.total_revenue(df):,.2f}")
kpi2.metric("Total Orders", f"{metrics.total_orders(df):,}")
kpi3.metric("Units Sold", f"{metrics.total_units_sold(df):,}")
kpi4.metric("Avg Order Value", f"${metrics.average_order_value(df):,.2f}")

st.markdown("---")

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
st.subheader("Revenue Analytics")

st.plotly_chart(charts.revenue_over_time(df), use_container_width=True)

chart_left, chart_right = st.columns(2)
with chart_left:
    st.plotly_chart(charts.revenue_by_product_chart(df), use_container_width=True)
with chart_right:
    st.plotly_chart(charts.revenue_by_category_chart(df), use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# Deterministic insights
# ---------------------------------------------------------------------------
st.subheader("📌 Business Insights")
st.caption("These insights are derived directly from your data — no AI predictions.")

for text in insights.generate_insights(df):
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)
