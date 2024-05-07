import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from repertoir.config import VIDEO_DIR_PATH
from repertoir.library.database.media.channel import search_channel
from repertoir.library.database.media.video import search_video


def run_fzfmenu(entries: list[str]):
    output = subprocess.check_output(
        ["fzfmenu", "no-preview"], input="\n".join(entries).encode("utf-8")
    )
    return output.decode("utf-8").strip()


def preprocess_video_filepaths(list_video_files: list[Path]) -> dict[str, str]:
    return {filepath.stem: str(filepath) for filepath in list_video_files}


def get_filepath(filename: str):
    return os.path.join(VIDEO_DIR_PATH, filename)


def search_video_data(db_conn, search_term: str = "", last: bool = False):
    channel = None
    if last:
        return choose_video(db_conn, search_term, None, last=True)
    if search_term == "":
        channel = choose_channel(db_conn, search_term)
    return choose_video(db_conn, search_term, channel.id if channel else None)


def choose_channel(db_conn, search_term: str = ""):
    channels = search_channel(db_conn, search_term)
    channel_dict = {channel.name: channel for channel in channels}
    channel_name = run_fzfmenu([channel.name for channel in channels])
    if channel_name == "":
        return None
    return channel_dict[channel_name]


def choose_video(
    db_conn, search_term: str = "", channel_id: Optional[int] = None, last: bool = False
):
    videos = search_video(db_conn, search_term, channel_id, last)
    if len(videos) == 1 and last:
        return videos[0]
    video_dict = {video.title: video for video in videos}
    video_title = run_fzfmenu([video.title for video in videos])
    if video_title == "":
        return None
    return video_dict[video_title]


def play_video_from_repertoire(db_conn, search_term: str = "", last: bool = False):
    video_data = search_video_data(db_conn, search_term=search_term, last=last)
    if video_data is None:
        return
    filepath = get_filepath(video_data.filename)
    subprocess.run(["mpv", filepath, f'--force-media-title={video_data.channel_name}  ##  {video_data.title}'])


def open_url_from_repertoire(db_conn, search_term: str = "", last: bool = False):
    video_data = search_video_data(db_conn, search_term, last=last)
    if video_data is None:
        return
    url = f"https://www.youtube.com/watch?v={video_data.ext_source_id}"
    print(url, file=sys.stdout)
    subprocess.run(["xdg-open", url])
