import csv
import pandas as pd

'''
Two agents count as linked if one posted smt and the other commented on it. Link is undirected and
weighted by the number of times this happened. Connectivity is symmetric with this definition.

ISSUE: DONE
    -We need to reduce the number of agents, since the connectivity matrix goes as N^2.
To do this, we only take the agents that commented or posted at least once.
We take this information from comment and post datasets 'agent_name', and assign a boolean in agents_col134.
There is the problem of the sorting of agents in the three datasets, which is not guaranteed to be the same.
So we need to sort them by agent_name and then assign the boolean or a value.
We implement the sorting option inside the select columns function.

ISSUE: LIST ACTIVE AGENTS
We assign each agent in the list a value of 1 for each action taken (posted or commented once).
We so check the authors of posts and comments, assign 

HOW TO IMPLEMENT:
filter posts by post[comments_count] > 0        NOT REQUIRED
filter comments by comment[post_id] in posts[post_id] NOT REQUIRED
link exists between filtered_comment[agent_name] and filtered_post[agent_name]
'''
ds=pd.read_csv('agents_col0134.csv')  # Specify the CSV file name
'''
filename = "comments_col0134.csv"  # Specify the CSV file name
column_name = 'id'    #select columns to plot 

with open(filename, 'r', newline='') as inp:
    reader = csv.reader(inp)
    rows = [row for row in reader if (row[2] > "0")] # Remove rows where comments count are 0

with open(f'filtered_{filename}', 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerows(rows)

'''
