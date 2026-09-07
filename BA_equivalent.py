import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_and_draw_equivalent_ba(target_N, target_E, target_clustering=None, seed=42):
    """
    Generates and visualizes a Barabási-Albert graph that aims to be equivalent
    to a given graph based on Nodes (N), Edges (E).
    Reports the discrepancy in clustering coefficient.

    Parameters:
    - target_N (int): Number of nodes in the desired equivalent graph.
    - target_E (int): Number of edges in the desired equivalent graph.
    - target_clustering (float, optional): The target average clustering coefficient.
    - seed (int): Random seed for reproducibility.
    """
    print("-" * 60)
    print(f"TARGET PROPERTIES: N={target_N}, E={target_E}, C_target={target_clustering}")
    print("-" * 60)

    # ---------------------------------------------------------
    # 1. Parameter Calculation (m)
    # ---------------------------------------------------------
    # In a standard BA model, E is approximately (N * m).
    # New nodes add 'm' edges each.
    
    # Validation: N must be greater than m.
    if target_N <= 1:
        print("Error: N must be greater than 1.")
        return

    m_calculated = round(target_E / target_N)
    
    # Ensure m is at least 1 and less than N.
    m_calculated = max(1, min(m_calculated, target_N - 1))
    
    print(f"Calculated BA parameter 'm' (edges added per step): {m_calculated}")
    print(f"Reasoning: E({target_E}) / N({target_N}) ≈ {target_E/target_N:.2f} -> rounded to {m_calculated}")

    # ---------------------------------------------------------
    # 2. Graph Generation
    # ---------------------------------------------------------
    print("\nGenerating standard Barabási-Albert graph...")
    G_ba = nx.barabasi_albert_graph(n=target_N, m=m_calculated, seed=seed)
    print("Graph generation complete.")

    # ---------------------------------------------------------
    # 3. Property Analysis and Reporting
    # ---------------------------------------------------------
    actual_N = G_ba.number_of_nodes()
    actual_E = G_ba.number_of_edges()
    actual_C = nx.average_clustering(G_ba)

    print("\nACTUAL PROPERTIES OF RESULTING BA GRAPH:")
    print(f"  - Nodes (N): {actual_N} (Match: {'YES' if actual_N == target_N else 'NO'})")
    print(f"  - Edges (E): {actual_E} (Requested: {target_E}, Discrepancy: {actual_E - target_E} ({np.abs(100 - 100*actual_E/target_E):.2f}%)")
    print(f"  - Avg. Clustering (C): {actual_C:.5f}")

    #ANALYSIS OF THE BA GRAPH
    deg_distribution = nx.degree_histogram(G_ba)
    density = nx.density(G_ba)
    betweenness_centrality = nx.betweenness_centrality(G_ba)

    #print(f"Histogram list: {deg_distribution}")
    #print(f"Density: {density}")
    #print(f"Betweenness Centrality: {betweenness_centrality}")      


    #VISUALIZE THE DISTRIBUTION OF DEGREES, CENTRALITY, CLUSTERING COEFFICIENTS
    # Compute sorted degree sequence and centrality lists for visualization
    degree_sequence = sorted([d for _, d in G_ba.degree()], reverse=True)      # sorted degrees (desc)
    centrality_vals = sorted(betweenness_centrality.values(), reverse=True) # sorted centrality values (desc)
    clustering = nx.clustering(G_ba)
    clust_vals = sorted(clustering.values(), reverse=True)
    avg_degree = sum(degree_sequence) / len(degree_sequence) if degree_sequence else 0

    avg_clust_coeff = sum(clust_vals) / len(clust_vals) if clust_vals else 0

    #PLOT THE STATISTICS
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
    #PLOT THE GRAPH
    plt.figure(figsize=(10, 8))
    
    # The spring layout visualizes hubs well
    pos = nx.spring_layout(G_ba, seed=seed) 

    # Draw nodes and edges
    nx.draw_networkx_edges(G_ba, pos, edge_color='gray', alpha=0.3)
    nx.draw_networkx_edges(G_ba, pos, edge_color='gray', alpha=0.3)
    
       # Highlight hubs: nodes in the top 5% by degree
    degrees = dict(G_ba.degree())
    hub_threshold = np.percentile(list(degrees.values()), 95)
    hubs = [node for node, degree in degrees.items()
            if degree >= hub_threshold]
    
    nx.draw_networkx_nodes(
        G_ba,
        pos,
        nodelist=[node for node in G_ba if node not in hubs],
        node_size=50,
        node_color='darkblue',
        alpha=0.7
    )
    
    nx.draw_networkx_nodes(
        G_ba,
        pos,
        nodelist=hubs,
        node_size=140,
        node_color='red',
        edgecolors='black',
        linewidths=0.5,
        label=f'Hubs (top 5%, n={len(hubs)})'
    )

    plt.legend()

    # Add titles and hide axes
    plt.title(f"Standard Barabási-Albert Graph\nN={actual_N}, E={actual_E}, m={m_calculated}\nAvg Clustering: {actual_C:.4f}", fontsize=14)
    plt.axis('off')
    print("\nVisualization complete. Close the plot window to finish.")
    plt.show()

    '''

#INITIAL SETTINGS (TO MATCH THE ACTUAL GRAPH)
# Define properties of a 'real' graph you want to mimic
# Real graphs often have much higher clustering than standard BA
given_N = 3111
given_E = 11612  # We want a mean degree around 2*E/N = 6, so m≈3
given_C = 0.11989993036014533  # High clustering - a 'small world' property

create_and_draw_equivalent_ba(given_N, given_E, given_C)




