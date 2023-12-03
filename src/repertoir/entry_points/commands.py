import click

from repertoir.library.database.schema import (
    create_tables,
    database_initiated,
    get_connection,
)
from repertoir.library.download_media import download_youtube_video
from repertoir.library.search_video_repertoir import (
    open_url_from_repertoire,
    play_video_from_repertoire,
)
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


@cli.group("search")
@click.option("--search-term", default="")
def cmd_search(search_term: str):
    pass


@cmd_search.command("play")
def cmd_play_video():
    with get_connection() as db_conn:
        play_video_from_repertoire(db_conn)


@cmd_search.command("url")
@click.option("--get-url", is_flag=True)
def cmd_open_url(get_url: bool):
    with get_connection() as db_conn:
        open_url_from_repertoire(db_conn)
