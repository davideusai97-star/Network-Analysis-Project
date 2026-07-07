import argparse
import csv
import pandas as pd

'''
Selects some columns from csv file and create some new csv with only selected ones.
Columns are called by name, not their position, so the former csv needs a header
Works with:
python module_select_col_csv.py .\input.csv .\output.csv sorting name_col1 name_col2 ... name_colN
sorting can be (asc, desc, none)

POSTS/ARCHIVE:
'id', 'agent_id', 'agent_name', 'submolt', 'title', 'content', 'url', 'score', 'comment_count', 
'created_at', 'fetched_at', 'is_pinned', 'dump_date'

AGENTS/ARCHIVE:
'id', 'name', 'description', 'karma', 'follower_count', 'following_count', 'is_claimed',
'owner_x_handle', 'first_seen_at', 'last_seen_at', 'created_at', 'avatar_url', 'dump_date'

COMMENTS/ARCHIVE:
'id', 'post_id', 'agent_id', 'agent_name', 'parent_id', 'content', 'score', 'created_at',
'fetched_at', 'dump_date'

SUBMOLTS/ARCHIVE:
'name', 'display_name', 'description', 'subscriber_count', 'post_count', 'created_at',
'first_seen_at', 'avatar_url', 'banner_url', 'dump_date'
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
            raise ValueError(f"Missing columns: {','.join(missing)}")

        writer = csv.DictWriter(outfile, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            writer.writerow({col: row.get(col, "") for col in columns})

def sort_csv_by_agent_name(output_csv):
    #SORTING ALGORITHM FOR AGENT NAME
    df = pd.read_csv(output_csv)

    # 2. Sort the rows
    df_sorted = df.sort_values(by="agent_name", ascending=True)

    # 3. Save the sorted data back to a CSV
    # You can overwrite the original file, or save to a new one
    df_sorted.to_csv(output_csv, index=False)
    print("CSV file sorted successfully!")


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
    sort_csv_by_agent_name(args.output_csv)