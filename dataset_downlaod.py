import csv
from datasets import load_dataset

SUB_DATASET="comments"      #can be: posts, agents, comments, submolts, world_frequency, snapshots
SPLIT="archive"

#ds = load_dataset("SimulaMet/moltbook-observatory-archive", "agents" , data_files="data/posts/2026-01-1*.parquet", split="archive")
ds = load_dataset("SimulaMet/moltbook-observatory-archive", SUB_DATASET , split=SPLIT)


FILENAME=f"full_{SUB_DATASET}.csv"
ds.to_csv(FILENAME, index=False)


print(ds.column_names)


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