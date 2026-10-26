import pandas as pd
import numpy as np
import csv

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
    We handle this noticing that each sibling comment has a unique parent, so we RIGHT-MERGE the ditcionaries
    when pd.isna(parent_id) (parent_id is not nan), and select the columns of the two comments authors.
    This should also solve the problem for grand-sons and the entire discendence.
'''

ds=pd.read_csv('matching_post_comm.csv', usecols=['post_auth', 'comm_id', 'comm_auth', 'parent_id'])
len_ds=len(ds)
progression_control_counter=1


header=['former_auth', 'latter_auth', 'bond_strenght', 'comm_to_comm']      #former can be post or comment author, latter is always comment auth
with open('agent_link.csv', 'w', encoding= 'utf-8') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(header)

    for i in range(len_ds):
        if pd.notna(ds.at[i, 'parent_id']):         #if is comment to comment
            former_comm_line_array=np.where(ds['comm_id']==ds.at[i, 'parent_id'])[0]      #search for the author of the parent comment (expected to be UNIQUE)
            former_auth=former_comm_line_array[0].fillna('UNKNOWN_PARENT')                #orphan control      
            output_line=pd.DataFrame({
                'former_auth': former_auth,
                'latter_auth': ds['comm_auth'],
                'bond_strenght': 0,                     #later used to count molteplicity (weight) of edges
                'comm_to_comm': 1
                })
            output_df.to_csv('agent_link.csv', index=False, encoding='utf-8')
        else:
            output_df = pd.DataFrame({
                'former_auth': ds.at[i, 'post_auth'],
                'latter_auth': ds.at[i, 'comm_auth'],
                'bond_strenght': 0, # Kept your original spelling from the header
                'comm_to_comm': 0 # Converts True/False to 1/0
            })
            output_df.to_csv('agent_link.csv', index=False, encoding='utf-8')
        
        if i==progression_control_counter*100000: print(f'line {progression_control_counter*100000} reached')
        
    




    
