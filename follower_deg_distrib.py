import csv
import pandas as pd
from matplotlib import pyplot as plt

filename = "filtered_agents_col134.csv"  # Specify the CSV file name
column_name = ["follower_count", "following_count"]    #select columns to plot 



try:
    ds=pd.read_csv(filename)
    
    for column in column_name:
        data = ds[column].dropna()
        bins = range(int(data.min()), int(data.max()) + 2, 1)

        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=bins, edgecolor="black", color="skyblue", alpha=0.7)

        plt.xlim(0, max(data) + 10)
        plt.title(f"Distribution Histogram of {column} (1-unit bins)", fontsize=14, pad=15)
        plt.xlabel(column, fontsize=12)
        plt.ylabel("Frequency (Count)", fontsize=12)
        plt.grid(axis="y", alpha=0.75, linestyle="--")

        # 4. Display the plot
        plt.tight_layout()
        #plt.show()
        plt.savefig(f"{column}_hist.png", dpi=300, bbox_inches="tight")
        plt.close()
        
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found. Check the path.")
except KeyError:
    print(f"Error: Column '{column_name}' not found. Check your CSV header names.")