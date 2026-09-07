import pandas as pd

# 1. Stream or load the datasets efficiently
# If files are multi-gigabyte, you can use usecols to only load necessary columns
post_ds = pd.read_csv("sort_posts_col028.csv", usecols=["id", "agent_name"])
comm_ds = pd.read_csv("sort_comments_col0134.csv")              #, usecols=["id", "post_id", 'agent_name', 'parent_id'])

# 2. Rename columns to make the merge and comparison clean
# We rename df2's name to match df1, and give scores unique names
comm_ds = comm_ds.rename(columns={"id": "comm_id", 'agent_name': 'comm_auth'})
post_ds = post_ds.rename(columns={"id": "post_id", 'agent_name': 'post_auth'})  #so that post_id appears in both comm_ds and post_ds

# 3. Vectorized Merge (Inner Join)
# This instantly matches rows where agent_name exists in both files at C-speed
matched_df = pd.merge(post_ds, comm_ds, on="post_id", how="inner")

'''
# 4. Create a vectorized comparison status column
# This eliminates row-by-row if/else checking
matched_df["correspondence"] = "Mismatch"               #add a column for flag
matched_df.loc[
    matched_df["score_file1"] == matched_df["score_file2"], "correspondence"
] = "Match"
'''

# 5. Optimize the writing operation
# Writing the entire block at once is drastically faster than appending row-by-row
output_file = "correspondence_report.csv"
matched_df.to_csv(output_file, index=False)

print(
    f"Successfully processed {len(matched_df)} correspondences and saved to {output_file}!"
)