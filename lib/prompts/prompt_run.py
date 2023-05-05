from ..llms.providers.openai import LLMProviderOpenAI
from ..llms.providers.anthropic import LLMProviderAnthropic

import time

from colored import fg, attr

def find_provider(provider_name):
  if provider_name == "openai":
    return LLMProviderOpenAI()
  elif provider_name == "anthropic":
    return LLMProviderAnthropic()
  else:
    raise Exception("Unknown provider: " + provider_name)

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

  def description(self, abbrev=True):
    c = self.config

    if abbrev:
      prompt = fg('blue') + "Prompt:     " + attr('reset') + self.prompt.text_abbrev(25) + " (" + str(self.prompt.text_len()) + " chars)\n"
    else:
      prompt = fg('blue') + "Prompt:     " + attr('reset') + "\n----\n" + self.prompt.text() + "\n----\n(" + str(self.prompt.text_len()) + " chars)\n\n"

    elapsed_time = fg('blue') + "Elapsed time: " + attr('reset') + str(round(self.elapsed_time, 2)) + "s  "

    if abbrev:
      completion = fg('blue') + "Completion: " + attr('reset') + self.response.completion_abbrev(25) + " (" + str(self.response.completion_len()) + " chars)\n"
    else:
      completion = fg('blue') + "Completion: " + attr('reset') + "\n----\n" + self.response.completion + "\n----\n(" + str(self.response.completion_len()) + " chars)\n\n"

    tokens_used = fg('blue') + "Tokens used: " + attr('reset') + str(self.response.tokens_used) + "\n"

    s =  prompt + completion + "\n" + elapsed_time + tokens_used

    return s


# takes prompt and model config, finds provider, runs the prompt
class PromptRun:
  def __init__(self, prompt, config):
    self.prompt = prompt
    self.config = config
    self.provider = find_provider(config['provider_name'])

  def run(self):
    result = PromptRunResult(self.prompt, self.config)
    
    result.before_run()

    response = self.provider.run(self.prompt, self.config)

    result.after_run()

    result.update_with_response(response)

    return result

