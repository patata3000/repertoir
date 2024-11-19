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
    created_at: str
    channel_name: str


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
    db_conn: DBConnection,
    search_term: str,
    channel_id: Optional[int] = None,
    last: bool = False,
) -> list[Video]:
    if channel_id:
        videos = db_conn.execute(
            """
SELECT
  video.id,
  video.title,
  video.filename,
  video.channel_id,
  video.watched,
  video.ext_source_id,
  video.created_at,
  channel.name
FROM video
JOIN channel ON channel.id = video.channel_id
WHERE (title LIKE ? or filename LIKE ?) and channel_id = ?
ORDER BY video.created_at DESC
            """,
            (f"%{search_term}%", f"%{search_term}%", channel_id),
        ).fetchall()
    else:
        videos = db_conn.execute(
            """
SELECT 
  video.id,
  video.title,
  video.filename,
  video.channel_id,
  video.watched,
  video.ext_source_id,
  video.created_at,
  channel.name
FROM video
JOIN channel ON channel.id = video.channel_id
WHERE title LIKE ? or filename LIKE ?
ORDER BY video.created_at DESC
            """,
            (f"%{search_term}%", f"%{search_term}%"),
        ).fetchall()
    if last:
        videos = videos[:1]
    return [
        Video(
            id=video[0],
            title=video[1],
            filename=video[2],
            channel_id=video[3],
            watched=video[4],
            ext_source_id=video[5],
            created_at=video[6],
            channel_name=video[7],
        )
        for video in videos
    ]
