import pandas as pd
import numpy as np

'''
We use a self merging algorithm to light out the 'commutative couples', e.g. link due to auth1 comment
to auth2 post is the same as link due to auth2 comment to auth1 post.
We merge the list of links to itself if former_auth in list1 is 

'''

# 1. Load your dataset (assuming columns: 'former_auth', 'latter_auth')
df = pd.read_csv('interaction_list - Copia.csv')

# 2. Extract the two author columns into a numpy array for blistering fast sorting
# This prevents Python loop overhead entirely
authors_array = df[['former_author', 'comment_author']].to_numpy().astype(str)

# 3. Sort each row horizontally (alphabetically)
# If a row is ['Bob', 'Alice'], it instantly becomes ['Alice', 'Bob']
# If a row is ['Alice', 'Bob'], it stays ['Alice', 'Bob']
sorted_authors = np.sort(authors_array, axis=1)

# 4. Overwrite the columns with the normalized, sorted names
df['person_A'] = sorted_authors[:, 0]
df['person_B'] = sorted_authors[:, 1]

# 5. Group by the unique pairs and aggregate
# - We count the occurrences of each pair to get the 'molteplicity'
# - For 'comm_to_comm' and 'bond_strenght', we can sum them or take the max depending on your preference
final_df = df.groupby(['person_A', 'person_B']).agg(
    molteplicity=('person_A', 'size'),
).reset_index()

# 6. Rename the columns back to your preferred style if desired
final_df = final_df.rename(columns={'person_A': 'agent_A', 'person_B': 'agent_B'})

# 7. Save the clean, filtered data
final_df.to_csv('edge_list_collapsed.csv', index=False, encoding='utf-8')

print(f"Original rows: {len(df)}")
print(f"Collapsed rows: {len(final_df)}")