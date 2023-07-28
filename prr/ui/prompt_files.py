import hashlib
import os

from prr.prompt.prompt_loader import PromptConfigLoader


class PromptFiles:
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path

        self.load()

    def load(self):
        self.loader = PromptConfigLoader()
        self.prompt = self.loader.load_from_path(self.prompt_path)

        dependencies = self.loader.file_dependencies

        self.files = {}

        for file_path in dependencies:
            file_id = hashlib.md5(file_path.encode()).hexdigest()
            file_name = os.path.basename(file_path)
            self.files[file_id] = {"path": file_path, "name": file_name, "id": file_id}

    def get_file_contents(self, file_id):
        file_path = self.get_file_path(file_id)

        if file_path:
            with open(file_path, "r") as f:
                file_contents = f.read()
                return file_contents

    def get_file_path(self, file_id):
        _path = self.files.get(file_id)

        if _path:
            file_path = self.files[file_id]["path"]

            return file_path

        return None

    def update_file(self, file_id, new_file_contents):
        file_path = self.get_file_path(file_id)

        if file_path:
            with open(file_path, "w") as f:
                f.write(new_file_contents)
