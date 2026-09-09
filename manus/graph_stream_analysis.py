"""
requires dynetx: https://github.com/GiulioRossetti/dynetx.git
conda install dynetx
OR
pip install dynetx
"""

import dynetx as dn
from dynetx import DynGraph
from networkx import Graph
import os

cwd = os.getcwd()

DATA_PATH = cwd + "/proc/"
SUBMOLT = "philosophy"
PREFIX = SUBMOLT + "_" if SUBMOLT != '' else ''


# Bunching function: takes the raw Link+datetime table, bunching interval (time), opt[start date, end date]
# timestamps: N time intervals of size bunching interval, from the first datetime to the 
# Return: link+timestamp table, where  in which the link occurs 

# Build the graph from link+timestamp table: 
# Append link(s) at timestamp T (group them per snapshot)
# If the link endpoints are duplicated (check either with the graph itself or an external list):
#  Update weight property of the link 
# NOTE: DynGraph is a subclass of nx.Graph, so it inherits its general interface
# The relevant differences are:
# Load with g.add_interaction
# Check interactions with g.interactions
# The spawn (and eventual death) times of the interactions are
# Handled through a property: g.time_to_edge like this {"ts1": {(u1, v1, "+"/"-"): None}, "ts2": {(u2, v2, "+"/"-"): None}, ...}
# ts are the timestamps, u and v the nodes
# ACHTUNG! WARNING! ATENCÌON!: DUPLICATED CONNECTION (for graph without edge removal) ARE QUIETLY SKIPPED
# Also, timed properties are not handled 
"""It's kinda shit NGL -MAP, 30/08/2026"""
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
