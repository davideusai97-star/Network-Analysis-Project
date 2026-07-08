import duckdb
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Connect database, now every result (intermediate) will be stored in memory for the time of the computation
con = duckdb.connect()

# Create tables named comments and posts
Tables = 1
if Tables:
    con.execute("""
    CREATE TABLE comments AS
    SELECT agent_id, post_id
    FROM read_csv_auto('full_comments.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)

    con.execute("""
    CREATE TABLE posts AS
    SELECT submolt, agent_id, id
    FROM read_csv_auto('full_posts.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)


# Query: active users by submolts
submolts_active_users = con.execute("""
SELECT
    submolt,
    COUNT(DISTINCT agent_id) AS active_users
FROM (

    -- Users who created posts
    SELECT
        p.submolt,
        p.agent_id
    FROM posts p

    UNION

    -- Users who commented
    SELECT
        p.submolt,
        c.agent_id
    FROM comments c
    JOIN posts p
        ON c.post_id = p.id

) activity

GROUP BY submolt
ORDER BY active_users DESC;
""").fetchdf()

print(submolts_active_users)
submolts_active_users.to_csv("submolts_active_users.csv")
