#!/usr/bin/env python

from common import *
from ClassFrequencyEncoder import *


@click.command()
@click.option(
    "-if",
    "--input_file",
    required=True,
    type=click.Path(exists=True),
    help="Input CSV file.",
)
@click.option(
    "-g",
    "--groups",
    type=COLUMN_GROUPING,
    required=True,
    help=(
        "JSON list of column groups. Example: " '\'[["country"], ["country", "city"]]\''
    ),
)
@click.option(
    "-of",
    "--output_file",
    required=False,
    type=click.Path(exists=False),
    default=f"output_file_{get_current_datetime()}.csv",
    help="Output CSV file.",
    show_default=True,
)
@click.option(
    "-r",
    "--raw_counts",
    required=False,
    is_flag=True,
    default=True,
    help="Store raw occurrence counts instead of normalized frequencies.",
    show_default=True,
)
def execute(input_file, groups, output_file, raw_counts):
    """

    :param input_file:
    :param groups:
    :param output_file:
    :param raw_counts:
    :return:
    """
    click.secho("Initializing...", fg="green")

    config = FrequencyEncodingConfig(column_groups=groups, normalize=raw_counts)

    pipeline = FrequencyEncodingPipeline(
        reader=CsvReader(), encoder=FrequencyEncoder(config=config), writer=CsvWriter()
    )

    pipeline.run(input_path=input_file, output_path=output_file)

    click.secho("\n✨ Execution Successful!", fg="green", bold=True)
    click.secho(f"\n✅ Created: {output_file}", fg="green")


if __name__ == "__main__":
    execute()
