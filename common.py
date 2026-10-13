#!/usr/bin/env python

import json
import click
import datetime


def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H_%M_%S")


class ColumnGroups(click.ParamType[str]):
    name = "column grouping"

    def convert(self, value: str, param, ctx) -> list[list[str]]:
        """
        Parse column groups supplied as JSON.
        Example input:

            [["country"], ["country", "city"]]
        """

        try:
            column_groups = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Column groups must be valid JSON. Example: "
                '\'[["country"], ["country", "city"]]\''
            ) from error

        if not isinstance(column_groups, list):
            raise ValueError("Column groups must be a list of lists.")

        if any(
            not isinstance(group, list)
            or any(not isinstance(column, str) for column in group)
            for group in column_groups
        ):
            raise ValueError(
                "Column groups must contain only lists of column-name strings."
            )

        return column_groups


# used as custom type for click
COLUMN_GROUPS = ColumnGroups()
