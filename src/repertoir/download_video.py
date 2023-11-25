import json
import subprocess

BASE_PATH = "/home/guillaume/Videos/repertoire"


def download_youtube_video(url: str):
    subprocess.call(
        [
            "yt-dlp",
            "--write-info-json",
            "--no-download",
            "--paths",
            f"{BASE_PATH}/youtube/index",
            url,
        ]
    )
    filename = (
        subprocess.check_output(
            [
                "yt-dlp",
                "--no-download",
                "--get-filename",
                url,
            ]
        )
        .decode("utf-8")
        .strip()
    )
    json_file = filename.replace(".webm", ".info.json")
    subprocess.call(["dunstify", f'"Downloading {filename.replace(".webm", "")}"'])
    info_json = None
    with open(f"{BASE_PATH}/youtube/index/{json_file}") as fp:
        info_json = json.load(fp)
    uploader = info_json["uploader"]
    uploader = uploader.replace(" ", "_")
    subprocess.call(
        [
            "yt-dlp",
            "--paths",
            f"{BASE_PATH}/youtube/{uploader}",
            url,
        ]
    )


