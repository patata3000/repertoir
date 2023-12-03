import json
import os
import subprocess
from dataclasses import dataclass
from sqlite3 import Connection as DBConnection

from repertoir.config import INDEX_DIR_PATH, VIDEO_DIR_PATH, VIDEO_TMP_DIR_PATH
from repertoir.library.database.manage_videos import insert_channel, insert_video


@dataclass
class Channel:
    name: str
    ext_source_id: str


@dataclass
class Video:
    ext_source_id: str
    title: str
    path: str


def _send_notification(title: str, body: str, *args):
    return (
        subprocess.check_output(["dunstify", title, body, *args])
        .decode("utf-8")
        .strip()
    )


def download_youtube_video(db_conn: DBConnection, url: str):
    notification_id = _send_notification(
        "Downloading video", "<i>Title incoming...</i>", "--printid"
    )
    title = (
        subprocess.check_output(["yt-dlp", "--no-download", "--get-title", url])
        .decode("utf-8")
        .strip()
    )
    subprocess.check_output(
        ["dunstify", "Downloading video", f"{title}", "--replace", notification_id]
    )
    INFO_JSON_TEMPLATE_NAME = "%(title)s_[%(id)s]"
    VIDEO_TEMPLATE_NAME = "%(title)s_[%(id)s].%(ext)s"
    info_json_filename, media_filename = (
        subprocess.check_output(
            [
                "yt-dlp",
                "--write-info-json",
                "--paths",
                f"{VIDEO_DIR_PATH}",
                "--paths",
                f"infojson:{INDEX_DIR_PATH}",
                "--print",
                f"{INFO_JSON_TEMPLATE_NAME}.info.json",
                "--print",
                VIDEO_TEMPLATE_NAME,
                url,
            ]
        )
        .decode("utf-8")
        .strip()
        .split("\n")
    )
    subprocess.call(
        [
            "yt-dlp",
            "--write-info-json",
            "--paths",
            f"{VIDEO_DIR_PATH}",
            "--paths",
            f"infojson:{INDEX_DIR_PATH}",
            "--paths",
            f"temp:{VIDEO_TMP_DIR_PATH}",
            "-o",
            VIDEO_TEMPLATE_NAME,
            "-o",
            f"infojson:{INFO_JSON_TEMPLATE_NAME}",
            url,
        ]
    )
    _send_notification("Downloaded video", title, "--replace", notification_id)
    channel, video = extract_metadata(info_json_filename, media_filename)
    channel_id = insert_channel(db_conn, channel.ext_source_id, channel.name)
    insert_video(db_conn, video.ext_source_id, video.title, video.path, channel_id)
    _send_notification("Video inserted", title, "--replace", notification_id)


def extract_metadata(info_json_filename: str, media_filename: str):
    info_json_path = os.path.join(INDEX_DIR_PATH, info_json_filename)
    with open(info_json_path, "r") as f:
        metadata = json.load(f)
    return (
        Channel(name=metadata["channel"], ext_source_id=metadata["channel_id"]),
        Video(
            title=metadata["title"], path=media_filename, ext_source_id=metadata["id"]
        ),
    )
