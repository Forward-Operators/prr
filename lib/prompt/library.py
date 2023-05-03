import os
import yaml

from .prompt import Prompt

class Library:
  def __init__(self, path):
    self.path = path

  def load_prompt(self, prompt_path, prompt_config_path=None):
    with open(prompt_path, 'r') as file:
      prompt_template = file.read()

    if prompt_config_path and os.path.isfile(prompt_config_path):
      with open(prompt_config_path, 'r') as file:
        prompt_config = yaml.load(file, Loader=yaml.FullLoader)
        return Prompt(prompt_template, prompt_config)
    
  def get_prompt_path(self, prompt_subpath):
    prompt_path = os.path.join(self.path, prompt_subpath)

    if os.path.isfile(prompt_path):
      # common/highest-peak is just a prompt file
      return prompt_path
    elif os.path.isdir(prompt_path):
      # common/highest-peak is a directory
      return os.path.join(prompt_path, "prompt")

  # full path to prompt file as argument    
  def get_prompt_config_path(self, full_prompt_path):
    dirname = os.path.dirname(full_prompt_path)
    return os.path.join(dirname, "config.yaml")

  def get_prompt(self, prompt_subpath="common/highest-peak"):
    full_prompt_path = self.get_prompt_path(prompt_subpath)
    prompt_config_path = self.get_prompt_config_path(full_prompt_path)

    return self.load_prompt(full_prompt_path, prompt_config_path)