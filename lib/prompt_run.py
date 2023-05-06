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


# takes prompt and model config, finds provider, runs the prompt
class PromptRun:
  def __init__(self, prompt, service, service_config):
    self.prompt = prompt
    self.service = service
    self.service_config = service_config

  def run(self):
    result = PromptRunResult(self.prompt, self.service_config)
    
    result.before_run()

    response = self.service.run(self.prompt, self.service_config)

    result.after_run()

    result.update_with_response(response)

    return result

