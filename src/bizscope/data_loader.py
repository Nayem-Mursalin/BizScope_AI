"""Load CSV data from file uploads or file paths."""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

import pandas as pd


def load_csv(source: str | Path | BytesIO) -> pd.DataFrame:
    """Read a CSV into a DataFrame.

    Args:
        source: A file path (str/Path) or an in-memory bytes buffer
                (e.g. from Streamlit's file_uploader).

    Returns:
        Raw DataFrame — not yet validated.

    Raises:
        ValueError: If the file cannot be parsed as CSV.
    """
    try:
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.is_file():
                raise ValueError(f"File not found: {path}")
            return pd.read_csv(path)
        # BytesIO / UploadedFile
        return pd.read_csv(source)
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded file is empty.")
    except pd.errors.ParserError as exc:
        raise ValueError(f"Could not parse CSV: {exc}")
