import time

class PromptRunResult:
  def __init__(self, prompt, config):
    self.prompt = prompt
    self.config = config
    self.start_time = None
    self.end_time = None
    self.elapsed_time = None

  def before_run(self):
    self.start_time = time.time()  

  def after_run(self):
    self.end_time = time.time()
    self.elapsed_time = self.end_time - self.start_time

  def update_with_response(self, response):
    self.response = response

  def metrics(self):
    return {
      'elapsed_time': self.elapsed_time,
      'tokens_used': self.response.tokens_used,
    }

