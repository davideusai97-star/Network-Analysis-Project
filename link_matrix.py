import csv
import pandas as pd

'''
Two agents count as linked if one posted smt and the other commented on it. Link is undirected and
weighted by the number of times this happened. Connectivity is symmetric with this definition.

HOW TO IMPLEMENT:
filter posts by post[comments_count] > 0
filter comments by comment[post_id] in posts[post_id]
link exists between filtered_comment[agent_name] and filtered_post[agent_name]
'''

posts = pd.read_csv("filtered_posts_col028.csv")
comments = pd.read_csv('./full_datasets/full_comments.csv')

#total_comments=posts['comment_count'].sum()
#print(f"Total comments: {total_comments}")
print(len(comments))
