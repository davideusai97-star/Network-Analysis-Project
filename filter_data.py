import csv

filename = "comments_col0134.csv"  # Specify the CSV file name
column_name = 'id'    #select columns to plot 

with open(filename, 'r', newline='') as inp:
    reader = csv.reader(inp)
    rows = [row for row in reader if (row[2] > "0")] # Remove rows where comments count are 0

with open(f'filtered_{filename}', 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerows(rows)


'''
POSTS/ARCHIVE:
'id', 'agent_id', 'agent_name', 'submolt', 'title', 'content', 'url', 'score', 'comment_count', 
'created_at', 'fetched_at', 'is_pinned', 'dump_date'

AGENTS/ARCHIVE:
'id', 'name', 'description', 'karma', 'follower_count', 'following_count', 'is_claimed',
'owner_x_handle', 'first_seen_at', 'last_seen_at', 'created_at', 'avatar_url', 'dump_date'

COMMENTS/ARCHIVE:
'id', 'post_id', 'agent_id', 'agent_name', 'parent_id', 'content', 'score', 'created_at',
'fetched_at', 'dump_date'

SUBMOLTS/ARCHIVE:
'name', 'display_name', 'description', 'subscriber_count', 'post_count', 'created_at',
'first_seen_at', 'avatar_url', 'banner_url', 'dump_date'
'''