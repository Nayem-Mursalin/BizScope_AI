# BizScope AI

**AI-ready Business Intelligence & Decision Support Platform — Day 1 MVP**

BizScope AI is a Streamlit-based dashboard that ingests sales CSV data, validates it, calculates key business metrics, displays interactive charts, and generates deterministic business insights — all without requiring API keys, databases, or internet access.

---

## Prerequisites

- **Python 3.10+**
- **pip** (bundled with Python)

## Setup

```bash
# 1. Clone or navigate to the project directory
cd BizScope-AI

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

# 3. Install the project and its dependencies
pip install -e ".[dev]"
```

## Running the App

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. No API keys or internet access required.

### Loading Data

- **Upload your own CSV** via the sidebar file uploader.
- **Use sample data**: click **Load sample dataset** in the sidebar to use the bundled synthetic data (`data/sample_sales.csv`).

## Running Tests

```bash
pytest
```

All tests run against small in-memory fixtures — no files, network, or Streamlit internals required.

## Expected CSV Columns

| Column       | Type              | Constraint        |
|------------- |------------------ |------------------ |
| `order_id`   | string            | non-empty         |
| `order_date` | date (YYYY-MM-DD) | valid date        |
| `product`    | string            | non-empty         |
| `category`   | string            | non-empty         |
| `quantity`    | integer           | positive (> 0)    |
| `unit_price` | numeric           | non-negative (≥ 0)|
| `region`     | string            | non-empty         |

Revenue is calculated as `quantity × unit_price`. A `total_sales` column is **not** required.

Multiple rows may share the same `order_id` (multi-product orders). Unique order count and average order value are computed from distinct `order_id` values.

## Sample Data

The file `data/sample_sales.csv` contains **33 rows** of synthetic sales data across:

- 25 unique orders (some with multiple product lines)
- 5 products: Wireless Mouse, USB-C Hub, Desk Lamp, Mechanical Keyboard, Notebook Set, Monitor Stand
- 3 categories: Electronics, Home Office, Stationery
- 4 regions: North, South, East, West
- Date range: January – March 2024

**This data is entirely synthetic and for demonstration purposes only.**

## Project Structure

```
BizScope-AI/
├── app.py                  # Streamlit dashboard
├── pyproject.toml          # Project metadata & dependencies
├── README.md
├── .gitignore
├── data/
│   └── sample_sales.csv    # Synthetic sample data
├── src/
│   └── bizscope/
│       ├── __init__.py
│       ├── data_loader.py  # CSV loading
│       ├── validation.py   # Schema & value validation
│       ├── metrics.py      # Business metric calculations
│       ├── insights.py     # Deterministic insight generation
│       └── charts.py       # Plotly chart factories
└── tests/
    ├── test_validation.py
    ├── test_metrics.py
    └── test_insights.py
```

## License

This project is for educational and demonstration purposes.
