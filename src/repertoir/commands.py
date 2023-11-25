import click

from .download_video import download_youtube_video
from .search_video_repertoir import search_video_repertoire


@click.group()
def cli():
    pass


@cli.command("download")
@click.argument("url")
def cmd_download_youtube_video(url: str):
    download_youtube_video(url)


@cli.command("search-video")
def cmd_search_video():
    search_video_repertoire()


if __name__ == "__main__":
    cli()
