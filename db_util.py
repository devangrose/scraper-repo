import duckdb
from datetime import datetime

def save_post(title: str, url: str, post_id: int, created_at) -> None:
    conn = duckdb.connect("./duck.db")
    # conn.execute("INSERT INTO posts (title, url, post_id, created_at) VALUES (?, ?, ?, ?)", (title, url, post_id, created_at))
    # try to insert the post, if it already exists, update the created_at
    try:
        conn.execute("INSERT INTO posts (title, url, post_id, created_at) VALUES (?, ?, ?, ?)", (title, url, post_id, created_at))
    except:
        conn.execute("UPDATE posts SET title = ?, url = ?, created_at = ? WHERE post_id = ?", (title, url, created_at, post_id))


def save_comment(post_id: int, text: str, created_at: str, sentiment: str) -> None:
    conn = duckdb.connect("./duck.db")
    # conn.execute("INSERT INTO comments (post_id, comment) VALUES (?, ?)", (post_id, comment))
    # try to insert the comment, if it already exists, update the created_at and text
    try:
        conn.execute("INSERT INTO comments (post_id, text, created_at, sentiment) VALUES (?, ?, ?)", (post_id, text, created_at, sentiment))
    except:
        conn.execute("UPDATE comments SET text = ?, created_at = ?, sentiment = ? WHERE post_id = ?", (text, created_at, post_id, sentiment))

def get_posts() -> list:
    conn = duckdb.connect("./duck.db")
    result = conn.execute("SELECT * FROM posts").fetchall()
    return result

def get_comments(post_id: int) -> list:
    conn = duckdb.connect("./duck.db")
    result = conn.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,)).fetchall()
    return result

def get_most_recent_timestamp() -> str:
    conn = duckdb.connect("./duck.db")
    result = conn.execute("SELECT MAX(created_at) FROM posts").fetchone()
    return result[0]

def get_posts_with_no_comments() -> list:
    conn = duckdb.connect("./duck.db")
    result = conn.execute("SELECT * FROM posts WHERE id NOT IN (SELECT post_id FROM comments)").fetchall()
    return result