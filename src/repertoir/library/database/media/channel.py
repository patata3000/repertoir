from dataclasses import dataclass
from sqlite3 import Connection as DBConnection


@dataclass
class Channel:
    id: int
    ext_source_id: str
    name: str
    created_at: str


def insert_channel(db_conn: DBConnection, ext_source_id: str, channel_name: str) -> int:
    channel_id = db_conn.execute(
        """
INSERT INTO channel (ext_source_id, name)
VALUES (?, ?)
ON CONFLICT(ext_source_id) DO UPDATE
SET name = excluded.name
RETURNING id
        """,
        (ext_source_id, channel_name),
    ).fetchone()[0]
    return channel_id


def search_channel(db_conn: DBConnection, search_term: str) -> list[Channel]:
    channels = db_conn.execute(
        """
SELECT DISTINCT channel.id, channel.name, channel.ext_source_id, channel.created_at
FROM channel
JOIN video ON channel.id = video.channel_id
WHERE name LIKE ?
ORDER BY video.created_at DESC
        """,
        (f"%{search_term}%",),
    ).fetchall()
    return [
        Channel(
            id=channel[0],
            name=channel[1],
            ext_source_id=channel[2],
            created_at=channel[3],
        )
        for channel in channels
    ]
