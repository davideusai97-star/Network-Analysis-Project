import argparse
import pandas as pd

'''
dataset di prova:
['./prova_dataset/prova.csv', './prova_dataset/prova4.csv']         './prova_dataset/prova_active_agents.csv'

dataset veri:
['sort_comments_col0134.csv', 'sort_posts_col028.csv']          'sort_active_agents_col01.csv'

'''


def reset_column(filename, column_name, reset_value, output_filename=None):
    ds = pd.read_csv(filename)

    if column_name not in ds.columns:
        raise ValueError(f"Column '{column_name}' not found in {filename}")

    ds[column_name] = reset_value
    output_path = output_filename or filename
    ds.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set every value in a CSV column to a default value."
    )
    parser.add_argument("input_csv", help="Path to the source CSV file")
    parser.add_argument("column_name", help="Name of the column to update")
    parser.add_argument("reset_value", help="Default value to write in the column")
    parser.add_argument("-o", "--output", dest="output_csv", help="Optional output CSV path")
    args = parser.parse_args()

    reset_column(args.input_csv, args.column_name, args.reset_value, args.output_csv)