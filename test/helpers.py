import os
import tempfile


def remove_temp_file(path):
    os.remove(path)


def create_temp_file(content, extension=None):
    suffix = ""

    if extension:
        suffix = "." + extension

    # Create a temporary file with the specified extension
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
        temp.write(content.encode())
        temp_path = temp.name

    return temp_path
