class Prompt:
  def __init__(self, template):
    self.template = template

  def text(self):
    return self.template
  
  def __str__(self):
    return self.text()