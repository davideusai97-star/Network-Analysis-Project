import duckdb
import pandas as pd


Maradona = 10
Pellè = 9

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Connect database, now every result (intermediate) will be stored in memory for the time of the computation
con = duckdb.connect()

# Create tables named comments and posts
con.execute("""
CREATE TABLE comments AS
SELECT id, agent_id, post_id, parent_id
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

# Query: users that posted or commented
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


# ========================================================
# Queries and tables for submolts filtered comments & users

SUBMOLT = 'philosophy'
PREFIX = SUBMOLT + "_" if SUBMOLT != '' else ''

SUBMOLT_COMMENTS = PREFIX + "comments"
LINKED_TABLE = PREFIX + "linked"

if SUBMOLT != '':
    # Table for filtered comments by submolt
    con.execute(f"""
    CREATE TABLE '{SUBMOLT_COMMENTS}' AS
    SELECT 
        c.id AS id,
        c.agent_id AS agent_id,
        c.post_id AS post_id,
        c.parent_id AS parent_id,
        submolt
    FROM comments c
    JOIN (SELECT * FROM posts WHERE submolt = '{SUBMOLT}') p
        ON c.post_id = p.id
    """)

# Query: users that are linked via commenting, optionally filtered by submolts
con.execute(f"""
CREATE TABLE '{LINKED_TABLE}' AS
SELECT DISTINCT  --DISTINCT should be redundant
LEAST (cid_1, cid_2) AS agent1,
GREATEST (cid_1, cid_2) AS agent2
FROM (

    -- Users who commented to a post in SUBMOLT
    SELECT
        c.agent_id AS cid_1,
        p.agent_id AS cid_2,
    FROM '{SUBMOLT_COMMENTS}' c
    JOIN posts p
        ON c.post_id = p.id

    UNION

    -- Users who commented to a comment
    SELECT
        c.agent_id AS cid_1,
        c2.agent_id AS cid_2
    FROM '{SUBMOLT_COMMENTS}' c
    JOIN (SELECT * FROM '{SUBMOLT_COMMENTS}' WHERE parent_id <> '0') c2
        ON c.id = c2.parent_id

)
WHERE agent1 <> agent2
ORDER BY agent1, agent2
""")

con.execute(f"""
COPY '{LINKED_TABLE}'
TO '{LINKED_TABLE}_users.csv'
(FORMAT CSV, HEADER);
""")

# Users list who commented or have been commented onto
active_users = con.execute(f"""
SELECT a.id AS id, name
FROM (
    SELECT agent1 AS id
    FROM {LINKED_TABLE}
                            
    UNION

    SELECT agent2 AS id
    FROM {LINKED_TABLE}
    ) a
    JOIN agents 
        ON a.id = agents.id
ORDER BY name
""").fetchdf()
active_users.to_csv(f"{PREFIX}active_users.csv")


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
