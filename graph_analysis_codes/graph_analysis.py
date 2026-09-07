import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Analysis of the graph data using NetworkX and Matplotlib. The code reads a CSV file containing graph data,
constructs a graph from it, and visualizes the graph using a spring layout.

MAKE A WEIGHTED VERSION OF DATASET, UN-TIMESTAMPED. CHECK IF WEIGHTS SIGNIFICANTLY CHANGE THE RESULTS

STATIC GRAPH ANALYSIS:
Degree distribution, V
avg degree (---> small world? scale free?),        
Connected components analysis;                              
Path analysis (avg path lenght, diameter, )
Clustering Coefficient (global + local, avg),     V         ----> low clustering? ---> barabasi-albert Clust_BA = (ln N^2)/N = 0.0052 for N=3111
Density analysis (sparse? dense? self-interactions?);       ---->unweighted density = 0.0024, weighted density = 0.0009??
Centrality analysis (degree,
    connectivity: katz?,
    geometrical: closeness? farness? betweeness?)
S-analysis with edge weight?

CLUSTER 1: COMMUNITY DISCOVERY
Assortativity (homophily, degree correlation)                   LOUVAIN ha senso qui?
Bridges detection (GIRVAN-NEUMANN) and neighbourhood
k-cliques?
Label propagation?


and many others ...
Compare with random models ER and BA, and see how the properties differ.
RANDOM MODEL: avg distance and degree in ER is it sparse?
BARABASI: max degree of a hub is consistent with osservation?


DYNAMIC ANALYSIS: is it present some sort of preferenctial attachment? or the new nodes and links are random?
'''



'''Datasets
edge_list_collapsed
philosophy_timestamped_users
philosophy_timestamped_users_weighted
'''

data_folder='./full_datasets/'
data=pd.read_csv(f'{data_folder}philosophy_timestamped_users.csv')  # Assuming you have a CSV file with graph data

col1=data.columns[0]
col2=data.columns[1]
#print(f'col1: {col1}, col2: {col2}')

# 2. Create the graph from the DataFrame
# If your graph has directional flow, add: create_using=nx.DiGraph()
G = nx.from_pandas_edgelist(
    data, 
    source=col1, 
    target=col2, 
    edge_attr=True # Keeps any extra columns (like 'weight') as edge attributes
)

#DEGREES AND DENSITY OF EDGES PROPERTIES
deg_distribution = nx.degree_histogram(G)
density = nx.density(G)
betweenness_centrality = nx.betweenness_centrality(G)

#print(f"Histogram list: {deg_distribution}")
#print(f"Density: {density}")
#print(f"Betweenness Centrality: {betweenness_centrality}")      

#VISUALIZE THE DISTRIBUTION OF DEGREES, CENTRALITY, CLUSTERING COEFFICIENTS
# Compute sorted degree sequence and centrality lists for visualization
degree_sequence = sorted([d for _, d in G.degree()], reverse=True)      # sorted degrees (desc)
centrality_vals = sorted(betweenness_centrality.values(), reverse=True) # sorted centrality values (desc)
clustering = nx.clustering(G)
clust_vals = sorted(clustering.values(), reverse=True)
avg_degree = sum(degree_sequence) / len(degree_sequence) if degree_sequence else 0
avg_clust_coeff = sum(clust_vals) / len(clust_vals) if clust_vals else 0

# Print basic stats
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
print(f"Max degree: {degree_sequence[0] if degree_sequence else 0}, avg degree: {avg_degree:.2f}, density: {density:.5f}")

#top_n = 10
#top_central = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
#print(f"Top {top_n} nodes by betweenness centrality: {top_central}")

'''
# Visualization: degree distribution histogram (log-scaled y), degree-rank plot, centrality histogram, clustering histogram
plt.figure(figsize=(10, 6))
plt.hist(degree_sequence, bins=50, color='C0', edgecolor='k', alpha=0.7)
plt.yscale('log')
plt.xlabel('Degree')
plt.ylabel('Frequency (log scale)')
plt.title('Degree Distribution (log y)')
plt.tight_layout()

plt.figure(figsize=(10, 6))
ranks = np.arange(1, len(degree_sequence) + 1)
plt.loglog(ranks, degree_sequence, marker='.', linestyle='none', markersize=4)
plt.xlabel('Rank')
plt.ylabel('Degree')
plt.title('Degree Rank Plot (log-log)')
plt.tight_layout()

plt.figure(figsize=(10, 6))
plt.hist(centrality_vals, bins=50, color='C1', edgecolor='k', alpha=0.7)
plt.yscale('log')
plt.xlabel('Betweenness Centrality')
plt.ylabel('Frequency (log scale)')
plt.title('Betweenness Centrality Distribution')
plt.tight_layout()

plt.figure(figsize=(10, 6))
plt.hist(clust_vals, bins=50, color='C2', edgecolor='k', alpha=0.7)
plt.xlabel('Clustering Coefficient')
plt.ylabel('Frequency')
plt.title('Clustering Coefficient Distribution')
plt.tight_layout()

plt.show()
'''

#PATH AND CONNECTED COMPONENTS ANALYSIS
is_directed = G.is_directed()
    
# 1. Check Connectivity
if is_directed:
    is_conn = nx.is_strongly_connected(G)
else:
    is_conn = nx.is_connected(G)
# 2. Extract Subgraph if Disconnected
if is_conn:
    target_graph = G
else:
    print("-> Analyzing path metrics on the Largest Connected Component (LCC)...")
    if is_directed:
        lcc_nodes = max(nx.strongly_connected_components(G), key=len)
    else:
        lcc_nodes = max(nx.connected_components(G), key=len)
    target_graph = G.subgraph(lcc_nodes).copy()
    print(f"-> LCC Size: {target_graph.number_of_nodes()} nodes ({target_graph.number_of_nodes()/G.number_of_nodes():.1%})")

# 3. Calculate Path Metrics
diameter = nx.diameter(target_graph)
radius = nx.radius(target_graph)
avg_path_length = nx.average_shortest_path_length(target_graph)
center_nodes = nx.center(target_graph)
periphery_nodes = nx.periphery(target_graph)

# 4. Display Results
print("PATH ANALYSIS RESULTS")

print(f"Diameter (Max shortest path):       {diameter}")
print(f"Radius (Min eccentricity):          {radius}")
print(f"Average Path Length:               {avg_path_length:.4f}")
print(f"Center Nodes (Eccentricity = {radius}):   {center_nodes[:5]}{'...' if len(center_nodes) > 5 else ''}")
print(f"Peripheral Nodes (Eccentricity = {diameter}): {periphery_nodes[:5]}{'...' if len(periphery_nodes) > 5 else ''}")

'''
# 3. Set up the canvas
plt.figure(figsize=(10, 8))

# 4. Calculate node positions
# spring_layout uses a physics simulation to space nodes evenly and reduce clutter
pos = nx.spring_layout(G, seed=42) 

# 5. Draw the graph
nx.draw(
    G, 
    pos, 
    with_labels=False, 
    node_color='red', 
    node_size=0.5, 
    edge_color='lightblue', 
    font_size=10, 
    font_weight='bold'
)

# 6. Render the plot
plt.title("Network Visualization", fontsize=14)
plt.show()

'''




'''
philosophy_timestamped_users_weighted.csv
mean clustering coefficient: 0.11989993036014533, average clustering coefficient (NetworkX): 0.11989993036014544
Nodes: 3111, Edges: 11612
Max degree: 574




'''