class Prompt:
  def __init__(self, template, config={}):
    self.template = template
    self.config = config

  def text(self, model="openai/gpt-4"):
    return self.template