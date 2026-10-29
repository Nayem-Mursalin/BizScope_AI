"""Tests for bizscope.metrics."""

import pandas as pd
import pytest

from bizscope.metrics import (
    total_revenue,
    total_orders,
    total_units_sold,
    average_order_value,
    revenue_by_date,
    revenue_by_product,
    revenue_by_category,
    revenue_by_region,
)
from bizscope.validation import prepare


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _prepared_df(rows: list[dict]) -> pd.DataFrame:
    """Build a prepared DataFrame from raw row dicts."""
    raw = pd.DataFrame(rows)
    return prepare(raw)


ROWS = [
    # ORD-001: 2 items → revenue = 2*10 + 1*20 = 40
    {"order_id": "ORD-001", "order_date": "2024-01-10", "product": "Alpha", "category": "Cat-A", "quantity": 2, "unit_price": 10.0, "region": "North"},
    {"order_id": "ORD-001", "order_date": "2024-01-10", "product": "Beta",  "category": "Cat-B", "quantity": 1, "unit_price": 20.0, "region": "North"},
    # ORD-002: 1 item  → revenue = 3*10 = 30
    {"order_id": "ORD-002", "order_date": "2024-01-12", "product": "Alpha", "category": "Cat-A", "quantity": 3, "unit_price": 10.0, "region": "South"},
    # ORD-003: 1 item  → revenue = 5*20 = 100
    {"order_id": "ORD-003", "order_date": "2024-01-12", "product": "Beta",  "category": "Cat-B", "quantity": 5, "unit_price": 20.0, "region": "South"},
]

TOTAL_REV = 20.0 + 20.0 + 30.0 + 100.0  # = 170.0


@pytest.fixture
def df():
    return _prepared_df(ROWS)


@pytest.fixture
def empty_df():
    cols = ["order_id", "order_date", "product", "category", "quantity", "unit_price", "region", "revenue"]
    return pd.DataFrame(columns=cols)


# ---------------------------------------------------------------------------
# Scalar metrics
# ---------------------------------------------------------------------------

class TestScalarMetrics:
    def test_total_revenue(self, df):
        assert total_revenue(df) == pytest.approx(TOTAL_REV)

    def test_total_orders(self, df):
        assert total_orders(df) == 3  # ORD-001, ORD-002, ORD-003

    def test_total_units_sold(self, df):
        assert total_units_sold(df) == 2 + 1 + 3 + 5  # 11

    def test_average_order_value(self, df):
        expected = TOTAL_REV / 3
        assert average_order_value(df) == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Empty dataset
# ---------------------------------------------------------------------------

class TestEmptyDataset:
    def test_revenue_zero(self, empty_df):
        assert total_revenue(empty_df) == 0.0

    def test_orders_zero(self, empty_df):
        assert total_orders(empty_df) == 0

    def test_units_zero(self, empty_df):
        assert total_units_sold(empty_df) == 0

    def test_aov_zero(self, empty_df):
        assert average_order_value(empty_df) == 0.0

    def test_revenue_by_date_empty(self, empty_df):
        result = revenue_by_date(empty_df)
        assert result.empty

    def test_revenue_by_product_empty(self, empty_df):
        assert revenue_by_product(empty_df).empty

    def test_revenue_by_category_empty(self, empty_df):
        assert revenue_by_category(empty_df).empty

    def test_revenue_by_region_empty(self, empty_df):
        assert revenue_by_region(empty_df).empty


# ---------------------------------------------------------------------------
# Grouped metrics
# ---------------------------------------------------------------------------

class TestGroupedMetrics:
    def test_revenue_by_date(self, df):
        result = revenue_by_date(df)
        # Two dates: 2024-01-10 and 2024-01-12
        assert len(result) == 2
        assert result["revenue"].sum() == pytest.approx(TOTAL_REV)

    def test_revenue_by_product(self, df):
        result = revenue_by_product(df)
        # Alpha: 2*10 + 3*10 = 50, Beta: 1*20 + 5*20 = 120
        alpha = result[result["product"] == "Alpha"]["revenue"].iloc[0]
        beta = result[result["product"] == "Beta"]["revenue"].iloc[0]
        assert alpha == pytest.approx(50.0)
        assert beta == pytest.approx(120.0)

    def test_revenue_by_category(self, df):
        result = revenue_by_category(df)
        assert len(result) == 2

    def test_revenue_by_region(self, df):
        result = revenue_by_region(df)
        north = result[result["region"] == "North"]["revenue"].iloc[0]
        south = result[result["region"] == "South"]["revenue"].iloc[0]
        assert north == pytest.approx(40.0)
        assert south == pytest.approx(130.0)
