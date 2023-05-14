import os
import tempfile

def create_temp_file(content, extension):
    # Create a temporary file with the specified extension
    with tempfile.NamedTemporaryFile(suffix='.' + extension, delete=False) as temp:
        temp.write(content.encode())
        temp_path = temp.name

    return temp_path


def remove_temp_file(path)
    os.remove(temp_path)
