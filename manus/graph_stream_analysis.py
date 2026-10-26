"""
requires dynetx: https://github.com/GiulioRossetti/dynetx.git
conda install dynetx
OR
pip install dynetx
"""

import dynetx as dn
import networkx as nx
import pandas as pd
from dynetx import DynGraph
from networkx import Graph
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()

DATA_PATH = cwd + "/proc/"
SUBMOLT = "many"
PREFIX = SUBMOLT + "_" if SUBMOLT != '' else ''
TIMESTAMP_FILE = PREFIX + "timestamped_users.csv"

BIN_SIZE = "1h"


# Bunching function: takes the raw Link+datetime table, bunching interval (time), opt[start date, end date]
# timestamps: N time intervals of size bunching interval, from the first datetime to the 
# Return: link+timestamp table, where  in which the link occurs 

def add_time_bins(df: pd.DataFrame | pd.Series, datetime_col, freq="1h", new_col="bin_timestamp"):
    """
    Example time frquencies:
    "30s"       # 30 seconds
    "5min"      # 5 minutes
    "2h"        # 2 hours
    "6h"        # 6 hours
    "3D"        # 3 days
    "2W"        # 2 weeks
    "1D12h"     # 1.5 days
    """
    df = df.copy()

    # Parse timestamps including timezone offset
    dt = pd.to_datetime(df[datetime_col], format="mixed", utc=True)

    # Create integer bin IDs starting from 0
    df[new_col] = (
        (dt - dt.min()) // pd.Timedelta(freq)
    ).astype(int)

    return df

# Gneral idea:
# Build the graph from link+timestamp table: 
# Append link(s) at timestamp T (group them per snapshot)
# TODO:
# If the link endpoints are duplicated (check either with the graph itself or an external list):
#  Update weight property of the link

df = pd.read_csv(DATA_PATH + TIMESTAMP_FILE)
df = add_time_bins(df, "timestamp", freq=BIN_SIZE)

G = DynGraph()

top_5_nodes = ['7c943ee1-d639-4901-8f9f-1b1a138f660d', 'd6936b86-9755-4317-9277-98ebb8e48808',
                  '4a4d8cae-020b-4d20-bae1-7583e41fc615', '36436542-f42e-449a-baf7-5d4c01ccc9b9',
                  'a25b5136-b143-4c1a-9f79-ddaa986f33d9']

# We calculate directly in the cycle the properties that vary in time

# TODO: measures
# Centrality? Path?

measures = {
    "nodes": [],
    "edges": [],
    "avg_degree": [],
    "density": [],
    "avg_cluster_coef": [],
    "conn_component": [],
    "0_node_degree": [],
    "1_node_degree": [],
    "2_node_degree": [],
    "3_node_degree": [],
    "4_node_degree": [],
    }

current_t = 0
verbose = 1
# ~ 2700 snapshots
# 27 min T.T
for _, row in df.iterrows():
    time = row["bin_timestamp"]

    if current_t < time:
        # Calculate measures
        nodes_n = G.number_of_nodes()
        edges_n = G.number_of_edges()
        avg_deg = sum(dict(G.degree()).values()) / G.number_of_nodes()
        dens = nx.density(G)
        clust_coef = nx.average_clustering(G)
        conn_comp = nx.number_connected_components(G)

        measures["nodes"].append(nodes_n)
        measures["edges"].append(edges_n)

        measures["avg_degree"].append(avg_deg)
        measures["density"].append(dens)
        measures["avg_cluster_coef"].append(clust_coef)
        measures["conn_component"].append(conn_comp)

        degs = G.degree(top_5_nodes)
        
        for i, deg in enumerate(degs.values()):
            measures[str(i) + "_node_degree"].append(deg)

        if verbose:
            print(f"\nSnapshot: {current_t}")
            print("Nodes:", nodes_n)
            print("Edges:", edges_n)
            print(
                "Average degree:",
                avg_deg
            )
            print(
                "Density:",
                dens
            )
            print(
                "Average clustering coef.:",
                clust_coef
            )
            print(
                "Connected components:",
                conn_comp
            )

        """
        Slowwwwww
        lcc = G.subgraph(max(nx.connected_components(G), key=len))
        print(
            "Diameter (largest connected component):",
            nx.diameter(lcc)
            )
        """
        current_t = time

    G.add_interaction(
        row["agent1"],
        row["agent2"],
        t=time
    )

# Top X (final) degree nodes, change of their degree in time
sorted_nodes_degrees = sorted(G.degree_iter(), key=lambda tup: tup[1], reverse=True)[:5]
print("Top 5 node degrees: ", sorted_nodes_degrees)

for title, vals in measures.items():
    plt.plot(vals)
    plt.title(title)
    plt.show()

# This takes forever
print("Average node number in time:", G.avg_number_of_nodes())
# This takes MORE forever
#print("Time density:", G.density())


# NOTE: DynGraph is a subclass of nx.Graph, so it inherits its general interface
# The relevant differences are:
# Load with g.add_interaction
# Check interactions with g.interactions
# The spawn (and eventual death) times of the interactions are
# Handled through a property: g.time_to_edge like this {"ts1": {(u1, v1, "+"/"-"): None}, "ts2": {(u2, v2, "+"/"-"): None}, ...}
# ts are the timestamps, u and v the nodes
# ACHTUNG! WARNING! ATENCÌON!: DUPLICATED CONNECTION (for graph without edge removal) ARE QUIETLY SKIPPED
# Also, timed properties are not handled

# To check for edges: self.has_edge(u, v) or (maybe better) self.interactions()
""" From ntwrokx.classes.graph.py, 231-237:
    **Subclasses (Advanced):**

    The Graph class uses a dict-of-dict-of-dict data structure.
    The outer dict (node_dict) holds adjacency information keyed by node.
    The next dict (adjlist_dict) represents the adjacency information and holds
    edge data keyed by neighbor.  The inner dict (edge_attr_dict) represents
    the edge data and holds edge attribute values keyed by attribute names.

"""
# We care about edge_attr_dict
# We need to add another index to distinguish timesteps
# Idea: another nested dict: at the key edge_attr_dict["custom_property"] we add a dictionary {ts: value_at_ts}
# Better not to do this manually if it can be avoided
# This should permit us to reference and modify the property somewhat cleanly

# Then run all the dynamic-adapted quantities: degree, density, ...
# Probably need to implement an indexing function to 
# cleanly manage the retrieval/set of the property (we usually want to change timestep by timestep)
