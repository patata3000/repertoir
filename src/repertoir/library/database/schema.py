import sqlite3 as sl
from sqlite3 import Cursor as DBCursor

from repertoir.config import DB_PATH


def get_connection():
    conn = sl.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def create_tables(db_cursor: DBCursor):
    db_cursor.execute(
        """
CREATE TABLE IF NOT EXISTS channel (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(channel_id)
);
        """
    )
    db_cursor.execute(
        """
CREATE TABLE IF NOT EXISTS video (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    title TEXT NOT NULL,
    path TEXT NOT NULL,
    channel_id INTEGER NOT NULL,
    UNIQUE(video_id),
    UNIQUE(title),
    UNIQUE(path),
    FOREIGN KEY(channel_id) REFERENCES channel(id)
);
        """
    )


def database_initiated(db_cursor: DBCursor) -> bool:
    names = db_cursor.execute(
        "select name from sqlite_schema where type = 'table'"
    ).fetchall()
    for name in names:
        if name[0] == "video":
            return True
    return False
