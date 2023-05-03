import time

class PromptRunStats:
  def __init__(self, prompt, model):
    self.prompt = prompt
    self.provider_name, self.model_name = model.split("/")
    self.model = self.model_name

    self.start_time = None
    self.end_time = None

  def before_run(self):
    self.start_time = time.time()  

  def after_run(self):
    self.end_time = time.time()

  def get_stats(self):
    return {
      "prompt": self.prompt.template,
      "prompt_bytes": len(self.prompt.template),
      "model": self.model,
      "provider": self.provider_name,
      "start_time": self.start_time,
      "end_time": self.end_time,
      "elapsed_time": self.end_time - self.start_time
    }