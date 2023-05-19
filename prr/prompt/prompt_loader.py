import os

import yaml

from prr.prompt import Prompt
from prr.prompt.prompt_config import PromptConfig
from prr.prompt.prompt_template import (
    PromptTemplate,
    PromptTemplateMessages,
    PromptTemplateSimple,
)


class PromptConfigLoader:
    def __init__(self):
        self.file_dependencies = []
        self.config = None

    def load_from_path(self, path):
        self.path = path
        self.config = PromptConfig(self.__search_path(), os.path.basename(path))

        if self.__is_file_yaml(path):
            # prompt is in yaml config file format
            self.__load_yaml_file(path)
        else:
            # simple text (or jinja) file, no config
            self.__load_text_file(path)

        self.__add_file_dependencies()

        return self.config

    #####################################

    def __is_file_yaml(self, path):
        root, extension = os.path.splitext(path)

        if extension == ".yaml":
            return True

        return False

    def __search_path(self):
        return os.path.dirname(self.path)

    def __load_text_file(self, path):
        self.config.load_from_template_contents_at_path(path)

    def __load_yaml_file(self, path):
        try:
            with open(path, "r") as stream:
                self.config.load_from_config_contents(stream.read())

        except yaml.YAMLError as exc:
            print(exc)

    def __add_file_dependencies(self):
        self.__add_file_dependency(self.path)

        for file_dependency in self.config.file_dependencies():
            self.__add_file_dependency(file_dependency)

    def __add_file_dependency(self, file_path):
        if os.path.isabs(file_path):
            absolute_path = file_path
        else:
            absolute_path = os.path.join(
                os.path.dirname(self.path), os.path.basename(file_path)
            )

        if not absolute_path in self.file_dependencies:
            self.file_dependencies.append(absolute_path)
