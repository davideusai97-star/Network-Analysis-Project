import csv
import argparse
import pandas as pd


def add_column_to_csv(input_filename, output_filename, new_column_name, new_column_value):
    """
    Adds a new column to an existing CSV file.

    Parameters:
    - input_filename: str, path to the input CSV file.
    - output_filename: str, path to the output CSV file.
    - new_column_name: str, name of the new column to add.
    - new_column_data: list or array-like, data for the new column (must match the number of rows in the input CSV).
    """

    new_column_value_array = pd.array([new_column_value] * len(pd.read_csv(input_filename)))  # Create an array of the new column value

    with open(input_filename, "r", newline="") as infile, open(output_filename, "w", newline="") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 1. Handle the header row
        header = next(reader)
        header.append(new_column_name)
        writer.writerow(header)

        # 2. Loop through rows and zip them with your new data
        for row, new_value in zip(reader, new_column_value_array):
            row.append(new_value)
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds a new column of value X to an existing CSV file."
    )
    parser.add_argument("input_csv", help="Path to the source CSV file")
    parser.add_argument("output_csv", help="Path to the new CSV file to create")
    parser.add_argument("new_column_name", help="Name of the new column to add")
    parser.add_argument(
        "new_column_value",
        help="Data for the new column (comma-separated values, must match the number of rows in the input CSV)",
    )
    args = parser.parse_args()

    add_column_to_csv(args.input_csv, args.output_csv, args.new_column_name, args.new_column_value)