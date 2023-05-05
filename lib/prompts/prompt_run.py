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

  def __str__(self):
    s = "PromptRunResult: "
    s += "Config: " + str(self.config) + " "
    s += "Prompt: [" + str(self.prompt) + "] "
    s += "Elapsed time: " + str(round(self.elapsed_time, 2)) + "s "
    s += "Response: " + str(self.response)

    return s


  def description(self, abbrev=True):
    c = self.config

    if 'model_config_name' in c:
      model_config_name = c['model_config_name']
    else:
      model_config_name = None

    provider_name = c['provider_name']
    model_name = c['model_name']

    if model_config_name:
      model_name = f'{fg("green")}🤖 {model_config_name} ({provider_name}/{model_name}):\n{attr("reset")}'
    else:
      model_name = f'🤖 {provider_name}/{model_name}:\n'

    if abbrev:
      prompt = fg('blue') + "Prompt: " + attr('reset') + self.prompt.text_abbrev(25) + " (" + str(self.prompt.text_len()) + " chars)\n"
    else:
      prompt = fg('blue') + "Prompt: " + attr('reset') + "\n----\n" + self.prompt.text() + "\n----\n(" + str(self.prompt.text_len()) + " chars)\n\n"

    elapsed_time = fg('blue') + "Elapsed time: " + attr('reset') + str(round(self.elapsed_time, 2)) + "s\n"

    if 'temperature' in c:
      temperature = fg('blue') + "Temperature: " + attr('reset') + str(c['temperature']) + "\n"
    else:
      temperature = ""

    if 'max_tokens' in c:
      max_tokens = fg('blue') + "Max tokens: " + attr('reset') + str(c['max_tokens']) + "\n"
    else:
      max_tokens = ""


    if 'top_p' in c:
      top_p = fg('blue') + "Top P: " + attr('reset') + str(c['top_p']) + "\n"
    else:
      top_p = ""

    if 'top_k' in c:
      top_k = fg('blue') + "Top K: " + attr('reset') + str(c['top_k']) + "\n"
    else:
      top_k = ""

    options = temperature + max_tokens + top_p + top_k

    if abbrev:
      completion = fg('blue') + "Completion: " + attr('reset') + self.response.completion_abbrev(25) + " (" + str(self.response.completion_len()) + " chars)\n"
    else:
      completion = fg('blue') + "Completion: " + attr('reset') + "\n----\n" + self.response.completion + "\n----\n(" + str(self.response.completion_len()) + " chars)\n\n"

    tokens_used = fg('blue') + "Tokens used: " + attr('reset') + str(self.response.tokens_used) + "\n"

    s = model_name + "\n" + prompt + options + "\n" + completion + elapsed_time + tokens_used

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

