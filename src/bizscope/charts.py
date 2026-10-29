"""Build Plotly chart figures from prepared sales data."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from bizscope import metrics

# Shared colour palette — professional and colourblind-friendly
_PALETTE = px.colors.qualitative.Set2


def revenue_over_time(df: pd.DataFrame) -> go.Figure:
    """Line chart of daily revenue."""
    data = metrics.revenue_by_date(df)
    fig = px.line(
        data,
        x="order_date",
        y="revenue",
        labels={"order_date": "Date", "revenue": "Revenue ($)"},
        title="Revenue Over Time",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_traces(mode="lines+markers")
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def revenue_by_product_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of revenue per product."""
    data = metrics.revenue_by_product(df)
    fig = px.bar(
        data,
        x="revenue",
        y="product",
        orientation="h",
        labels={"revenue": "Revenue ($)", "product": "Product"},
        title="Revenue by Product",
        color="product",
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def revenue_by_category_chart(df: pd.DataFrame) -> go.Figure:
    """Pie / donut chart of revenue per category."""
    data = metrics.revenue_by_category(df)
    fig = px.pie(
        data,
        values="revenue",
        names="category",
        title="Revenue by Category",
        hole=0.4,
        color_discrete_sequence=_PALETTE,
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
