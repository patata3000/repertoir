import os
import subprocess
from pathlib import Path

BASE_PATH = "/home/guillaume/Videos/repertoire"


def video_repertoire():
    for dirpath, _dirnames, filenames in Path(BASE_PATH).walk():
        if dirpath.match("index$"):
            continue
        for filename in filenames:
            yield Path(os.path.join(dirpath, filename))


def run_fzfmenu(list_video_files: list[str]):
    subprocess.run(
        ["fzfmenu", "no-preview"], input="\n".join(list_video_files).encode("utf-8")
    )


def preprocess_video_filepaths(list_video_files: list[Path]) -> list[str]:
    return [filepath.suffix for filepath in list_video_files]



def search_video_repertoire():
    list_video_files = list(video_repertoire())
    list_video_files = preprocess_video_filepaths(list_video_files)
    run_fzfmenu(list_video_files)


if __name__ == "__main__":
    search_video_repertoire()
