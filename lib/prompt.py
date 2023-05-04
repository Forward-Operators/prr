class Prompt:
  def __init__(self, template):
    self.template = template

  def text(self):
    return self.template
  
  def __str__(self):
    return self.text()
  
  def text_len(self):
    return len(self.text())
  
  def text_abbrev(self, max_len = 25):
    if self.text_len() > max_len:
      str = self.text()[0:max_len] + "..."
    else:
      str = self.text()

    return str.replace("\n", " ").replace("  ", " ")
