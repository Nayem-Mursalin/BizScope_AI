"""Validate a sales DataFrame against the required data contract."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "unit_price",
    "region",
]


def validate(df: pd.DataFrame) -> list[str]:
    """Check *df* against the sales data contract.

    Returns a list of human-readable error strings.
    An empty list means the data is valid.
    """
    errors: list[str] = []

    if df.empty:
        errors.append("The dataset is empty — no rows found.")
        return errors

    # --- required columns ---
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Missing required column(s): {', '.join(missing)}")
        return errors  # remaining checks depend on columns existing

    # --- null / empty string checks for text columns ---
    text_cols = ["order_id", "product", "category", "region"]
    for col in text_cols:
        n_empty = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
        if n_empty > 0:
            errors.append(f"Column '{col}' has {n_empty} empty or missing value(s).")

    # --- date parsing ---
    try:
        pd.to_datetime(df["order_date"], format="mixed", dayfirst=False)
    except (ValueError, TypeError):
        errors.append("Column 'order_date' contains values that cannot be parsed as dates.")

    # Check for NaT after parsing (individual bad dates)
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    n_bad_dates = parsed_dates.isna().sum()
    if n_bad_dates > 0:
        errors.append(
            f"Column 'order_date' has {n_bad_dates} value(s) that cannot be parsed as dates."
        )

    # --- numeric checks ---
    quantity_numeric = pd.to_numeric(df["quantity"], errors="coerce")
    n_bad_qty = quantity_numeric.isna().sum()
    if n_bad_qty > 0:
        errors.append(f"Column 'quantity' has {n_bad_qty} non-numeric value(s).")

    price_numeric = pd.to_numeric(df["unit_price"], errors="coerce")
    n_bad_price = price_numeric.isna().sum()
    if n_bad_price > 0:
        errors.append(f"Column 'unit_price' has {n_bad_price} non-numeric value(s).")

    # --- value constraints ---
    if n_bad_qty == 0:
        # quantity must be a positive integer
        non_int = (quantity_numeric != quantity_numeric.astype(int)).sum()
        if non_int > 0:
            errors.append(f"Column 'quantity' has {non_int} non-integer value(s).")
        n_non_positive = (quantity_numeric <= 0).sum()
        if n_non_positive > 0:
            errors.append(
                f"Column 'quantity' has {n_non_positive} value(s) that are zero or negative."
            )

    if n_bad_price == 0:
        n_negative = (price_numeric < 0).sum()
        if n_negative > 0:
            errors.append(f"Column 'unit_price' has {n_negative} negative value(s).")

    return errors


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy with proper types and a computed *revenue* column.

    Call this only after :func:`validate` returns no errors.
    """
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df
