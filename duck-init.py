import duckdb

# Connect to an in-memory database (or specify a file path for persistence)
conn = duckdb.connect("./duck.db")

# Create a table
conn.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        post_id INTEGER,
    )
""")

# create a comments table with a fkey to the posts table
conn.execute("""
    CREATE TABLE comments (
        id INTEGER PRIMARY KEY,
        post_id INTEGER,
        comment TEXT,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    )
""")
