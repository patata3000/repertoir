from dataclasses import dataclass
from sqlite3 import Connection as DBConnection
from typing import Optional


@dataclass
class Video:
    id: int
    ext_source_id: str
    title: str
    filename: str
    channel_id: int
    watched: bool


def insert_video(
    db_conn: DBConnection,
    ext_source_id: str,
    title: str,
    filename: str,
    channel_id: int,
) -> int:
    return db_conn.execute(
        """
            INSERT INTO video (ext_source_id, title, filename, channel_id)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(ext_source_id) DO UPDATE
            SET title = excluded.title,
                filename = excluded.filename
            RETURNING id
        """,
        (ext_source_id, title, filename, channel_id),
    ).fetchone()[0]


def search_video(
    db_conn: DBConnection, search_term: str, channel_id: Optional[int] = None
) -> list[Video]:
    if channel_id:
        videos = db_conn.execute(
            """
                SELECT id, title, filename, channel_id, watched, ext_source_id
                FROM video
                WHERE (title LIKE ? or filename LIKE ?) and channel_id = ?
            """,
            (f"%{search_term}%", f"%{search_term}%", channel_id),
        ).fetchall()
    else:
        videos = db_conn.execute(
            """
                SELECT id, title, filename, channel_id, watched, ext_source_id
                FROM video
                WHERE title LIKE ? or filename LIKE ?
            """,
            (f"%{search_term}%", f"%{search_term}%"),
        ).fetchall()
    return [
        Video(
            id=video[0],
            title=video[1],
            filename=video[2],
            channel_id=video[3],
            watched=video[4],
            ext_source_id=video[5],
        )
        for video in videos
    ]
