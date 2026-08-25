import sqlite3
import logging

DB="blog.db"
logger = logging.getLogger(__name__)

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY,
            topic TEXT UNIQUE
        )
        """)
    logger.info("Database initialized: %s", DB)

def topic_exists(topic):
    with sqlite3.connect(DB) as conn:
        found = conn.execute("SELECT 1 FROM posts WHERE topic=?", (topic,)).fetchone()
    exists = found is not None
    logger.debug("Topic lookup completed: exists=%s", exists)
    return exists

def save_topic(topic):
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO posts(topic) VALUES(?)", (topic,))
    logger.info("Saved generated topic")