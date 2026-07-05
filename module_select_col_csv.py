import argparse
import csv

'''
Selects some columns from csv file and create some new csv with only selected ones.
Columns are called by name, not their position, so the former csv needs a header
Works with:
python module_select_col_csv.py .\input.csv .\output.csv name_col1 name_col2 ... name_colN
'''

def copy_selected_columns(input_csv, output_csv, columns):
    with open(input_csv, "r", newline="", encoding="utf-8") as infile, open(
        output_csv, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.DictReader(infile)
        

        if not reader.fieldnames:
            raise ValueError("The input CSV does not contain a header row.")

        missing = [col for col in columns if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        writer = csv.DictWriter(outfile, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            writer.writerow({col: row.get(col, "") for col in columns})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy selected columns from one CSV file into a new CSV file."
    )
    parser.add_argument("input_csv", help="Path to the source CSV file")
    parser.add_argument("output_csv", help="Path to the new CSV file to create")
    parser.add_argument(
        "columns",
        nargs="+",
        help="One or more column names to copy (must match the header names)",
    )
    args = parser.parse_args()

    copy_selected_columns(args.input_csv, args.output_csv, args.columns)

