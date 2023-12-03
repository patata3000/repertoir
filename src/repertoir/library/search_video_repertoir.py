import os
import subprocess
from pathlib import Path

from repertoir.config import VIDEO_STORAGE_PATH


def video_repertoire():
    for dirpath, _dirnames, filenames in Path(VIDEO_STORAGE_PATH).walk():
        if dirpath.match("index$"):
            continue
        for filename in filenames:
            yield Path(os.path.join(dirpath, filename))


def run_fzfmenu(list_video_files: list[str]):
    output = subprocess.check_output(
        ["fzfmenu", "no-preview"], input="\n".join(list_video_files).encode("utf-8")
    )
    return output.decode("utf-8").strip()


def preprocess_video_filepaths(list_video_files: list[Path]) -> dict[str, str]:
    return {filepath.stem: str(filepath) for filepath in list_video_files}


def search_video_repertoire():
    video_dict = list(video_repertoire())
    video_dict = preprocess_video_filepaths(video_dict)
    filename = run_fzfmenu(list(video_dict.keys()))
    subprocess.run(["mpv", video_dict[filename]])
