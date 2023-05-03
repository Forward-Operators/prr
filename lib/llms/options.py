class ModelOptions():
  def __init__(self, options = {}):
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
