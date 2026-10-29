"""Tests for bizscope.validation."""

import pandas as pd
import pytest

from bizscope.validation import validate, prepare


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _valid_row(**overrides) -> dict:
    """Return a single valid row dict, with optional field overrides."""
    row = {
        "order_id": "ORD-001",
        "order_date": "2024-01-15",
        "product": "Widget",
        "category": "Gadgets",
        "quantity": 3,
        "unit_price": 10.00,
        "region": "North",
    }
    row.update(overrides)
    return row


def _df_from_rows(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


# ---------------------------------------------------------------------------
# Valid data
# ---------------------------------------------------------------------------

class TestValidData:
    def test_valid_single_row(self):
        df = _df_from_rows(_valid_row())
        assert validate(df) == []

    def test_valid_multiple_rows(self):
        df = _df_from_rows(
            _valid_row(order_id="ORD-001", product="A"),
            _valid_row(order_id="ORD-001", product="B"),
            _valid_row(order_id="ORD-002", product="A"),
        )
        assert validate(df) == []


# ---------------------------------------------------------------------------
# Missing columns
# ---------------------------------------------------------------------------

class TestMissingColumns:
    def test_missing_one_column(self):
        row = _valid_row()
        del row["region"]
        errors = validate(pd.DataFrame([row]))
        assert len(errors) == 1
        assert "region" in errors[0]

    def test_missing_multiple_columns(self):
        row = _valid_row()
        del row["region"]
        del row["category"]
        errors = validate(pd.DataFrame([row]))
        assert len(errors) == 1
        assert "region" in errors[0] and "category" in errors[0]


# ---------------------------------------------------------------------------
# Empty / blank values
# ---------------------------------------------------------------------------

class TestEmptyValues:
    def test_empty_order_id(self):
        df = _df_from_rows(_valid_row(order_id=""))
        errors = validate(df)
        assert any("order_id" in e for e in errors)

    def test_none_product(self):
        df = _df_from_rows(_valid_row(product=None))
        errors = validate(df)
        assert any("product" in e for e in errors)

    def test_empty_dataset(self):
        df = pd.DataFrame(columns=[
            "order_id", "order_date", "product", "category",
            "quantity", "unit_price", "region",
        ])
        errors = validate(df)
        assert any("empty" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# Date validation
# ---------------------------------------------------------------------------

class TestDateValidation:
    def test_invalid_date(self):
        df = _df_from_rows(_valid_row(order_date="not-a-date"))
        errors = validate(df)
        assert any("date" in e.lower() for e in errors)

    def test_valid_iso_date(self):
        df = _df_from_rows(_valid_row(order_date="2024-12-31"))
        assert validate(df) == []


# ---------------------------------------------------------------------------
# Numeric validation
# ---------------------------------------------------------------------------

class TestNumericValidation:
    def test_non_numeric_quantity(self):
        df = _df_from_rows(_valid_row(quantity="abc"))
        errors = validate(df)
        assert any("quantity" in e for e in errors)

    def test_non_numeric_unit_price(self):
        df = _df_from_rows(_valid_row(unit_price="xyz"))
        errors = validate(df)
        assert any("unit_price" in e for e in errors)

    def test_zero_quantity(self):
        df = _df_from_rows(_valid_row(quantity=0))
        errors = validate(df)
        assert any("zero or negative" in e.lower() for e in errors)

    def test_negative_quantity(self):
        df = _df_from_rows(_valid_row(quantity=-2))
        errors = validate(df)
        assert any("zero or negative" in e.lower() for e in errors)

    def test_negative_unit_price(self):
        df = _df_from_rows(_valid_row(unit_price=-5.0))
        errors = validate(df)
        assert any("negative" in e.lower() for e in errors)

    def test_zero_unit_price_is_ok(self):
        """A free item (price=0) is acceptable."""
        df = _df_from_rows(_valid_row(unit_price=0.0))
        assert validate(df) == []


# ---------------------------------------------------------------------------
# prepare()
# ---------------------------------------------------------------------------

class TestPrepare:
    def test_revenue_computed(self):
        df = _df_from_rows(
            _valid_row(quantity=4, unit_price=10.00),
        )
        result = prepare(df)
        assert "revenue" in result.columns
        assert result["revenue"].iloc[0] == pytest.approx(40.0)

    def test_date_dtype(self):
        result = prepare(_df_from_rows(_valid_row()))
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
