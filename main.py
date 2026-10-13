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
    "-cg",
    "--column_groups",
    type=COLUMN_GROUPS,
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
    "-rc",
    "--raw_counts",
    required=False,
    is_flag=True,
    default=False,
    help="Store raw occurrence counts instead of normalized frequencies.",
    show_default=True,
)
@click.option(
    "-em",
    "--export_mapping",
    required=False,
    is_flag=True,
    default=False,
    help="Write the frequency-encoder mapping to a .mapping.json file.",
    show_default=True,
)
def execute(input_file, column_groups, output_file, raw_counts, export_mapping):
    """
    :param input_file:
    :param column_groups:
    :param output_file:
    :param raw_counts:
    :param export_mapping:
    :return:
    """
    click.secho("Initializing...\n", fg="green")

    config = FrequencyEncodingConfig(column_groups=column_groups, normalize=raw_counts)
    encoder = FrequencyEncoder(config=config)

    pipeline = FrequencyEncodingPipeline(
        reader=CsvReader(), encoder=encoder, writer=CsvWriter()
    )

    pipeline.run(input_path=input_file, output_path=output_file)

    click.secho("✨ Execution Successful!", fg="green", bold=True)
    click.secho(f"✅ Created data file: {output_file}", fg="green")

    if export_mapping:
        mapping_file = f"{Path(output_file)}.json"
        encoder.write_mapping(mapping_file)
        click.secho(f"✅ Created mapping file: {mapping_file}", fg="green")


if __name__ == "__main__":
    execute()
