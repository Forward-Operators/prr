class ModelResponse():
  def __init__(self, result = {}):
    if 'completion' in result:
      self.completion = result['completion']

    if 'tokens_used' in result:
      self.tokens_used = result['tokens_used']

  def ready(self):
    return hasattr(self, 'completion')
  
  def completion_len(self):
    if self.ready():
      return len(self.completion)

    return 0

  def completion_abbrev(self, max_len = 25):
    if self.completion_len() > max_len:
      str = self.completion[0:max_len] + "..."
    else:
      str = self.completion

    return str.replace("\n", " ").replace("  ", " ")

  def __str__(self):
    s = "Completion: ["
    s += self.completion_abbrev(25) + "] "
    s += "Len: " + str(self.completion_len()) + " "
    s += "Tokens used: " + str(self.tokens_used)

    return s
