import argparse
import os
import pandas as pd


def main():
    # 1. Set up terminal argument parsing
    parser = argparse.ArgumentParser(
        description="Print CSV headers and sort by a specific column."
    )
    parser.add_file = parser.add_argument(
        "filename", type=str, help="The path to the input CSV file."
    )
    args = parser.parse_args()

    # 2. Check if file exists
    if not os.path.exists(args.filename):
        print(f"Error: The file '{args.filename}' does not exist.")
        return

    # 3. Read and print the headers safely (loading only the first row)
    try:
        preview_df = pd.read_csv(args.filename, nrows=0)
        headers = list(preview_df.columns)
        print("\n--- CSV HEADERS ---")
        for i, header in enumerate(headers, 1):
            print(f"{i}. {header}")
        print("-------------------\n")
    except Exception as e:
        print(f"Error reading file headers: {e}")
        return

    # 4. Get the column name to sort by from the user
    target_column = input(
        "Enter the exact name of the column you want to sort by: "
    ).strip()

    if target_column not in headers:
        print(
            f"Error: '{target_column}' is not a valid column in this CSV file."
        )
        return

    # 5. Get the sorting order preference
    order_input = (
        input("Sort in descending order? (y/N): ").strip().lower()
    )
    ascending_order = order_input != "y"

    # 6. Load the full dataset, sort it, and save it
    print(f"\nLoading and sorting dataset by '{target_column}'...")
    try:
        df = pd.read_csv(args.filename)
        df_sorted = df.sort_values(by=target_column, ascending=ascending_order)

        # Generate output filename (e.g., data_sorted.csv)
        base, ext = os.path.splitext(args.filename)
        output_filename = f"{base}{ext}"

        df_sorted.to_csv(output_filename, index=False)
        print(f"Success! Sorted file saved as: {output_filename}\n")

    except Exception as e:
        print(f"An error occurred during sorting: {e}")


if __name__ == "__main__":
    main()