import os

from .prompt import Prompt

class PromptLoader:
  def __init__(self, prompt_path):
    if not os.path.isfile(prompt_path):
      raise Exception(f"Prompt file not found: {prompt_path}")
    
    self.path = prompt_path

  def load(self):
    if os.path.exists(self.path):
      return Prompt(self.path)
