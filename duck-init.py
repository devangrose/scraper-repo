import duckdb

# Connect to an in-memory database (or specify a file path for persistence)
conn = duckdb.connect("./duck.db")

conn.execute("DROP TABLE IF EXISTS comments")
conn.execute("DROP TABLE IF EXISTS posts")

conn.execute("DROP SEQUENCE IF EXISTS postid")
conn.execute("DROP SEQUENCE IF EXISTS commentid")

conn.execute("""
    CREATE SEQUENCE postid START 1;
    CREATE SEQUENCE commentid START 1;
""")
# Create a table
conn.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY DEFAULT nextval('postid'),
        url VARCHAR(100),
        title VARCHAR(100),
        created_at TIMESTAMP,
        post_id INTEGER UNIQUE
    )
""")

# create a comments table with a fkey to the posts table
conn.execute("""
    CREATE TABLE comments (
        id INTEGER PRIMARY KEY DEFAULT nextval('commentid'),
        post_id INTEGER,
        text TEXT,
        sentiment TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    )
""")
