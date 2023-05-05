from ..llms.providers.openai import LLMProviderOpenAI
from ..llms.providers.anthropic import LLMProviderAnthropic

import time

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

    prompt = "[blue]Prompt[/blue]:     "

    if abbrev:
      prompt = prompt + self.prompt.text_abbrev(25) + " (" + str(self.prompt.text_len()) + " chars)\n"
    else:
      prompt = prompt + "\n----[yellow]\n" + self.prompt.text() + "\n[/yellow]----\n(" + str(self.prompt.text_len()) + " chars)\n\n"

    elapsed_time = "[blue]Elapsed time[/blue]: " + str(round(self.elapsed_time, 2)) + "s  "

    completion = "[blue]Completion[/blue]: "

    if abbrev:
      completion = completion + self.response.completion_abbrev(25) + " (" + str(self.response.completion_len()) + " chars)\n"
    else:
      completion = completion + "\n----\n[green]" + self.response.completion + "[/green]\n----\n(" + str(self.response.completion_len()) + " chars)\n\n"

    tokens_used = "[blue]Tokens used[/blue]: " + str(self.response.tokens_used) + "\n"

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

