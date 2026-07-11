import duckdb
import pandas as pd


Maradona = 10
Pellè = 9

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Connect database, now every result (intermediate) will be stored in memory for the time of the computation
con = duckdb.connect()

# Create tables named comments and posts
Tables = 1
if Tables:
    con.execute("""
    CREATE TABLE comments AS
    SELECT id, agent_id, post_id, parent_id
    FROM read_csv_auto('full_comments.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)

    con.execute("""
    CREATE TABLE comments2 AS
    SELECT id, agent_id, parent_id
    FROM read_csv_auto('full_comments.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)

    con.execute("""
    CREATE TABLE posts AS
    SELECT submolt, agent_id, id
    FROM read_csv_auto('full_posts.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)

    con.execute("""
    CREATE TABLE agents AS
    SELECT id, name
    FROM read_csv_auto('full_agents.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
    """)

# Query: users that posts
poster_users = con.execute("""
-- Users who commented or posted
SELECT DISTINCT
    id,
    name
FROM (
    SELECT DISTINCT a.id AS id, a.name AS name
    FROM agents a
    JOIN posts p
        ON a.id = p.agent_id
    
    UNION
    
    SELECT DISTINCT a.id AS id, a.name AS name
    FROM agents a
    JOIN comments c
        ON a.id = c.agent_id
)
--WHERE name <> ''
ORDER BY name
""").fetchdf()
poster_users.to_csv("poster_users.csv")


# Query: linked users
con.execute("""
CREATE TABLE linked AS
SELECT DISTINCT  --DISTINCT should be redundant
LEAST (cid_1, cid_2) AS agent1,
GREATEST (cid_1, cid_2) AS agent2
FROM (

    -- Users who commented to a posts
    SELECT
        c.agent_id AS cid_1,
        p.agent_id AS cid_2
    FROM comments c
    JOIN posts p
        ON c.post_id = p.id

    UNION

    -- Users who commented to a comment
    SELECT
        c.agent_id AS cid_1,
        c2.agent_id AS cid_2
    FROM comments c
    JOIN (SELECT * FROM comments2 WHERE parent_id != '0') c2
        ON c.id = c2.parent_id

) linked
WHERE agent1 <> agent2
ORDER BY agent1, agent2
""")

con.execute("""
COPY linked
TO 'linked_users.csv'
(FORMAT CSV, HEADER);
""")

active_users = con.execute("""
SELECT a.id AS id, name
FROM (
    SELECT agent1 AS id
    FROM linked
                            
    UNION

    SELECT agent2 AS id
    FROM linked
    ) a
    JOIN agents 
        ON a.id = agents.id
""").fetchdf()
active_users.to_csv("active_users.csv")


# Equivalent query
if Maradona < Pellè:
    linked_users2 = con.execute("""
    SELECT DISTINCT user1, user2
    FROM (

        SELECT
            LEAST(c.agent_id, p.agent_id) AS user1,
            GREATEST(c.agent_id, p.agent_id) AS user2
        FROM comments c
        JOIN posts p
            ON c.post_id = p.id
        WHERE c.agent_id <> p.agent_id

        UNION

        SELECT
            LEAST(c.agent_id, parent.agent_id) AS user1,
            GREATEST(c.agent_id, parent.agent_id) AS user2
        FROM comments c
        JOIN comments parent
            ON c.parent_id = parent.id
        WHERE c.parent_id <> '0'
        AND c.agent_id <> parent.agent_id

    ) linked
    ORDER BY user1, user2 
    """).fetchdf()

    #print(linked_users)
    linked_users2.to_csv("linked_users2.csv")
