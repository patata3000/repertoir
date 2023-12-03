import click

from repertoir.library.database.schema import (
    create_tables,
    database_initiated,
    get_connection,
)
from repertoir.library.download_video import download_youtube_video
from repertoir.library.search_video_repertoir import search_video_repertoire
from repertoir.library.setup_repertoir import init_data_home


@click.group()
def cli():
    init_data_home()
    with get_connection() as db_conn:
        cursor = db_conn.cursor()
        if not database_initiated(cursor):
            print("Database not initiated. Creating database...")
            create_tables(cursor)


@cli.command("download")
@click.argument("url")
def cmd_download_youtube_video(url: str):
    with get_connection() as db_conn:
        download_youtube_video(db_conn, url)


@cli.command("search-video")
def cmd_search_video():
    search_video_repertoire()
