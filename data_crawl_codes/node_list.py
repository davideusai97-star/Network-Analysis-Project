import pandas as pd

# 1. Load your edge list dataset
df = pd.read_csv('edge_list_collapsed.csv')

# 2. Combine unique values from both columns and drop duplicates
# pd.concat on index/series level is incredibly fast
unique_nodes = pd.concat([df['agent_A'], df['agent_B']]).unique()

# 3. Create a clean DataFrame for the nodes
nodes_df = pd.DataFrame(unique_nodes, columns=['agent_name'])

# 4. Optional: Drop any missing or UNKNOWN entries if they filtered through
nodes_df = nodes_df.dropna()
nodes_df = nodes_df[nodes_df['agent_name'] != 'UNKNOWN_PARENT']

# 5. Save the list of nodes
nodes_df.to_csv('nodes_list.csv', index=False, encoding='utf-8')

print(f"Total unique nodes (agents) found: {len(nodes_df)}")