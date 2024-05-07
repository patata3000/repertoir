import json
import os
import subprocess
from dataclasses import dataclass
from sqlite3 import Connection as DBConnection
from typing import Optional

from repertoir.config import INDEX_DIR_PATH, VIDEO_DIR_PATH
from repertoir.library.database.media.channel import insert_channel
from repertoir.library.database.media.video import insert_video


@dataclass
class Channel:
    name: str
    ext_source_id: str


@dataclass
class Video:
    ext_source_id: str
    title: str
    path: str


def _send_notification(
    title: str,
    body: str,
    print_id: bool = False,
    replace_id=None,
    actions: Optional[list[tuple[str, str]]] = None,
):
    args = []
    if print_id:
        args.append("--printid")
    if replace_id:
        args.extend(["--replace", replace_id])
    actions = actions or []
    for action in actions:
        args.append(f"--action={",".join(action)}")
    return (
        subprocess.check_output(["dunstify", title, body, *args])
        .decode("utf-8")
        .strip()
    )


def download_youtube_video(db_conn: DBConnection, url: str):
    notification_id = _send_notification(
        "Downloading video", "<i>Title incoming...</i>", print_id=True
    )
    channel_name, title = (
        subprocess.check_output(
            ["yt-dlp", "--no-download", "--print", "channel", "--get-title", url]
        )
        .decode("utf-8")
        .strip()
    ).split("\n")
    _send_notification(
        "Downloading video",
        f"<b>{channel_name}</b>\n{title}",
        replace_id=notification_id,
    )
    INFO_JSON_TEMPLATE_NAME = "%(id)s"
    VIDEO_TEMPLATE_NAME = "%(id)s.%(ext)s"
    base_call = [
        "yt-dlp",
        "--write-info-json",
        "--paths",
        f"{VIDEO_DIR_PATH}",
        "--paths",
        f"infojson:{INDEX_DIR_PATH}",
    ]
    info_json_filename, media_filename = (
        subprocess.check_output(
            [
                *base_call,
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
            *base_call,
            "-o",
            VIDEO_TEMPLATE_NAME,
            "-o",
            f"infojson:{INFO_JSON_TEMPLATE_NAME}",
            url,
        ]
    )
    _send_notification(
        "Downloaded video",
        f"<b>{channel_name}</b>\n{title}",
        replace_id=notification_id,
    )
    channel, video = extract_metadata(info_json_filename, media_filename)
    channel_id = insert_channel(db_conn, channel.ext_source_id, channel.name)
    insert_video(db_conn, video.ext_source_id, video.title, video.path, channel_id)
    result = _send_notification(
        "Video inserted",
        f"<b>{channel_name}</b>\n{title}",
        replace_id=notification_id,
        actions=[("open_video", title)],
    ).strip()
    if result == "open_video":
        subprocess.call(["xdg-open", os.path.join(VIDEO_DIR_PATH, video.path)])


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
