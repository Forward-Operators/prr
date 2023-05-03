import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from .prompt.prompt import Prompt
from .llms.providers.openai import LLMProviderOpenAI
from .llms.providers.anthropic import LLMProviderAnthropic
from .llms.stats import PromptRunStats
from .llms.response import ModelResponse

from colored import fg, attr

# takes prompt and model, finds provider, runs the prompt
class Runner:
  def __init__(self, prompt, model="openai/gpt-3.5-turbo"):
    self.prompt = prompt
    self.provider_name, self.model_name = model.split("/")
    self.model = self.model_name

    if self.provider_name == "openai":
      self.provider = LLMProviderOpenAI()
    elif self.provider_name == "anthropic":
      self.provider = LLMProviderAnthropic()
    else:
      raise Exception("Unknown provider: " + self.provider_name)

    self.stats = PromptRunStats(prompt, model)
    self.response = ModelResponse()

  def prompt_template_len(self):
    return len(self.prompt.template)

  def prompt_abbrev(self):
    if self.prompt_template_len() > 40:
      return self.prompt.template[0:40] + "..."
    else:
      return self.prompt.template

  def response_completion_len(self):
    return self.response.completion_len()

  def response_abbrev(self):
    return self.response.completion_abbrev()

  def model_id(self):
    return "/".join([self.provider_name, self.model_name])

  def run(self, options):
    eprint ('🧠 {model_id}: sending {template_bytes} bytes of prompt:\n{green}{prompt_abbrev}{normal}'.format(
      model_id=self.model_id(),
      prompt_abbrev=self.prompt_abbrev(),
      template_bytes=self.prompt_template_len(),
      green=fg('green'),
      normal=attr('reset')))
    
    self.stats.before_run()
    self.response = ModelResponse(self.provider.run(self.prompt, self.model, options))
    self.stats.after_run()

    _stats = self.stats.get_stats()
    elapsed_time = round(_stats['elapsed_time'], 2)

    eprint ('✅ {model_id}: received {response_bytes} bytes of response in {response_elapsed_time}s:\n{green}{response_abbrev}{normal}'.format(
      model_id=self.model_id(),
      response_abbrev=self.response_abbrev(),
      response_elapsed_time=elapsed_time,
      response_bytes=self.response_completion_len(),
      green=fg('green'),
      normal=attr('reset')))

  def get_stats(self):
    return self.stats.get_stats()
  
  def get_result(self):
    return self.response