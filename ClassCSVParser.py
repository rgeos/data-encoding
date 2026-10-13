#!/usr/bin/env python

from pathlib import Path
import pandas as pd


class CsvReader:
    """Reads CSV files into pandas DataFrames."""

    @staticmethod
    def read(input_path: str | Path) -> pd.DataFrame:
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input CSV file does not exist: {input_path}")

        if not input_path.is_file():
            raise ValueError(f"Input path is not a file: {input_path}")

        return pd.read_csv(input_path)


class CsvWriter:
    """Writes pandas DataFrames to CSV files."""

    @staticmethod
    def write(
        dataframe: pd.DataFrame,
        output_path: str | Path,
    ) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        dataframe.to_csv(output_path, index=False)
