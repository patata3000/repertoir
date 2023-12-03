import os

from repertoir.config import REPERTOIR_HOMEDIR


def init_data_home():
    os.makedirs(REPERTOIR_HOMEDIR, exist_ok=True)
