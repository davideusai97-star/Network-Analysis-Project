
import pandas as pd
import numpy as np

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

def count_same_author(ds, max_len, max_chunk, row, counter):            #recursive function to count post
    tmp_author_name=ds.at[row,'agent_name']       #memorize author name of the first post
    if row+1>=max_len: return counter           #prevent recursion at the end of the array
        
    if tmp_author_name == ds.at[row+1,'agent_name']:   #check if they wrote the second as well
        row = row+1
        counter=count_same_author(ds, max_len, max_chunk, row, counter)
    if counter >= max_chunk: return counter     #quit recursion to avoid stack overflow

    return counter+1

'''
dataset di prova:
['./prova_dataset/prova.csv', './prova_dataset/prova4.csv']         './prova_dataset/prova_active_agents.csv'

dataset veri:
['sort_comments_col0134.csv', 'sort_posts_col028.csv']          'sort_active_agents_col01.csv'

'''


#INIZIALIZZAZIONE VARIABILI
datasets_filename= ['sort_comments_col0134.csv', 'sort_posts_col028.csv']
agent_list_filename='sort_active_agents_col01.csv'
agent_list=pd.read_csv(agent_list_filename) #opens the csv that is to be modified
agent_list['activity']=pd.to_numeric(agent_list['activity'], errors='coerce')   #checks that activity value is an actual number
#agent_list_index=agent_list.set_index('name')
total_matches = 0

#INIZIO DEL CONFRONTO (ricerca di coincidenze tra autori di post e commenti con gli agenti)
for datasets in datasets_filename: 
    print(f'entering {datasets}')

    with open(datasets, 'r', encoding='utf-8') as f:    #count max lenght
        len_dataset = sum(1 for _ in f) -1              #remove header from the count

    row_counter=0
    max_recursion=50                   #insert limit to the recursion in the stack memory (max counter for 1 function call)
    control_counter=0

    progressing_control=1

    ds=pd.read_csv(datasets)

    while (row_counter<len_dataset) and (control_counter<max_recursion):
        control_counter += 1
        tmp_author_name=ds.at[row_counter, 'agent_name']            # memorize author
        if tmp_author_name in agent_list['name'].values:            # if is an agent, proceed to count their posts/comments
            nr_posts = count_same_author(ds, len_dataset, max_recursion, row_counter, 0)

            author_line=np.where(agent_list['name'] == tmp_author_name)[0]       # extract author line in agent_list
            #with open(datasets, 'w', encoding='utf-8') as f:
            agent_list.at[author_line[0], 'activity'] += nr_posts       #assigns activity accordingly to the number of posts/comments
            agent_list.to_csv(agent_list_filename, index=False)
            row_counter = row_counter + nr_posts                    #jumps to next author
            total_matches = total_matches + nr_posts

        else:
            row_counter += 1                  #cif author is not in agents, checks next line for existing authors
        
        if (row_counter-progressing_control*100000 <0) :    #print flag each 100k lines checked
            print(f'row {progressing_control*100}k reached')
            progressing_control += 1


    print(total_matches)


