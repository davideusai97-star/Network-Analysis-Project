import csv
import pandas as pd

'''
Two agents count as linked if one posted smt and the other commented on it. Link is undirected and
weighted by the number of times this happened. Connectivity is symmetric with this definition.

    -ISSUE: DONE
We need to reduce the number of agents, since the connectivity matrix goes as N^2.
To do this, we only take the agents that commented or posted at least once.
We take this information from comment and post datasets 'agent_name', and assign a boolean in agents_col134.
There is the problem of the sorting of agents in the three datasets, which is not guaranteed to be the same.
So we need to sort them by agent_name and then assign the boolean or a value.
We implement the sorting option inside the select columns function.

    -ISSUE: LIST ACTIVE AGENTS
We assign each agent in the list a value of +1 for each action taken (posted or commented once).
The final value of each agent can be used as a proxy for the degree of the node.
We could take each agent name and check its word frequency in post and comments reduced datasets (without
reading the actual content of the post or comment). Unfortunately, several agents name are numbers or contain
characters that would invalidate this approach. There may be also that some name is part of other agents' larger names.
The only way is to check the actual array of posts and comments and count the presence.
Since they are ordered, all the posts with the same author are next to each other, so we can count the number of lines with the same author name
and assign the number to active_agents[activity] where active_agents[author_name].
In this way, there is no searching over the two datasets.
'''

def count_same_author(ds, max_len, row, counter):            #recursive function to count post
    print('row nr ', row)
    tmp_author_name=ds['agent_name'][row]       #memorize author name of the first post
    if row+1>=max_len: return counter           #prevent recursion at the end of the array
        
    if tmp_author_name == ds['agent_name'][row+1]:   #check if they wrote the second as well
        print(f'entering line {row}')
        row = row+1
        counter=count_same_author(ds, max_len, row, counter)

#INIZIALIZZAZIONE VARIABILI
ds_name=['sort_comments_col0134.csv']#, 'sort_posts_col0134.csv']

agent_list=pd.read_csv('sort_active_agents_col1.csv') #opens the csv that is to be modified
agent_list['activity']=pd.to_numeric(agent_list['activity'], errors='coerce')   #checks that activity value is an actual number
agent_list=agent_list.set_index('name')
total_matches = 0

#INIZIO DEL CONFRONTO (ricerca di coincidenze tra autori di post e commenti con gli agenti)
for datasets in ds_name: 
    row_counter=0
    ds=pd.read_csv(ds_name)
    while (row_counter<len(ds)):
        tmp_author_name=ds[row_counter]['agent_name']       # memorize author
        if tmp_author_name in agent_list['name']:           # if is an agent, proceed to count their posts/comments
            nr_posts = count_same_author(ds, len(ds), row_counter, 1)
            agent_list[tmp_author_name][row_counter] = nr_posts     #sets activity accordingly to the number of posts/comments
            row_counter += nr_posts             #jumps to next author
        else: row_counter += 1                  #checks next line for existing authors