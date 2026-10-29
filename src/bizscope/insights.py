"""Generate deterministic, data-backed business insights."""

from __future__ import annotations

import pandas as pd

from bizscope import metrics


def generate_insights(df: pd.DataFrame) -> list[str]:
    """Return a short list of factual insight strings derived from *df*.

    Every statement is directly supported by the data — no predictions,
    causal claims, or invented advice.
    """
    if df.empty:
        return ["No data available to generate insights."]

    insights: list[str] = []

    # --- top product by revenue ---
    by_product = metrics.revenue_by_product(df)
    if not by_product.empty:
        top = by_product.iloc[0]
        insights.append(
            f"Highest-revenue product: {top['product']} "
            f"(${top['revenue']:,.2f})."
        )

    # --- top category by revenue ---
    by_category = metrics.revenue_by_category(df)
    if not by_category.empty:
        top = by_category.iloc[0]
        insights.append(
            f"Highest-revenue category: {top['category']} "
            f"(${top['revenue']:,.2f})."
        )

    # --- top region by revenue ---
    by_region = metrics.revenue_by_region(df)
    if not by_region.empty:
        top = by_region.iloc[0]
        insights.append(
            f"Highest-revenue region: {top['region']} "
            f"(${top['revenue']:,.2f})."
        )

    # --- strongest revenue day ---
    by_date = metrics.revenue_by_date(df)
    if not by_date.empty:
        best_day = by_date.loc[by_date["revenue"].idxmax()]
        date_str = pd.Timestamp(best_day["order_date"]).strftime("%Y-%m-%d")
        insights.append(
            f"Strongest revenue day: {date_str} "
            f"(${best_day['revenue']:,.2f})."
        )

    # --- average order value context ---
    aov = metrics.average_order_value(df)
    insights.append(f"Average order value: ${aov:,.2f}.")

    return insights
