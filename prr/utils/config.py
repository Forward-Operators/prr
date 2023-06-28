import os

from dotenv import dotenv_values


def ensure_api_key(config, api_key_variable_name):
    _value = config.get(api_key_variable_name, None)

    if _value is None:
        raise Exception(
            f'API key or access variable "{api_key_variable_name}" not set in ~/.prr_rc'
        )

    return _value


def load_config():
    config = dotenv_values(os.path.expanduser("~/.prr_rc"))
    return config
