class ModelOptions():
  def __init__(self, options = {}):
    self.temperature = None
    self.max_tokens = None
    self.top_k = None
    self.top_p = None

    if 'temperature' in options:
      self.temperature = options['temperature']
    else:
      self.temperature = 1.0

    if 'max_tokens' in options:
      self.max_tokens = options['max_tokens']
    else:
      self.max_tokens = 32

    if 'top_k' in options:
      self.top_k = options['top_k']
    else:
      self.top_k = -1

    if 'top_p' in options:
      self.top_p = options['top_p']
    else:
      self.top_p = -1

  def description(self):
    parts = []

    if self.temperature != None:
      parts.append("t=" + str(self.temperature))

    if self.max_tokens != None:
      parts.append("max=" + str(self.max_tokens))

    if self.top_k != None:
      parts.append("k=" + str(self.top_k))

    if self.top_p != None:
      parts.append("p=" + str(self.top_p))

    return " ".join(parts)
