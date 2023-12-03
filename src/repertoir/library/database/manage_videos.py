from sqlite3 import Connection as DBConnection


def insert_video(
    db_conn: DBConnection, ext_source_id: str, title: str, path: str, channel_id: int
) -> int:
    return db_conn.execute(
        """
        INSERT INTO video (video_id, title, path, channel_id)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE
        SET title = excluded.title,
            path = excluded.path
        RETURNING id
        """,
        (ext_source_id, title, path, channel_id),
    ).fetchone()[0]


def insert_channel(db_conn: DBConnection, ext_source_id: str, channel_name: str) -> int:
    channel_id = db_conn.execute(
        """
        INSERT INTO channel (channel_id, name)
        VALUES (?, ?)
        ON CONFLICT(channel_id) DO UPDATE
        SET name = excluded.name
        RETURNING id
        """,
       (ext_source_id, channel_name),
    ).fetchone()[0]
    return channel_id
