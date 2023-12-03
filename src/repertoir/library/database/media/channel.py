from dataclasses import dataclass
from sqlite3 import Connection as DBConnection


@dataclass
class Channel:
    id: int
    ext_source_id: str
    name: str


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
            SELECT id, name, ext_source_id
            FROM channel
            WHERE name LIKE ?
        """,
        (f"%{search_term}%",),
    ).fetchall()
    return [
        Channel(
            id=channel[0],
            name=channel[1],
            ext_source_id=channel[2],
        )
        for channel in channels
    ]
