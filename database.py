import sqlite3

DB="blog.db"

def init_db():
    conn=sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY,
        topic TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

def topic_exists(topic):
    conn=sqlite3.connect(DB)
    cur=conn.execute("SELECT 1 FROM posts WHERE topic=?",(topic,))
    found=cur.fetchone()
    conn.close()
    return found is not None

def save_topic(topic):
    conn=sqlite3.connect(DB)
    conn.execute("INSERT INTO posts(topic) VALUES(?)",(topic,))
    conn.commit()
    conn.close()