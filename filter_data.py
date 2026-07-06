import csv
import pandas as pd

filename = "agents_col134.csv"  # Specify the CSV file name
column_name = ["follower_count", "following_count"]    #select columns to plot 

with open(filename, 'r', newline='') as inp:
    reader = csv.reader(inp)
    rows = [row for row in reader if ((row[1] != "0") or (row[2] != "0"))] # Remove rows where both followr and following counters are zero

with open(f'filtered_{filename}', 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerows(rows)