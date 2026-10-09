import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

# Graph parameters
num_nodes = 9339
num_edges = 56674
seed = random.seed()

# Generate the Erdős-Rényi random graph G(n, m)
G_er = nx.gnm_random_graph(n=num_nodes, m=num_edges, seed=seed)

# Degree and clustering statistics
degree_dict = dict(G_er.degree())
degree_sequence = sorted(degree_dict.values(), reverse=True)
clustering = nx.clustering(G_er)
clust_vals = sorted(clustering.values(), reverse=True)

# Betweenness centrality: exact computation is too expensive for this graph size;
# a sampled approximation keeps the analysis tractable.
betweenness_dict = nx.betweenness_centrality(G_er, k=1000, seed=seed)
centrality_vals = sorted(betweenness_dict.values(), reverse=True)

density = nx.density(G_er)
avg_degree = sum(degree_sequence) / len(degree_sequence) if degree_sequence else 0
avg_clustering = sum(clust_vals) / len(clust_vals) if clust_vals else 0

print(f'density: {density}, avg degree: {avg_degree:.4f}, avg clustering coefficient: {avg_clustering:.4f}')
print(f'max degree: {max(degree_sequence)}, max betweenness centrality: {max(centrality_vals):.4f}')


'''
# Degree-rank plot
ranks = np.arange(1, len(degree_sequence) + 1)

plt.figure(figsize=(10, 6))
plt.hist(degree_sequence, bins=50, color='C0', edgecolor='k', alpha=0.7)
plt.yscale('log')
plt.xlabel('Degree')
plt.ylabel('Frequency (log scale)')
plt.title('Degree Distribution (log y)')
plt.tight_layout()

plt.figure(figsize=(10, 6))
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

'''

# Plot the graph
plt.figure(figsize=(10, 8))
# Fewer iterations keep the layout computation tractable on a large graph.
pos = nx.spring_layout(G_er, seed=seed, k=0.25, iterations=25)

nx.draw_networkx_edges(G_er, pos, edge_color='gray', alpha=0.3)

hub_threshold = np.percentile(list(degree_dict.values()), 95)
hubs = [node for node, degree in degree_dict.items() if degree >= hub_threshold]


nx.draw_networkx_nodes(
    G_er,
    pos,
    nodelist=G_er.nodes(),
    node_size=5,
    node_color='red',
    edgecolors='lightblue',
    linewidths=0.3,
    alpha=0.7,
)

plt.axis('off')
print("\nVisualization complete. Close the plot window to finish.")
plt.show()