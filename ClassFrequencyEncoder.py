#!/usr/bin/env python

from dataclasses import dataclass
from collections import Counter
from pathlib import Path
from ClassCSVParser import CsvReader, CsvWriter
import pandas as pd
from typing import Sequence


@dataclass(frozen=True)
class FrequencyEncodingConfig:
    """
    Configuration for frequency encoding.

    column_groups:
        Each inner list represents one frequency-encoding group.

        Examples:
            [["country"], ["country", "city"]]

    normalize:
        If True, output relative frequencies between 0 and 1.
        If False, output raw occurrence counts.
    """

    column_groups: Sequence[Sequence[str]]
    normalize: bool = True

    def validate(self) -> None:
        if not self.column_groups:
            raise ValueError("At least one column group must be provided.")

        for group in self.column_groups:
            if not group:
                raise ValueError("Column groups cannot be empty.")

            if len(group) != len(set(group)):
                raise ValueError(f"Duplicate column names found in group: {group}")


class FrequencyEncoder:
    """Adds frequency-encoded columns to a DataFrame."""

    MISSING_VALUE_MARKER = "__MISSING_VALUE__"

    def __init__(self, config: FrequencyEncodingConfig):
        self.config = config
        self.config.validate()

    def encode(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Return a copy of the DataFrame with frequency-encoded columns added.
        """

        encoded_dataframe = dataframe.copy()

        self._validate_columns(encoded_dataframe)

        for column_group in self.config.column_groups:
            self._encode_group(
                dataframe=encoded_dataframe,
                column_group=list(column_group),
            )

        return encoded_dataframe

    def _validate_columns(self, dataframe: pd.DataFrame) -> None:
        missing_columns = {
            column
            for group in self.config.column_groups
            for column in group
            if column not in dataframe.columns
        }

        if missing_columns:
            raise ValueError(
                "The following columns were not found in the input CSV: "
                f"{sorted(missing_columns)}"
            )

    def _encode_group(
        self,
        dataframe: pd.DataFrame,
        column_group: list[str],
    ) -> None:
        output_column = self._get_output_column_name(column_group)

        if output_column in dataframe.columns:
            raise ValueError(f"Output column already exists: {output_column}")

        row_keys = self._create_row_keys(
            dataframe=dataframe,
            column_group=column_group,
        )

        frequencies = Counter(row_keys)

        encoded_values = [frequencies[row_key] for row_key in row_keys]

        if self.config.normalize:
            row_count = len(dataframe)

            if row_count == 0:
                encoded_values = []
            else:
                encoded_values = [value / row_count for value in encoded_values]

        dataframe[output_column] = encoded_values

    def _create_row_keys(
        self,
        dataframe: pd.DataFrame,
        column_group: list[str],
    ) -> list[tuple]:
        """
        Convert every row into a hashable tuple.

        For one column:

            ["USA"] -> ("USA",)

        For multiple columns:

            ["USA", "New York"] -> ("USA", "New York")
        """

        selected_columns = dataframe[column_group]

        selected_columns = selected_columns.astype(object).where(
            selected_columns.notna(),
            self.MISSING_VALUE_MARKER,
        )

        return list(
            selected_columns.itertuples(
                index=False,
                name=None,
            )
        )

    @staticmethod
    def _get_output_column_name(
        column_group: list[str],
    ) -> str:
        return "freq_" + "_".join(column_group)


class FrequencyEncodingPipeline:
    """Coordinates CSV reading, encoding, and writing."""

    def __init__(
        self,
        reader: CsvReader,
        encoder: FrequencyEncoder,
        writer: CsvWriter,
    ):
        self.reader = reader
        self.encoder = encoder
        self.writer = writer

    def run(
        self,
        input_path: str | Path,
        output_path: str | Path,
    ) -> None:
        dataframe = self.reader.read(input_path)
        encoded_dataframe = self.encoder.encode(dataframe)
        self.writer.write(encoded_dataframe, output_path)
