"""Calculate sales metrics from a validated DataFrame.

Every function expects a DataFrame that has already passed through
``validation.prepare`` (i.e. it has proper dtypes and a *revenue* column).
"""

from __future__ import annotations

import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    """Sum of all row-level revenue."""
    if df.empty:
        return 0.0
    return float(df["revenue"].sum())


def total_orders(df: pd.DataFrame) -> int:
    """Count of unique order IDs."""
    if df.empty:
        return 0
    return int(df["order_id"].nunique())


def total_units_sold(df: pd.DataFrame) -> int:
    """Sum of all quantities."""
    if df.empty:
        return 0
    return int(df["quantity"].sum())


def average_order_value(df: pd.DataFrame) -> float:
    """Total revenue / unique order count. Returns 0.0 when there are no orders."""
    orders = total_orders(df)
    if orders == 0:
        return 0.0
    return total_revenue(df) / orders


def revenue_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by *order_date*, sorted chronologically.

    Returns a DataFrame with columns ``order_date`` and ``revenue``.
    """
    if df.empty:
        return pd.DataFrame(columns=["order_date", "revenue"])
    return (
        df.groupby("order_date", as_index=False)["revenue"]
        .sum()
        .sort_values("order_date")
        .reset_index(drop=True)
    )


def revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by *product*, sorted descending.

    Returns a DataFrame with columns ``product`` and ``revenue``.
    """
    if df.empty:
        return pd.DataFrame(columns=["product", "revenue"])
    return (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by *category*, sorted descending.

    Returns a DataFrame with columns ``category`` and ``revenue``.
    """
    if df.empty:
        return pd.DataFrame(columns=["category", "revenue"])
    return (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )


def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by *region*, sorted descending.

    Returns a DataFrame with columns ``region`` and ``revenue``.
    """
    if df.empty:
        return pd.DataFrame(columns=["region", "revenue"])
    return (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
