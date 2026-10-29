"""Tests for bizscope.insights."""

import pandas as pd
import pytest

from bizscope.insights import generate_insights
from bizscope.validation import prepare


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _prepared_df(rows: list[dict]) -> pd.DataFrame:
    return prepare(pd.DataFrame(rows))


ROWS = [
    {"order_id": "ORD-001", "order_date": "2024-01-10", "product": "Alpha", "category": "Cat-A", "quantity": 2, "unit_price": 10.0, "region": "North"},
    {"order_id": "ORD-001", "order_date": "2024-01-10", "product": "Beta",  "category": "Cat-B", "quantity": 1, "unit_price": 50.0, "region": "North"},
    {"order_id": "ORD-002", "order_date": "2024-01-12", "product": "Alpha", "category": "Cat-A", "quantity": 3, "unit_price": 10.0, "region": "South"},
]
# Revenues: Alpha=2*10+3*10=50, Beta=1*50=50
# Cat-A=50, Cat-B=50  (tie — first one reported is fine)
# North=20+50=70, South=30
# Day 2024-01-10: 20+50=70, Day 2024-01-12: 30  → strongest = 2024-01-10
# AOV = 100 / 2 = 50


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestInsights:
    def test_returns_list_of_strings(self):
        df = _prepared_df(ROWS)
        result = generate_insights(df)
        assert isinstance(result, list)
        assert all(isinstance(s, str) for s in result)
        assert len(result) >= 3  # at least product, category, day

    def test_empty_dataset(self):
        cols = [
            "order_id", "order_date", "product", "category",
            "quantity", "unit_price", "region", "revenue",
        ]
        empty = pd.DataFrame(columns=cols)
        result = generate_insights(empty)
        assert any("no data" in s.lower() for s in result)

    def test_contains_top_product(self):
        df = _prepared_df(ROWS)
        result = generate_insights(df)
        # Either Alpha or Beta could be first since they tie at 50
        assert any("highest-revenue product" in s.lower() for s in result)

    def test_contains_top_category(self):
        df = _prepared_df(ROWS)
        result = generate_insights(df)
        assert any("highest-revenue category" in s.lower() for s in result)

    def test_contains_strongest_day(self):
        df = _prepared_df(ROWS)
        result = generate_insights(df)
        # Strongest day is 2024-01-10 with $70
        day_insights = [s for s in result if "strongest revenue day" in s.lower()]
        assert len(day_insights) == 1
        assert "2024-01-10" in day_insights[0]

    def test_contains_aov(self):
        df = _prepared_df(ROWS)
        result = generate_insights(df)
        assert any("average order value" in s.lower() for s in result)
        aov_insight = [s for s in result if "average order value" in s.lower()][0]
        assert "$50.00" in aov_insight
