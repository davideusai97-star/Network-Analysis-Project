import pandas as pd
import numpy as np
import csv

ds=pd.read_csv('matching_post_comm.csv', usecols=['post_auth', 'comm_id', 'comm_auth', 'parent_id'])
len_ds=len(ds)

header=['former_auth', 'latter_auth', 'bond_strenght', 'comm_to_comm']      #former can be post or comment author, latter is always comment auth
with open('agent_link.csv', 'w', encoding= 'utf-8') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(header)
    for i in range(len_ds):
        if pd.notna(ds.at[i, 'parent_id']):         #if is comment to comment
            former_comm_line=np.where(ds['comm_id']==ds.at[i, 'parent_id'])[0]      #search for the author of the parent comment
            # Safety check: Ensure the parent comment actually exists in the file
            if former_comm_line > 0:
                former_comm_line = former_comm_line[0]
                parent_author = ds.at[former_comm_line, "comm_auth"]

                writer.writerow([parent_author, ds.at[i, "comm_auth"], 0, 1])       #former comm auth and latter comment auth
            else:
                # Fallback row if parent_id exists but its matching row wasn't found
                writer.writerow(["UNKNOWN_PARENT", ds.at[i, "comm_auth"], 0, 1])
        else:
            writer.writerow([ds.at[i, 'post_auth'], ds.at[i, 'comm_auth'], 0, 0])


    
