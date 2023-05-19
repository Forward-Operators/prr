import os

import yaml

from . import Prompt
from .prompt_template import PromptTemplate, PromptTemplateSimple, PromptTemplateMessages
from .prompt_config import PromptConfig

class PromptConfigLoader:
  def __init__(self):
    self.dependency_files = []
    self.config = None
  
  def load_from_path(self, path):
    self.path = path
    self.config = PromptConfig(self.__search_path(), os.path.basename(path))
    self.__add_file_dependency(path)

    if self.__is_file_yaml(path):
      # prompt is in yaml config file format
      self.__load_yaml_file(path)
    else:
      # simple text (or jinja) file, no config
      self.__load_text_file(path)

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

  def __add_file_dependency(self, path):
    if not path in self.dependency_files:
      self.dependency_files.append(path)
