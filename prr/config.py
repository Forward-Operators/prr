import os

from dotenv import dotenv_values


def load_config():
    config = dotenv_values(os.path.expanduser("~/.prr_rc"))
    return config
