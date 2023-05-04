import os
import yaml

from .prompt import Prompt

class Library:
  def __init__(self, path="prompts"):
    """Initialize the Library class with a specified path."""
    self.path = path

  def load_prompt(self, prompt_path, prompt_config_path=None):
    """Load a prompt from a given prompt file and an optional config file.
    
    Args:
        prompt_path (str): The path to the prompt file.
        prompt_config_path (str, optional): The path to the prompt configuration file.
        
    Returns:
        Prompt: The Prompt object initialized with the loaded prompt template and configuration.
    """
    # Read the prompt template from the file
    with open(prompt_path, 'r') as file:
        # print ("Loading prompt: " + prompt_path)
        prompt_template = file.read()

    # If prompt_config_path is provided and the file exists, load the configuration
    if prompt_config_path and os.path.isfile(prompt_config_path):
        # print ("Loading prompt config: " + prompt_config_path)
        with open(prompt_config_path, 'r') as file:
            prompt_config = yaml.load(file, Loader=yaml.FullLoader)
            return Prompt(prompt_template, prompt_config)
        
    return Prompt(prompt_template)

  def get_prompt_path(self, prompt_path):
      """Get the full path of a prompt file given its subpath.
      
      Args:
          prompt_subpath (str): The subpath to the prompt file or directory, like "common/dingo-dog"
          
      Returns:
          str: The full path to the prompt file.
      """

      if os.path.isfile(prompt_path):
        # If the provided path is a prompt file
        return prompt_path
      elif os.path.isdir(prompt_path):
        # If the provided path is a directory, we either have "prompt" file or "prompt" directory
        return self.get_prompt_path(os.path.join(prompt_path, "prompt"))

  def get_prompt_config_path(self, full_prompt_path):
      """Get the full path of a prompt configuration file given the full path to the prompt file.
      
      Args:
          full_prompt_path (str): The full path to the prompt file.
          
      Returns:
          str: The full path to the prompt configuration file.
      """
      full_prompt_path_dirname = os.path.dirname(full_prompt_path)
      y = os.path.join(full_prompt_path_dirname, "config.yaml")
      print(y)
      return os.path.join(full_prompt_path_dirname, "config.yaml")

  def get_prompt(self, prompt_subpath="common/highest-peak"):
      """Load and return a Prompt object given a subpath to the prompt file.
      
      Args:
          prompt_subpath (str, optional): The subpath to the prompt file or directory. Defaults to "common/highest-peak".
          
      Returns:
          Prompt: The loaded Prompt object including config YAML file if available.
      """

      full_prompt_subpath = os.path.join(self.path, prompt_subpath)
      
      full_prompt_path = self.get_prompt_path(full_prompt_subpath)

      prompt_config_path = self.get_prompt_config_path(full_prompt_path)

      return self.load_prompt(full_prompt_path, prompt_config_path)