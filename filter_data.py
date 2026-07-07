import csv

filename = "posts_col028.csv"  # Specify the CSV file name
column_name = ["follower_count", "following_count"]    #select columns to plot 

with open(filename, 'r', newline='') as inp:
    reader = csv.reader(inp)
    rows = [row for row in reader if (row[2] > "0")] # Remove rows where comments count are 0

with open(f'filtered_{filename}', 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerows(rows)