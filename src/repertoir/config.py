import os

# Raw data
VIDEO_STORAGE_PATH = "/home/guillaume/Videos/repertoire"
VIDEO_DIR_PATH = f"{VIDEO_STORAGE_PATH}/youtube/videos"
VIDEO_TMP_DIR_PATH = f"{VIDEO_STORAGE_PATH}/youtube/tmp_videos"
INDEX_DIR_PATH = f"{VIDEO_STORAGE_PATH}/youtube/index"


# Database
XDG_DATA_HOME = os.environ.get(
    "XDG_DATA_HOME", os.path.join(os.environ["HOME"], ".local", "share")
)
REPERTOIR_HOMEDIR = os.path.join(XDG_DATA_HOME, "repertoir")
DB_PATH = os.path.join(REPERTOIR_HOMEDIR, "repertoir.db")
