'''
In order to create the list of edges, we must link comments authors to posts authors and also
comments author to previuous comments authors: we read the matched dictionary and use a flag
to recognize comments to comments. If that is the case, we need to carefully menage the situation.
Since the list of matching post and comments is long, we need to vectorialize:
case 1) comment to post: we can simply select the column of the two authors, adding then column
    for bonding strenght and a False comm_to_comm flag.
    If more than one comment is present, each is treated differently, and eventually more comments
    of the same author will be menagend later in the count of the weight of the link;
case 2) a comment to comment exist: then an infinite many can exist.
    To vectorialize we can match parent_id of the latter to the comm_id of the former as before, but the case
    of a parent comment having more comment sons can happen, so the final dictionary can be a mess with
    different number of columns.
    We handle this noticing that each sibling comment has a unique parent, so we LEFT-MERGE the ditcionaries
    when pd.isna(parent_id) (parent_id is not nan), and select the columns of the two comments authors.
    This should also solve the problem for grand-sons and the entire discendence.
'''

import pandas as pd
import numpy as np

# 1. Load your original database
df = pd.read_csv('matching_post_comm - Copia.csv')

# 2. Create a reference mapping of comment IDs to their authors
# This is our lookup table for parent comments
comment_user_map = df[['comm_id', 'comm_auth']].rename(
    columns={'comm_id': 'parent_id', 'comm_auth': 'parent_author'}
)

# 3. Merge the mapping back into the main database
# Rows with NaN in 'parent_id' will simply get a NaN in 'parent_author'
merged_df = pd.merge(df, comment_user_map, on='parent_id', how='left')

# 4. Determine the 'former_author' using a vectorized conditional
# If 'parent_id' is NaN, it's a comment-to-post -> use 'post_auth'
# If 'parent_id' exists, it's a comment-to-comment -> use 'parent_author'
former_author = np.where(
    merged_df['parent_id'].isna(), 
    merged_df['post_auth'], 
    merged_df['parent_author']
)

# 5. Create the final clean database
final_df = pd.DataFrame({
    'former_author': former_author,
    'comment_author': merged_df['comm_auth']
})

# Optional: Clean up any instances where a parent_id existed but wasn't found in comment_id
final_df['former_author'] = final_df['former_author'].fillna('UNKNOWN_PARENT')

final_df['molteplicity']=0      #add molteplicity column at the end

# Save or view the result
final_df.to_csv('interaction_list.csv', index=False)

# COUNT THE MOLTEPLICITY OF THE COMMUTATOR