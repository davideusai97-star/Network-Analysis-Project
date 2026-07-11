import pandas as pd
import numpy as np
import graph_tool.all as gt # This is heavy
from IPython.display import display, SVG
import matplotlib.pyplot as plt

from time import time


DATA_PATH = ""
start = time()
# Read the tables
nodes = pd.read_csv(DATA_PATH + "active_users.csv", usecols=[1, 2])
links = pd.read_csv(DATA_PATH + "linked_users.csv", usecols=[0, 1])
end = time()
print(f"Reading time: {end-start:.5f}")
NODES_ID_COL = "id"
NODES_LABEL_COL = "name"
LINKS_COL1 = "agent1"
LINKS_COL2 = "agent2"

# Create a directed graph
g = gt.Graph(directed=False)

# Add one vertex per node in the nodes table
g.add_vertex(len(nodes))

# Vertex properties
# They are built via property maps, which have to be called as below with the node as the index
v_node_label = g.new_vertex_property("string")
#v_leaning = g.new_vertex_property("string")

# Map external node_id -> internal vertex index
# Dictionary with structure: {"Id": vertex,}
# Not strictly needed but very useful for referral 
# Crucial for removal through iteration
vertex_dict = {}

# Assignment of properties (in this case, the ID is also a property)
start = time()
for i, row in nodes.iterrows():
    v = g.vertex(i)         # This is to call the nodes created in the graph at initialization, they are indexed by integers
                            # The order is meaningless as of now, as we will assign an id
    vertex_dict[row[NODES_ID_COL]] = v         # this is to build the dict
    v_node_label[v] = str(row[NODES_LABEL_COL])   # this tells the property map that node v has the string property row[NODES_LABEL_COL] (names)
    #v_leaning[v] = str(row["leaning"])      # same as above, but with a categorical property
end = time()
print(f"Elapsed time for vertex allocation: {end-start:.5f}")

# IMPORTANT: this assignation step is crucial to make the properties part of the graph
g.vertex_properties["node_label"] = v_node_label
#g.vertex_properties["leaning"] = v_leaning
g.vertex_properties["node_label"][g.vertex(len(nodes) - 1)]

# Edge property
# As above, they are given through edge property maps
#e_weight = g.new_edge_property("double")

# Add edges and weights
missing_entries = {}
start = time()
for _, row in links.iterrows():
    # Similar as above, an edge is used as its own index in the property map
    pos = 1
    try:
        source_node = vertex_dict[row[LINKS_COL1]]
    except KeyError:
        missing = row[LINKS_COL1]
        if missing not in missing_entries:
            missing_entries[missing] = 1
        else:
            missing_entries[missing] = missing_entries[missing] + 1
        continue
    try:
        target_node = vertex_dict[row[LINKS_COL2]]
    except KeyError:
        missing = row[LINKS_COL2]
        if missing not in missing_entries:
            missing_entries[missing] = 1
        else:
            missing_entries[missing] = missing_entries[missing] + 1
        continue

    e = g.add_edge(source_node, target_node)


    #e_weight[e] = float(row["weight"])
end = time()
print(f"Elapsed time for edges allocation: {end-start:.5f}")

print(missing_entries, len(missing_entries))

exit()
#g.edge_properties["weight"] = e_weight

# Fast implementation of the degree
# Note: of course you do this after the edges, duh
v_tot_degree = g.degree_property_map("total")
g.vertex_properties["tot_degree"] = v_tot_degree

# Useful question: how do we list the nodes/edges/neighbours?
# Answer: via a method. gt is very method-centric

# Accessing and sorting example
rows = []
for v in g.vertices():
    degree = v.in_degree() # degree
    rows.append((degree, v))

rows.sort(key= lambda x: x[0])

for deg, v in rows:
    print(f"{deg}, {g.vertex_properties["node_label"][v]}")
    print(v.in_degree(), v.out_degree())


# ===============================================


# Diffusion
# The diffusion is a new object that generate the dynamics via some rules
# Most important methods are .iterate_sync/async -> step evolution and get_state -> Property Map
DIFFUSION = False
if DIFFUSION:
    state = gt.SISState(g, beta=0.01, gamma=0.007, v0=vertex_dict["B-VOLLEYBALL-READY"])
    X = []
    for t in range(1000):
        ret = state.iterate_sync()
        #print(state.get_state().a)
        X.append(state.get_state().a.sum()) # This is an important line
        # VertexPropertyMap.a returns a filtered numpy array that points to the property values
        # In the SIS case, either 0 or 1 => sum is the count of infected nodes

    # As above, we need to add the property map of the diffusion to the graph
    # I think we could have more control on the kind of property map offered by the process
    g.vertex_properties["Infected"] = state.get_state()
    plt.plot(X)
    plt.savefig("reddit_network_SIS_results.png")
    plt.show()


# ===============================================


# Visualization

# List all properties on the graph (VERY useful)
g.list_properties()

out_name = "moltbook_base"
# Best: open in Gephi
# Every ranking on Gephi-lite online can be obtained through a property map
g.save(out_name + ".graphml")

# Draw to SVG
gt.graph_draw(
    g,
    vertex_text=v_node_label,
    vertex_fill_color="lightsteelblue",
    vertex_size=2,
    #edge_pen_width=gt.prop_to_size(e_weight, 0.5, 4.0),
    edge_end_marker="arrow",
    edge_color="red",
    output=out_name,
)

display(SVG(out_name))
