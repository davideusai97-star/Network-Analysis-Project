import duckdb
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Connect database, now every result (intermediate) will be stored in memory for the time of the computation
con = duckdb.connect()

# Create tables named comments and posts
con.execute("""
CREATE TABLE comments AS
SELECT agent_id, post_id
FROM read_csv_auto('full_comments.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
""")

con.execute("""
CREATE TABLE posts AS
SELECT submolt, agent_id, id, comment_count
FROM read_csv_auto('full_posts.csv', nullstr=['NaT', 'NA', 'N/A', 'null'])
""")

# Total comments in submolts
con.execute("""
CREATE TABLE submolts_comments AS
SELECT
    submolt,
    SUM(comment_count) AS total_comments
FROM posts
GROUP BY submolt
ORDER BY total_comments DESC, submolt
""")

# Active users by submolts
con.execute("""
CREATE TABLE submolts_users AS
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

)
GROUP BY submolt
ORDER BY active_users DESC, submolt;
""")

con.execute("""
COPY submolts_users
TO 'submolts_active_users.csv'
(FORMAT CSV, HEADER);
""")

# Submolts aggregated info
con.execute("""
CREATE TABLE submolts_details AS
SELECT 
    u.submolt AS submolt,
    active_users,
    total_comments
FROM submolts_users u
LEFT JOIN submolts_comments c
    ON u.submolt = c.submolt
                       
ORDER BY active_users DESC, total_comments DESC, submolt
""")

con.execute("""
COPY submolts_details
TO 'submolts_details.csv'
(FORMAT CSV, HEADER);
""")
